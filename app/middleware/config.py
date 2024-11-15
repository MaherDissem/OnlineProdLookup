from dataclasses import dataclass

@dataclass
class Config:
    # LLM configuration
    llm_selection = "gemini" # "local" or "gemini"

    # Gemini LLM
    gemini_model_name: str = "gemini-1.5-flash"

    # Local LLM
    model_name: str = "llama3.1:8b-instruct-q4_0"
    model_ctx: int = 4 * 1024

    # Web search
    nbr_links: int = 5

    # Save output to file
    save_to_file: bool = True
