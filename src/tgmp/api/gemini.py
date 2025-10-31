from google import genai
import config

MODEL_FLASH="gemini-2.5-flash"

client = genai.Client(api_key = "AIzaSyC6jN9ZUcD85uzCag3Nv3E6U2MmneciSD4")

def generate_content(contents):
    response = client.models.generate_content(
        model=MODEL_FLASH,
        contents=contents,
    )
    return response.text


