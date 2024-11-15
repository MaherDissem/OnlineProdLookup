import os
import google.generativeai as genai
import time


class GeminiLLM:
    def __init__(self, model_name: str, max_attempts=5):
        self.model_name = model_name
        self.max_attempts = max_attempts
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel(self.model_name)

    def generate_text(self, prompt: str) -> str:
        attempt = 0
        while True:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                # Check if the error is a 429 error (rate limit exceeded)
                if "429" in str(e):
                    attempt += 1
                    print(
                        f"Rate limit exceeded. Sleeping for {60 * attempt} seconds (attempt {attempt})"
                    )
                    time.sleep(
                        60 * attempt
                    )  # Exponential backoff (increases sleep time after each attempt)
                    if attempt > self.max_attempts:
                        raise Exception("Rate limit exceeded. Please try again later.")
                else:
                    # Raise other exceptions
                    raise e


# Example of usage
if __name__ == "__main__":
    gemini_llm = GeminiLLM("gemini-1.5-flash")
    prompt = "What is the price of the product?"
    print(gemini_llm.generate_text(prompt))
