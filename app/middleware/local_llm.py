import ollama
from app.middleware.config import Config as cfg


class LocalLlm:
    """
    A wrapper around the Ollama API to generate text using a specified model and context.

    Attributes:
    - model_name (str): Name of the model to use for text generation.
    - model_ctx (int): Maximum context length for the model.
    """

    def __init__(
        self, model_name: str = cfg.model_name, model_ctx: int = cfg.model_ctx
    ):
        self.model_name = model_name
        self.model_ctx = model_ctx

    def generate_text(self, prompt: str, num_ctx: int = None, seed: int = 0) -> str:
        """
        Generates text based on a given prompt.

        Args:
        - prompt (str): Input text for the model to generate a response.
        - num_ctx (int, optional): Context length for this specific generation. Defaults to instance's model_ctx.
        - seed (int, optional): Seed for reproducibility of results. Default is 0.
        - log (bool, optional): If True, prints debug information. Default is False.

        Returns:
        - str: The generated response text or an error message if generation fails.
        """
        context_length = num_ctx if num_ctx is not None else self.model_ctx

        try:
            response = ollama.generate(
                prompt=prompt,
                model=self.model_name,
                options={"num_ctx": context_length, "seed": seed},
            )

            if "response" in response:
                return response["response"]
            else:
                return "Error: Unexpected response format from Ollama API."

        except ConnectionError:
            return "Error: Could not connect to Ollama API. Please check your connection and try again."
        except Exception as e:
            return f"Error generating text: {str(e)}"


# Example of usage
if __name__ == "__main__":
    local_llm = LocalLlm()
    prompt = """What do you know about "Goodwin FlowGuard 120"."""
    print(local_llm.generate_text(prompt))
