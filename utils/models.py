import requests
from typing import List, Dict

def get_local_models() -> List[str]:
    """Fetch available models from Ollama"""
    try:
        response = requests.get('http://localhost:11434/api/tags')
        if response.status_code == 200:
            models = response.json()
            return [model['name'] for model in models['models']]
        return []
    except:
        return [] 