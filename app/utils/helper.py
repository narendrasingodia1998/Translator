import aiofiles
from sanic.exceptions import  BadRequest
from app.utils.lang_code import lang_code

def get_code(language):
    return lang_code[language.strip().lower()]


def get_language(code):
    code_lang = {v: k for k, v in lang_code.items()}
    language = code_lang[code]
    return language[0].upper() + language[1:]

def copy_data(request,response):
    '''
    Copy the data from the request and language_detector respone
    Args :
        request :
        respones :
    Return : dict 
    '''
    request_data = {
    'source_language': response['source_language'],
    'source_text' : request['source_text'],
    'target_language': request['target_language']}
    return request_data

def split_text_into_chunks(text, chunk_size):
    chunks = []
    current_chunk = ""

    for word in text.split():
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    # Add the last chunk, if any
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

async def read_file_(input_file):
    try: 
        async with aiofiles.open(input_file, mode='r') as file:
            input_text = await file.read()
            return input_text
    except:
        BadRequest("Input file doesnot exist")

async def write_file_(input_file,input_text):
    async with aiofiles.open(input_file,mode='w') as file:
        await file.write(input_text)
