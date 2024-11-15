from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re


class WebPageParser:
    def __init__(self, url: str) -> None:
        """
        Initializes the WebPageParser with a URL.
        Args:
            url (str): The URL of the webpage to parse.
        """
        self.url = url
        self.driver = None
        self.soup = None

    def setup_driver(self) -> None:
        """Sets up the Selenium WebDriver with Chrome."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        # Try to fool websites into thinking we are a real user
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        )
        chrome_options.add_argument("accept-language=en-US,en;q=0.9")
        chrome_options.add_argument("accept-encoding=gzip, deflate, br")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

    def fetch_page(self) -> None:
        """Fetches the webpage and loads its content."""
        if self.driver is None:
            self.setup_driver()

        self.driver.get(self.url)
        page_source = self.driver.page_source
        self.soup = BeautifulSoup(page_source, "html.parser")

    def post_process_text(self, text: str) -> str:
        """
        Processes the raw text extracted from the page.
        Args:
            text (str): The raw text to process.
        Returns:
            str: The processed text.
        """
        # Remove extra spaces and newlines.
        processed_text = re.sub(r"\s+", " ", text)
        return processed_text

    def get_parsed_text(self) -> str:
        """Extracts and processes the page's full text."""
        if self.soup is None:
            raise ValueError("Page source not fetched. Call 'fetch_page()' first.")

        raw_text = self.soup.text
        processed_text = self.post_process_text(raw_text)
        return processed_text

    def close_driver(self) -> None:
        """Closes the Selenium WebDriver."""
        if self.driver:
            self.driver.quit()

    def parse(self) -> None:
        """Main method to parse the page."""
        try:
            self.fetch_page()
            processed_text = self.get_parsed_text()
            return processed_text
        finally:
            self.close_driver()


# Usage Example
if __name__ == "__main__":
    url = "https://aftermarket.express/caterpillar/2610017"
    parser = WebPageParser(url)
    output = parser.parse()
    print(output)
    