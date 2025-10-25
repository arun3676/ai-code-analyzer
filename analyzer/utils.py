import re
from typing import Dict, Any, Tuple
from pygments.lexers import guess_lexer
from pygments.util import ClassNotFound
from .llm_clients import LLMClientManager

def detect_language_with_llm(code: str) -> str:
    """Detect the programming language of a code snippet using an LLM."""
    try:
        llm_manager = LLMClientManager()
        # Prioritize Hugging Face for this task if available
        model = "huggingface" if "huggingface" in llm_manager.get_available_models() else list(llm_manager.get_available_models().keys())[0]
        prompt = f"""
        Analyze the following code snippet and identify its programming language. 
        Respond with only the language name (e.g., 'python', 'java', 'javascript', 'go', 'cpp', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'csharp', 'c').
        If you are unsure, respond with 'unknown'.

        Code:
        ```
        {code}
        ```

        Language:
        """
        response = llm_manager.query(model, prompt, temperature=0.1)
        if response.success:
            detected_language = response.content.strip().lower()
            if detected_language and detected_language != "unknown":
                return detected_language
    except Exception as e:
        print(f"LLM-based language detection failed: {e}")
    return "unknown"

def detect_language(code: str) -> str:
    """Detect the programming language using LLM first for accurate detection, then fallback to pattern matching."""
    # Try LLM-based detection first for accurate results
    detected = detect_language_with_llm(code)
    if detected != "unknown":
        return detected
    
    # Fallback to pattern matching only if LLM fails
    code_lower = code.lower()
    
    # HTML detection (check first as it's very common and specific)
    if re.search(r'<html|<head|<body|<div|<span|<p\s|class\s*=|id\s*=', code, re.IGNORECASE):
        return "html"
    
    # CSS detection (check early as it's specific)
    if re.search(r'\.\w+\s*\{|@media|@import|background:|color:|font-|margin:|padding:', code, re.IGNORECASE):
        return "css"
    
    # Go language detection (check early as it's most specific)
    if re.search(r'package\s+main|func\s+\w+\s*\(|import\s*\(', code, re.IGNORECASE):
        return "go"
    
    # Python language detection
    if re.search(r'def\s+\w+\s*\(|import\s+\w+|from\s+\w+\s+import|if\s+__name__\s*==\s*["\']__main__["\']', code, re.IGNORECASE):
        return "python"
    
    # JavaScript language detection (more specific patterns)
    js_patterns = [
        r'function\s+\w+\s*\([^)]*\)\s*\{',  # function declaration with body
        r'const\s+\w+\s*=\s*\([^)]*\)\s*=>',  # arrow function
        r'let\s+\w+\s*=\s*\([^)]*\)\s*=>',    # arrow function with let
        r'var\s+\w+\s*=\s*\([^)]*\)\s*=>',    # arrow function with var
        r'console\.log\s*\(',                  # console.log
        r'document\.getElementById',           # DOM manipulation
        r'addEventListener\s*\(',              # event listeners
        r'require\s*\(|import\s+.*\s+from',    # module imports
        r'export\s+(default\s+)?(function|const|class)',  # exports
    ]
    
    # TypeScript detection (check before JavaScript)
    if re.search(r'interface\s+\w+|type\s+\w+\s*=|:\s*\w+\[\]|:\s*string\s*[;=]|:\s*number\s*[;=]', code, re.IGNORECASE):
        return "typescript"
    
    # If it matches JavaScript patterns
    for pattern in js_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            return "javascript"
    
    # Java language detection
    if re.search(r'public\s+class\s+\w+|System\.out\.println|import\s+java\.', code, re.IGNORECASE):
        return "java"
    
    # C++ language detection
    if re.search(r'#include\s*<|std::|using\s+namespace\s+std', code, re.IGNORECASE):
        return "cpp"
    
    # C language detection
    if re.search(r'#include\s*<|int\s+main\s*\(|printf\s*\(', code, re.IGNORECASE):
        return "c"
    
    # C# language detection
    if re.search(r'using\s+System|namespace\s+\w+|public\s+class\s+\w+', code, re.IGNORECASE):
        return "csharp"
    
    # Rust language detection
    if re.search(r'fn\s+\w+\s*\(|let\s+\w+\s*:|use\s+\w+::', code, re.IGNORECASE):
        return "rust"
    
    # PHP language detection
    if re.search(r'<\?php|echo\s+|\$\w+\s*=', code, re.IGNORECASE):
        return "php"
    
    # Ruby language detection
    if re.search(r'def\s+\w+\s*|puts\s+|require\s+', code, re.IGNORECASE):
        return "ruby"
    
    # Swift language detection
    if re.search(r'func\s+\w+\s*\(|let\s+\w+\s*:|var\s+\w+\s*:', code, re.IGNORECASE):
        return "swift"
    
    # Kotlin language detection
    if re.search(r'fun\s+\w+\s*\(|val\s+\w+\s*=|var\s+\w+\s*=', code, re.IGNORECASE):
        return "kotlin"
    
    # Fallback to Pygments if no pattern matches
    try:
        from pygments.lexers import guess_lexer
        from pygments.util import ClassNotFound
        lexer = guess_lexer(code)
        return lexer.name.lower()
    except (ClassNotFound, ImportError):
        return "unknown"
    return "unknown"

