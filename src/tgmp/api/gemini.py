from google import genai
import config

MODEL_FLASH="gemini-2.5-flash"

client = genai.Client(api_key = "AIzaSyC6jN9ZUcD85uzCag3Nv3E6U2MmneciSD4")

def generate_content():
    response = client.models.generate_content(
        model=MODEL_FLASH,
        contents="2+2",
    )
    print(response.text)


