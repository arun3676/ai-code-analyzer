def get_code_analysis_prompt(code: str, language: str = "auto-detect") -> str:
    """Generate a focused prompt for practical code analysis."""
    return f"""
You are an expert code reviewer. Analyze this {language} code for practical issues that matter to developers.

Code to analyze:
{code}

Provide a focused analysis with complete, readable sentences. Do NOT use markdown symbols like ### or ** in your response.

1. QUALITY_SCORE: Rate 0-100 (consider bugs, readability, maintainability)

2. SUMMARY: One complete sentence describing what this code does

3. BUG_DETECTION: 
   - List actual bugs or logical errors found
   - Include potential crashes or exceptions
   - Mention edge cases not handled
   (Write complete sentences, skip if none found)

4. CODE_QUALITY_ISSUES:
   - Poor naming or structure problems
   - Code readability issues  
   - Maintainability concerns
   (Focus on practical fixes, write complete sentences)

5. SECURITY_VULNERABILITIES:
   - Injection risks (SQL, XSS, etc.)
   - Insecure data handling
   - Authentication/authorization flaws
   (Only include actual security risks, write complete sentences)

6. QUICK_FIXES: 
   - Top 3 specific improvements with examples
   - Focus on high-impact, easy changes
   - Write complete actionable sentences

Format each section as clear, complete sentences. Be specific and actionable. Skip sections if no issues found.
"""

def get_github_analysis_prompt(repo_structure: str, main_files: str) -> str:
    """Generate prompt for GitHub repository analysis."""
    return f"""
Analyze this GitHub repository structure and key files. Provide clear, complete analysis without using markdown symbols.

Repository Structure:
{repo_structure}

Main Files Content:
{main_files}

Provide analysis focusing on:

1. PROJECT_OVERVIEW: Write one clear sentence about what this project does

2. ARCHITECTURE_QUALITY: 
   - Project structure assessment (write complete sentences)
   - Code organization quality (write complete sentences)
   - Missing important files like tests, docs, etc. (write complete sentences)

3. CRITICAL_ISSUES:
   - Security vulnerabilities across files (write complete sentences)
   - Major bugs or design flaws (write complete sentences)
   - Dependencies/configuration problems (write complete sentences)

4. IMPROVEMENT_PRIORITIES:
   - Top 5 specific things to fix first (write complete sentences)
   - Missing features or best practices (write complete sentences)
   - Code quality improvements needed (write complete sentences)

Write clear, complete sentences without markdown symbols. Be practical and focus on actionable feedback for the repository owner.
"""

def get_comparison_prompt(code: str, language: str = "auto-detect") -> str:
    """Generate a prompt for multi-model comparison."""
    return f"""
As an expert code reviewer, analyze this {language} code:
{code}

Provide a concise but thorough analysis covering:
- Main functionality
- Code quality (rate 0-100)
- Critical issues
- Top 3 improvements
- Security/performance concerns

Be specific and actionable in your feedback.
""" 