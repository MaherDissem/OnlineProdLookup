from app.middleware.local_llm import LocalLlm
from app.middleware.gemini_llm import GeminiLLM
from app.middleware.config import Config as cfg


def get_llm_instance():
    if cfg.llm_selection == "local":
        return LocalLlm()
    elif cfg.llm_selection == "gemini":
        return GeminiLLM(model_name=cfg.gemini_model_name)
    else:
        raise NotImplementedError("Invalid LLM selection")
