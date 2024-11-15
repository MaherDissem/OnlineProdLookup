from duckduckgo_search import DDGS # https://pypi.org/project/duckduckgo-search/


def search_duckduckgo(prompt: str, max_results: int = 5):
    """
    Searches DuckDuckGo for the given prompt and returns results.

    Args:
    - prompt (str): The search query.
    - max_results (int): The maximum number of results to return. Default is 5.

    Returns:
    - list: A list of dictionaries containing search results with 'title', 'href', and 'body' keys.
    """
    try:
        ddgs = DDGS()
        results = ddgs.text(prompt, max_results=max_results)
        return list(results)

    except Exception as e:
        return f"Error during search: {str(e)}"


# Example usage
if __name__ == "__main__":
    prompt = """ CAT, 261-0017 VALVE GP-CONTROL. PESSCO IS OFFERING 1 V120623-8 """
    search_results = search_duckduckgo(prompt, max_results=5)
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['href']}")
        print(f"Snippet: {result['body']}\n")
        print("-" * 50)