def parse_analysis_result(text: str, model: str = None) -> Dict[str, Any]:
    """Parse LLM response into structured format with new focused categories."""
    result = {
        'quality_score': 75,  # default
        'detected_language': None,  # AI-detected language
        'summary': '',
        'bugs': [],
        'quality_issues': [],
        'security_vulnerabilities': [],
        'quick_fixes': [],
        # Legacy fields for compatibility
        'strengths': [],
        'issues': [],
        'suggestions': [],
        'security_concerns': [],
        'performance_notes': []
    }
    
    # Extract detected language first
    language_patterns = [
        r'(?:DETECTED_LANGUAGE|language)[:\s]*([a-z]+)(?:\s|$|\.|,)',
        r'^language[:\s]*([a-z]+)(?:\s|$|\.|,)',
        r'(?:programming\s+language)[:\s]*([a-z]+)(?:\s|$|\.|,)',
    ]
    
    for pattern in language_patterns:
        lang_match = re.search(pattern, text, re.IGNORECASE)
        if lang_match:
            detected_lang = lang_match.group(1).strip().lower()
            # Validate it's a known language
            known_languages = ['python', 'javascript', 'java', 'cpp', 'c', 'rust', 'go', 'php', 'ruby', 'swift', 'kotlin', 'typescript', 'csharp', 'html', 'css']
            if detected_lang in known_languages:
                result['detected_language'] = detected_lang
                break
    
    # Extract quality score
    score_patterns = [
        r'(?:QUALITY_SCORE|quality[_\s]*score)[:\s]*(\d+)(?:/100)?',
        r'(?:score|rating)[:\s]*(\d+)(?:/100)?'
    ]
    
    for pattern in score_patterns:
        score_match = re.search(pattern, text, re.IGNORECASE)
        if score_match:
            result['quality_score'] = int(score_match.group(1))
            break
    
    # Extract sections with new focused format
    sections = {
        # New focused sections
        'summary': r'(?:SUMMARY|summary)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'bugs': r'(?:BUG_DETECTION|bug[s]?|logical\s+error)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'quality_issues': r'(?:CODE_QUALITY_ISSUES|quality\s+issue|readability)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'security_vulnerabilities': r'(?:SECURITY_VULNERABILITIES|security\s+vulnerabilit|security\s+risk)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'quick_fixes': r'(?:QUICK_FIXES|improvement|suggestion)[s]?[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        
        # Legacy sections for backward compatibility
        'strengths': r'(?:strength|positive|good)[s]?[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'issues': r'(?:issue|problem)[s]?[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'suggestions': r'(?:suggestion|recommendation)[s]?[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'security_concerns': r'(?:security\s+concern)[s]?[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)',
        'performance_notes': r'(?:performance|optimization)[:\s]*(.+?)(?=\n\s*(?:\d+\.|[A-Z_]+:)|$)'
    }
    
    for key, pattern in sections.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            if key == 'summary':
                # Clean up summary and remove markdown symbols
                clean_summary = re.sub(r'^[:\-\s]*', '', content).split('\n')[0].strip()
                clean_summary = re.sub(r'#+\s*', '', clean_summary)  # Remove ### symbols
                result[key] = clean_summary
            else:
                # Extract bullet points and clean them
                items = []
                
                # Try different bullet point patterns
                bullet_patterns = [
                    r'^\s*[-•*]\s*(.+)$',  # Standard bullets
                    r'^\s*\d+\.\s*(.+)$',  # Numbered lists
                    r'^\s*[◦▪▫]\s*(.+)$',  # Alternative bullets
                ]
                
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.lower() in ['none', 'none found', 'skip if none found']:
                        continue
                    
                    # Clean up markdown symbols and extra characters
                    line = re.sub(r'#+\s*', '', line)  # Remove ### symbols
                    line = re.sub(r'^\*+\s*', '', line)  # Remove ** symbols
                    line = re.sub(r'^[:\-\s]*', '', line)  # Remove colons and dashes
                        
                    # Try each bullet pattern
                    item_found = False
                    for bullet_pattern in bullet_patterns:
                        bullet_match = re.match(bullet_pattern, line)
                        if bullet_match:
                            clean_item = bullet_match.group(1).strip()
                            clean_item = re.sub(r'#+\s*', '', clean_item)  # Remove ### from items
                            if clean_item and len(clean_item) > 5:  # Avoid very short items
                                items.append(clean_item)
                            item_found = True
                            break
                    
                    # If no bullet pattern, treat as potential item if it's substantial
                    if not item_found and len(line) > 15:  # Increased minimum length
                        clean_line = re.sub(r'#+\s*', '', line)  # Remove ### symbols
                        items.append(clean_line)
                
                # If no bullet points found, split by sentences and clean
                if not items and content.strip():
                    sentences = re.split(r'[.!?]+', content)
                    for sentence in sentences:
                        clean_sentence = sentence.strip()
                        clean_sentence = re.sub(r'#+\s*', '', clean_sentence)  # Remove ### symbols
                        if clean_sentence and len(clean_sentence) > 15:
                            items.append(clean_sentence)
                
                result[key] = items[:4]  # Limit to 4 items per section
    
    return result

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def validate_code(code: str, language: str) -> Dict[str, Any]:
    """
    Perform basic validation on the code.
    
    Args:
        code (str): The code to validate
        language (str): The programming language
        
    Returns:
        dict: Validation result with 'is_valid' and 'message' keys
    """
    if not code.strip():
        return {"is_valid": False, "message": "Code is empty"}
    
    # Basic validation rules
    validation_rules = {
        'python': [
            (r'^[ \t]*[^\s#]', "Code appears to have inconsistent indentation"),
        ],
        'javascript': [
            (r'\{[^}]*$', "Unclosed curly braces detected"),
            (r'\([^)]*$', "Unclosed parentheses detected"),
        ],
        'java': [
            (r'public\s+class\s+\w+', "Should contain a public class"),
        ],
        'cpp': [
            (r'#include', "Should contain include statements"),
        ],
        'c': [
            (r'#include', "Should contain include statements"),
        ]
    }
    
    # Check for common issues
    lines = code.split('\n')
    
    # Check for extremely long lines
    max_line_length = 200
    for i, line in enumerate(lines):
        if len(line) > max_line_length:
            return {
                "is_valid": False, 
                "message": f"Line {i+1} is very long ({len(line)} characters). Consider breaking it up."
            }
    
    # Language-specific validation
    if language in validation_rules:
        for pattern, message in validation_rules[language]:
            if language == 'python' and pattern == r'^[ \t]*[^\s#]':
                # Check indentation consistency for Python
                indentation_types = set()
                for line in lines:
                    if line.strip() and line[0] in [' ', '\t']:
                        if line.startswith(' '):
                            indentation_types.add('spaces')
                        elif line.startswith('\t'):
                            indentation_types.add('tabs')
                
                if len(indentation_types) > 1:
                    return {"is_valid": False, "message": "Mixed tabs and spaces for indentation"}
            
            elif not re.search(pattern, code, re.MULTILINE):
                return {"is_valid": False, "message": message}
    
    return {"is_valid": True, "message": "Code appears to be well-formed"}

def clean_response(response: str) -> str:
    """
    Clean and format the LLM response.
    
    Args:
        response (str): Raw response from LLM
        
    Returns:
        str: Cleaned and formatted response
    """
    if not response:
        return "No response generated"
    
    # Remove excessive whitespace
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', response)
    cleaned = cleaned.strip()
    
    # Ensure proper markdown formatting
    # Fix bullet points
    cleaned = re.sub(r'^\s*[-*]\s*', '- ', cleaned, flags=re.MULTILINE)
    
    # Fix numbered lists
    cleaned = re.sub(r'^\s*(\d+)\.\s*', r'\1. ', cleaned, flags=re.MULTILINE)
    
    # Ensure code blocks are properly formatted
    cleaned = re.sub(r'```(\w+)?\s*\n', r'```\1\n', cleaned)
    
    return cleaned 