import requests
import os

def get_ollama_models():
    """
    Fetch available models from Ollama.
    """
    url = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/api/tags"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return [{"name": m["name"], "provider": "ollama"} for m in models]
    except Exception:
        pass
    return []

def get_lm_studio_models():
    """
    Fetch available models from LM Studio.
    """
    url = os.environ.get("LM_STUDIO_HOST", "http://localhost:1234") + "/v1/models"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            models = response.json().get("data", [])
            return [{"name": m["id"], "provider": "lm_studio"} for m in models]
    except Exception:
        pass
    return []

def get_all_models():
    """
    Get a list of all detected local models plus OpenAI.
    """
    models = [{"name": "gpt-3.5-turbo", "provider": "openai"}, {"name": "gpt-4", "provider": "openai"}]
    models.extend(get_ollama_models())
    models.extend(get_lm_studio_models())
    return models
