class Prompter:

    def __init__(self, product_title: str) -> None:
        self.product_title = product_title

    def get_price_websearch_prompt(self) -> str:
        """
        Generates a prompt for a web search engine to look for the price of a product.
        """
        return f"""Price of {self.product_title}"""

    def get_weight_websearch_prompt(self) -> str:
        """
        Generates a prompt for a web search engine to look for the weight of a product.
        """
        return f"""Weight of {self.product_title}"""

    def get_llm_price_prompt(self, webpage_content: str) -> str:
        """
        Generates a prompt for a language model to predict the price of a product.
        """
        return f"""Given the content of the following webpage, return the price of {self.product_title}.
        You must only return the price and its currency, and nothing else.
        If the price is not found, return 'No information about price in the webpage'.
        \n\nWebpage content:\n{webpage_content}"""

    def get_llm_weight_prompt(self, webpage_content: str) -> str:
        """
        Generates a prompt for a language model to predict the weight of a product.
        """
        return f"""Given the content of the following webpage, return the weight of {self.product_title}.
        You must only return the weight and its unit, and nothing else.
        If the weight is not found, return 'No information about weight in the webpage'.
        \n\nWebpage content:\n{webpage_content}"""
    