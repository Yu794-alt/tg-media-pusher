from google import genai
import config

MODEL_FLASH="gemini-2.5-flash"

client = genai.Client(api_key = config.GEMINI_API_KEY)

context = 'I got new message what should I say? don`t say that you AI. Keep your answer with few words refer to me. Describe in Russian'

def generate_content(contents):
    response = client.models.generate_content(
        model=MODEL_FLASH,
        contents=f"{context} + {contents}",
    )
    return response.text


