# OnlineProdLookup

This is a lightweight FastAPI application for retrieving additional online information about products by searching the web. 

Given a JSON file containing product details (like the product name and ID), the application queries the internet using the DuckDuckGo API for information such as price, weight, etc. 
The application selects top URLs from the search results, and in parallel scrapes them using Selenium to handle dynamic js content.
The extracted text is sent to either a local LLM or the Gemini API for information retrieval using predefined prompts.
The retrieved information is then added to the input JSON.

# Folder structure
```
├── app/                             # Source code directory
│   ├── middleware.py 
│   │    ├── config.py        # Sets configuration parameters.
│   │    ├── local_llm.py     # Code for running a local LLM using Ollama.
│   │    ├── gemini_llm.py    # Code for calling the Gemini LLM.
│   │    ├── prompts.py       # Generates prompts for the LLM or search engine given a product name and/or a webpage.
│   │    ├── web_scrape.py    # Parses content of URLs with Selenium to handle JavaScript.
│   │    ├── web_search.py    # Handles web search queries with DuckDuckGo.
│   │    ├── utils.py         # Contains utility functions.
│   │    └── processPrompt.py # Extracts product information from the scraped URLs.
│   ├── templates/
│   │    └── form.html        # FastAPI HTML template for user input.
│   ├── main.py               # FastAPI server entry point.
```

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/MaherDissem/OnlineProdLookup.git
cd OnlineProdLookup
```

### 2. Create and activate a virtual environment
```
python -m venv virtual
source 
```

### 3. Install dependencies
To use the local LLM, install [Ollama](https://ollama.com/download/windows) and download the desired model. It must then be set in `app/middleware/config.py`. 
For example:
```
ollama pull llama3.1:8b-instruct-q4_0
```

Otherwise, if using Gemini, define the API key as an environment variable.
```
export API_KEY=<YOUR_API_KEY>
```
For obtaining Gemini API key visit [Google AI for Devs](https://ai.google.dev/gemini-api/docs/api-key).

Then install the remaining dependencies:
```
pip install -r requirements.txt
```
   Note: Selenium needs Google Chrome to be installed.
   
### 4. Run the app
```
uvicorn app.main:app --reload
```
Then visit http://localhost:8000 to access the application.
