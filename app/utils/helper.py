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