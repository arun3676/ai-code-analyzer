from typing import Dict, Any, List, Optional, Generator, Literal
import time
import requests
import os
import re
import hashlib
import json
from tqdm import tqdm

from .llm_clients import LLMClientManager, LLMResponse
from .prompts import get_code_analysis_prompt, get_comparison_prompt, get_github_analysis_prompt
from .utils import detect_language, parse_analysis_result

ModelType = Literal["codet5", "deepseek-finetuned", "deepseek-finetuned-remote"]

class CodeAnalyzer:
    """Main code analysis engine with support for APIs, local models, and GitHub integration."""
    
    def __init__(self, cache_dir: str = None, precision: str = "fp16"):
        # API-based models
        self.llm_manager = LLMClientManager()
        self.available_models = self.llm_manager.get_available_models()
    
        # Local/Remote Hugging Face models
        self.model_type: Optional[ModelType] = None
        self.model_id: Optional[str] = None
        self.adapter_path: Optional[str] = None
        self.remote_api_url: Optional[str] = None
        
        self.cache_dir = cache_dir
        self.precision = precision.lower().strip()
        self.cache = {}
        
        if cache_dir is not None:
            os.makedirs(cache_dir, exist_ok=True)
        self._load_cache()

    def _get_cache_key(self, code: str) -> str:
        """Generate a unique cache key for a piece of code and model type."""
        combined = f"{self.model_type}:{self.model_id}:{code}"
        return hashlib.md5(combined.encode()).hexdigest()

    def _load_cache(self):
        """Load analysis cache from disk if available."""
        if self.cache_dir is None:
            self.cache = {}
            return
        
        cache_file = os.path.join(self.cache_dir, "analysis_cache.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    self.cache = json.load(f)
                print(f"📁 Loaded {len(self.cache)} cached analyses")
            except (json.JSONDecodeError, IOError):
                self.cache = {}

    def _save_cache(self):
        """Save the analysis cache to disk."""
        if self.cache_dir is None:
            return
            
        cache_file = os.path.join(self.cache_dir, "analysis_cache.json")
        with open(cache_file, 'w') as f:
            json.dump(self.cache, f)

    def _check_cache(self, code: str) -> Optional[Dict[str, Any]]:
        """Check if an analysis for the given code is in the cache."""
        cache_key = self._get_cache_key(code)
        return self.cache.get(cache_key)

    def _save_to_cache(self, code: str, result: Dict[str, Any]):
        """Save an analysis result to the cache."""
        cache_key = self._get_cache_key(code)
        self.cache[cache_key] = result
        self._save_cache()

    def analyze_code(
        self,
        code: str,
        model: str,
        language: Optional[str] = None,
        max_tokens: int = 1024,
    ) -> Dict[str, Any]:
        """
        Analyze code using a specified LLM provider.
        This is a non-streaming, direct analysis method.
        Language detection is now handled by AI for accuracy.
        """
        # Skip local language detection - let AI handle it for accuracy
        if language is None:
            language = "auto-detect"  # Let AI detect it
        
        prompt = get_code_analysis_prompt(code, language, model)
        
        start_time = time.time()
        response = self.llm_manager.query(model, prompt)
        total_time = time.time() - start_time
        
        if response.success:
            structured_data = parse_analysis_result(response.content, model)
            
            # Use AI-detected language if available, otherwise fallback to auto
            detected_lang = structured_data.get('detected_language')
            if detected_lang:
                language = detected_lang.upper()
            else:
                # Fallback to LLM-based detection if not in response
                language = detect_language(code).upper()
            
            result = {
                "raw_response": response.content,
                "quality_score": structured_data.get('quality_score', 0),
                "execution_time": total_time,
                "model": response.model,
                "cached": False,
                **structured_data,
                "language": language,
                "line_count": len(code.splitlines()),
            }
        else:
            result = {'error': response.error}
            
        return result

    def analyze_code_remote(self, code: str, max_tokens: int = 300) -> Dict[str, Any]: # Increased token limit
        """Analyze code using a remote Hugging Face Space API."""
        if not self.remote_api_url:
            return {'error': 'Remote API URL is not configured.'}

        cached_result = self._check_cache(code)
        if cached_result:
            cached_result["cached"] = True
            return cached_result
            
        start_time = time.time()
        
        try:
            # First, try FastAPI endpoint /analyze
            response = requests.post(
                f"{self.remote_api_url}/analyze",
                json={"code": code, "max_tokens": max_tokens},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            
            # Assuming the remote API returns a structured response
            total_time = time.time() - start_time
            result = {
                "raw_response": data.get("analysis", str(data)),
                "quality_score": data.get("quality_score", 0),
                "execution_time": total_time,
                "model": data.get("model", "remote-deepseek"),
                "cached": False,
                "bugs": data.get("bugs", []),
                "security_vulnerabilities": data.get("security_vulnerabilities", []),
                "quality_issues": data.get("quality_issues", []),
                "quick_fixes": data.get("quick_fixes", []),
                "language": data.get("language", detect_language(code)),
                "line_count": data.get("line_count", len(code.splitlines())),
            }
            self._save_to_cache(code, result)
            return result

        except requests.exceptions.RequestException as e:
            # Fallback for Gradio or other errors
            return {'error': f"Remote analysis failed: {e}"}
    
    def analyze_github_repo(self, repo_url: str, model: str = None) -> Dict[str, Any]:
        """Analyze a GitHub repository."""
        start_time = time.time()
        
        # Use first available model if none specified
        if not model or model not in self.available_models:
            model = list(self.available_models.keys())[0]
        
        try:
            # Parse GitHub URL
            if not repo_url.startswith('https://github.com/'):
                return {'error': 'Please provide a valid GitHub repository URL'}
            
            # Extract owner and repo
            parts = repo_url.replace('https://github.com/', '').split('/')
            if len(parts) < 2:
                return {'error': 'Invalid GitHub repository URL format'}
            
            owner, repo = parts[0], parts[1]
            
            # Get repository structure and key files
            repo_data = self._fetch_github_repo_data(owner, repo)
            if 'error' in repo_data:
                return repo_data
            
            # Generate analysis prompt
            prompt = get_github_analysis_prompt(
                repo_data['structure'], 
                repo_data['main_files']
            )
            
            # Query LLM
            response = self.llm_manager.query(model, prompt)
            
            if response.success:
                analysis = self._parse_github_analysis(response.content)
                analysis['raw_response'] = response.content
                analysis['repository_info'] = repo_data['info']
            else:
                analysis = {
                    'error': response.error,
                    'project_overview': f"Analysis failed: {response.error}",
                    'architecture_quality': [],
                    'critical_issues': [],
                    'improvement_priorities': []
                }
            
            # Add metadata
            analysis['model'] = response.model
            analysis['execution_time'] = round(time.time() - start_time, 2)
            analysis['repo_url'] = repo_url
            
            return analysis
            
        except Exception as e:
            return {
                'error': f"GitHub analysis failed: {str(e)}",
                'execution_time': round(time.time() - start_time, 2)
            }
    
    def _fetch_github_repo_data(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository data from GitHub API."""
        try:
            # GitHub API endpoints
            api_base = f"https://api.github.com/repos/{owner}/{repo}"
            
            # Get repository info
            headers = {}
            if os.getenv('GITHUB_TOKEN'):
                headers['Authorization'] = f"token {os.getenv('GITHUB_TOKEN')}"
            
            repo_response = requests.get(api_base, headers=headers)
            if repo_response.status_code != 200:
                return {'error': f'Repository not found or private: {owner}/{repo}'}
            
            repo_info = repo_response.json()
            
            # Get file tree
            tree_response = requests.get(f"{api_base}/git/trees/main?recursive=1", headers=headers)
            if tree_response.status_code != 200:
                # Try master branch
                tree_response = requests.get(f"{api_base}/git/trees/master?recursive=1", headers=headers)
            
            if tree_response.status_code != 200:
                return {'error': 'Could not fetch repository structure'}
            
            tree_data = tree_response.json()
            
            # Build structure and get key files
            structure = self._build_repo_structure(tree_data['tree'])
            main_files = self._get_key_files(owner, repo, tree_data['tree'], headers)
            
            return {
                'info': {
                    'name': repo_info['name'],
                    'description': repo_info.get('description', 'No description'),
                    'language': repo_info.get('language', 'Unknown'),
                    'stars': repo_info.get('stargazers_count', 0),
                    'forks': repo_info.get('forks_count', 0),
                    'size': repo_info.get('size', 0)
                },
                'structure': structure,
                'main_files': main_files
            }
            
        except Exception as e:
            return {'error': f'Failed to fetch repository data: {str(e)}'}
    
    def _build_repo_structure(self, tree: List[Dict]) -> str:
        """Build a readable repository structure."""
        structure_lines = []
        dirs = set()
        
        for item in tree[:50]:  # Limit to first 50 items
            if item['type'] == 'tree':
                dirs.add(item['path'])
            else:
                structure_lines.append(f"📄 {item['path']}")
        
        for dir_path in sorted(dirs):
            structure_lines.append(f"📁 {dir_path}/")
        
        return '\n'.join(structure_lines[:30])  # Limit output
    
    def _get_key_files(self, owner: str, repo: str, tree: List[Dict], headers: Dict) -> str:
        """Get content of key files like README, main source files."""
        key_files = []
        
        # Priority files to analyze
        priority_patterns = [
            'README.md', 'readme.md', 'README.txt',
            'package.json', 'requirements.txt', 'Cargo.toml', 'go.mod',
            'main.py', 'index.js', 'main.js', 'app.py', 'server.js'
        ]
        
        for item in tree:
            if item['type'] == 'blob':
                filename = item['path'].split('/')[-1]
                
                # Check if it's a priority file
                if filename in priority_patterns or any(
                    pattern in filename.lower() for pattern in ['main', 'index', 'app']
                ):
                    try:
                        file_response = requests.get(
                            f"https://api.github.com/repos/{owner}/{repo}/contents/{item['path']}", 
                            headers=headers
                        )
                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            if file_data.get('encoding') == 'base64':
                                import base64
                                content = base64.b64decode(file_data['content']).decode('utf-8', errors='ignore')
                                key_files.append(f"\n--- {item['path']} ---\n{content[:1000]}")  # First 1000 chars
                    except:
                        continue
                
                if len(key_files) >= 5:  # Limit to 5 key files
                    break
        
        return '\n'.join(key_files)
    
    def _parse_github_analysis(self, text: str) -> Dict[str, Any]:
        """Parse GitHub repository analysis results."""
        result = {
            'project_overview': '',
            'architecture_quality': [],
            'critical_issues': [],
            'improvement_priorities': [],
            'onboarding_guide': [],
            'tech_stack_rationale': [],
            'api_endpoint_summary': [],
        }
        
        sections = {
            'project_overview': r'(?:PROJECT_OVERVIEW|project\s+overview)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'architecture_quality': r'(?:ARCHITECTURE_QUALITY|architecture|structure)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'critical_issues': r'(?:CRITICAL_ISSUES|critical|major\s+issue)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'improvement_priorities': r'(?:IMPROVEMENT_PRIORITIES|improvement|priorit)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'onboarding_guide': r'(?:ONBOARDING_GUIDE|onboarding|setup)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'tech_stack_rationale': r'(?:TECH_STACK_RATIONALE|tech\s+stack|stack\s+rationale)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
            'api_endpoint_summary': r'(?:API_ENDPOINT_SUMMARY|api\s+endpoint|endpoints)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                
                if key == 'project_overview':
                    # Clean project overview
                    clean_overview = content.split('\n')[0].strip()
                    clean_overview = re.sub(r'#+\s*', '', clean_overview)  # Remove ### symbols
                    clean_overview = re.sub(r'^\*+\s*', '', clean_overview)  # Remove ** symbols
                    result[key] = clean_overview
                else:
                    # Extract and clean bullet points
                    items = []
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.lower() in ['none', 'none found']:
                            # Clean up markdown symbols and extra characters
                            line = re.sub(r'#+\s*', '', line)  # Remove ### symbols
                            line = re.sub(r'^\*+\s*', '', line)  # Remove ** symbols
                            line = re.sub(r'^[-•*]\s*', '', line)  # Remove bullet markers
                            line = re.sub(r'^[:\-\s]*', '', line)  # Remove colons and dashes
                            
                            if len(line) > 10:  # Only include substantial content
                                items.append(line)
                    
                    # If no structured items found, try to extract sentences
                    if not items and content.strip():
                        sentences = re.split(r'[.!?]+', content)
                        for sentence in sentences:
                            clean_sentence = sentence.strip()
                            clean_sentence = re.sub(r'#+\s*', '', clean_sentence)  # Remove ### symbols
                            clean_sentence = re.sub(r'^\*+\s*', '', clean_sentence)  # Remove ** symbols
                            if clean_sentence and len(clean_sentence) > 15:
                                items.append(clean_sentence)
                    
                    result[key] = items[:4]  # Limit to 4 items per section
        
        return result
    
    def analyze_with_all_models(self, code: str, language: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """Analyze code using all available models."""
        results = {}
        
        for model_key in self.available_models:
            results[model_key] = self.analyze_code(code, model_key, language)
        
        return results
    
    def compare_analyses(self, results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Compare results from different models with focus on critical issues."""
        comparison = {
            'average_score': 0,
            'consensus_bugs': [],
            'consensus_security': [],
            'model_scores': {},
            'best_model': None,
            'analysis_time': sum(r['execution_time'] for r in results.values())
        }
        
        # Calculate average score and find best model
        scores = []
        for model, result in results.items():
            if 'error' not in result:
                score = result['quality_score']
                scores.append(score)
                comparison['model_scores'][model] = score
        
        if scores:
            comparison['average_score'] = round(sum(scores) / len(scores), 1)
            best_model = max(comparison['model_scores'].items(), key=lambda x: x[1])
            comparison['best_model'] = best_model[0]
        
        # Find consensus on critical issues
        all_bugs = []
        all_security = []
        
        for result in results.values():
            if 'error' not in result:
                all_bugs.extend(result.get('bugs', []))
                all_security.extend(result.get('security_vulnerabilities', []))
        
        # Simple consensus: issues mentioned by multiple models
        def find_consensus(items):
            consensus = []
            for item in items:
                if any(item.lower() in other.lower() or other.lower() in item.lower() 
                      for other in items if other != item):
                    if item not in consensus:
                        consensus.append(item)
            return consensus[:3]  # Top 3 consensus items
        
        comparison['consensus_bugs'] = find_consensus(all_bugs)
        comparison['consensus_security'] = find_consensus(all_security)
        
        return comparison 