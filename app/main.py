from fastapi import FastAPI, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.middleware.processPrompt import promptResponse
import json

app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def process_form(request: Request, json_file: UploadFile = File(...)):
    # Read the uploaded JSON file
    json_content = await json_file.read()

    try:
        # Parse the JSON content to ensure it's valid
        json_data = json.loads(json_content)

        # Format the JSON data with indentation for better readability
        formatted_json_string = json.dumps(json_data, indent=4, sort_keys=True)
    except json.JSONDecodeError:
        formatted_json_string = "Invalid JSON file"

    # Pass the formatted JSON string to the promptResponse function
    newResponse = promptResponse(formatted_json_string)

    # Purge (delete) the uploaded file content after processing
    await json_file.close()

    return templates.TemplateResponse(
        "form.html", {"request": request, "response": newResponse}
    )
