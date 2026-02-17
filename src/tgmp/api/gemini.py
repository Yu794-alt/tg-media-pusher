from google import genai
import config

MODEL_FLASH = "gemini-2.5-flash"

client = genai.Client(api_key=config.GEMINI_API_KEY)

# context = 'I got new message what should I say? don`t say that you AI. Keep your answer with few words refer to me. Describe in Russian'
context = (
    'Can you analise CV docs and return json object where list of tags are keys and value queues your raiting in from 1 to 5 for tags technologies from CV '
    'example: { javaScript: 5/5, java: 3/5} where tags were javaScript and java '
    'dont use any formatting container just send me as string'
    'PLEASE return JSON, keep string same at all time - with this format'
    '{"key": "val", "key": "val"}'
    'if technologies not exist just set your rating 0/5. Max rating 5. Here is tags:')


def generate_content(tags, cv):
    response = client.models.generate_content(

        model=MODEL_FLASH,
        contents=[cv, f"{context} + {tags} +  and CV"],
    )
    return response.text


def upload_file(filepath):
    myfile = client.files.upload(file=filepath)
    print(f"file uploaded {myfile=}")
    return myfile
