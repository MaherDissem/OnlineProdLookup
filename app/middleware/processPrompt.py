import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from app.middleware.prompts import Prompter
from app.middleware.utils import get_llm_instance
from app.middleware.web_search import search_duckduckgo
from app.middleware.web_scrape import WebPageParser
from app.middleware.config import Config as cfg


def promptResponse(json_string: str) -> str:
    """Process the input JSON string and return the augmented product details."""
    input_dict = json.loads(json_string)
    for product_object in tqdm(input_dict):
        product_title = product_object["title"]
        product_object["augmented"] = {}

        # lookup price
        pred_price = search_price(product_title)
        pred_price = pred_price.strip()
        product_object["augmented"]["price"] = pred_price

        # lookup weight
        pred_weight = search_weight(product_title)
        pred_weight = pred_weight.strip()
        product_object["augmented"]["weight"] = pred_weight

        print(f"{product_title} - Price: {pred_price}, Weight: {pred_weight}")

    # return the response
    output_json = json.dumps(input_dict, indent=4)
    response = f"Here are the product details:\n{output_json}"

    # optionally save the response to a file
    if cfg.save_to_file:
        with open("response.json", "w") as file:
            file.write(response)

    return response


def search_price(product_title: str) -> str:
    product_prompter = Prompter(product_title)
    price_search_prompt = product_prompter.get_price_websearch_prompt()
    search_results = search_duckduckgo(price_search_prompt, max_results=cfg.nbr_links)

    def process_result(result: dict) -> str:
        """Search for the price of a single search result."""
        link = result["href"]
        webpage_parser = WebPageParser(link)
        llm = get_llm_instance()

        webpage_content = webpage_parser.parse()
        llm_price_prompt = product_prompter.get_llm_price_prompt(webpage_content)
        price = llm.generate_text(llm_price_prompt)
        return price

    # Run each result in parallel
    with ThreadPoolExecutor() as executor:
        future_to_price = {
            executor.submit(process_result, result): result for result in search_results
        }
        webpage_results = []
        for future in as_completed(future_to_price):
            try:
                price = future.result()
                webpage_results.append(price)
            except Exception as e:
                print(f"Error processing result: {e}")
    return select_best_llm_response(webpage_results)


def search_weight(product_title: str) -> str:
    product_prompter = Prompter(product_title)
    weight_search_prompt = product_prompter.get_price_websearch_prompt()
    search_results = search_duckduckgo(weight_search_prompt, max_results=cfg.nbr_links)

    def process_result(result: dict) -> str:
        """Search for the weight of a single search result."""
        link = result["href"]
        webpage_parser = WebPageParser(link)
        llm = get_llm_instance()

        webpage_content = webpage_parser.parse()
        llm_weight_prompt = product_prompter.get_llm_weight_prompt(webpage_content)
        weight = llm.generate_text(llm_weight_prompt)
        return weight

    # Run each result in parallel
    with ThreadPoolExecutor() as executor:
        future_to_weight = {
            executor.submit(process_result, result): result for result in search_results
        }
        webpage_results = []
        for future in as_completed(future_to_weight):
            try:
                weight = future.result()
                webpage_results.append(weight)
            except Exception as e:
                print(f"Error processing result: {e}")
    return select_best_llm_response(webpage_results)


def select_best_llm_response(llm_responses: list) -> str:
    """Naively select the most appropriate from the list of LLM responses."""
    llm_responses = [
        response
        for response in llm_responses
        if any(char.isdigit() for char in response) and len(response) < 100
    ]
    return min(llm_responses, key=len) if llm_responses else "No information found."


if __name__ == "__main__":
    json_path = "products.json"
    with open(json_path, "r", encoding="utf-8") as file:
        json_string = file.read()
    response = promptResponse(json_string)
