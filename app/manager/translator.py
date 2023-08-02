from app.manager.client import Client
from app.manager.language_detect import DetectManager
from app.utils.helper import copy_data
from app.model.request import TranslatorRequest
from app.utils.constants import UrlEndPoints
from app.model.response import TranslatorResponse
from app.utils.helper import get_code,read_file_,write_file_
from sanic.exceptions import  BadRequest
from app.Config import config
from sanic.exceptions import SanicException
import aiofiles
import asyncio
from sanic.log import logger
from app.utils.helper import split_text_into_chunks

class Translator(Client):

    @classmethod
    async def validate(cls,request):
        '''
        Detect source language based on source text
        Args :
            request : dict
        return : dict (request data created by adding source add)
        '''
        # Checking source text language
        response = await DetectManager.detect_language(request)
        # if source language is not same as source text
        if 'source_language' in request and request['source_language'].lower() != response['source_language'].lower():
            SanicException("Source text and Source Language does not match.", status_code=400)
        request = copy_data(request,response)
        return request
    
    @classmethod
    async def translate_text(cls,request):
        '''
        Translate the text 
        Args : 
            request : dict
        return : dict
        '''
        request = TranslatorRequest(**request)
        headers,params,data,our_response =  cls._build(request)
        response = await cls.async_api_call(headers,params,data)
        return dict(cls._build_response(our_response,response))

    @classmethod
    async def translate_validate(cls,request):
        '''
        Translate and validate
        Args :
            request : dict
        return : dict
        '''
        request = await cls.validate(request)
        return await cls.translate_text(request)
    
    @classmethod
    async def add_log(cls,text):
        '''
        Add the text in log file. 
        '''
        async with aiofiles.open(cls.file, mode='a') as f:
            await f.write(text+'/n')
    
class Google(Translator):
    success = 1
    failure = 1
    api_limit = 5000
    url = UrlEndPoints.GOOGLE_URL
    file = "google_log.txt"

    @classmethod
    def _build(cls,request):
        '''
        Build the parameter for Google API
        Args : TranslatorRequest
        Return : headers,params,data,response
        '''
        params = {
                "q": request.source_text,
                "target": get_code(request.target_language),
                "key": config.google_api_key}
        response = {"source_language" : request.source_language,
                         "source_text" : request.source_text,
                         "target_language" : request.target_language}
        return None,params,None,response

    @classmethod  
    def _build_response(self,our_response,response):
        '''
        Build for response
        Args : 
            response : dict
        Return : TranslatorResponse
        '''
        our_response['target_text'] =response['data']['translations'][0]['translatedText']
        return TranslatorResponse(**our_response)
    
    @classmethod
    async def file_translate(cls,request):
        
        input_file = request['input_file']
        input_text = await read_file_(input_file)

        chunks = split_text_into_chunks(input_text, cls.api_limit)
        our_data ={"source_language":request["source_language"],
               "target_language":request["target_language"]}
        tasks = []
        
        for chunk in chunks:
            our_data["source_text"] = chunk
            tasks.append(cls.translate_text(our_data))

        translated_chunks =  await asyncio.gather(*tasks,return_exceptions=True)
        translated_chunks = [chunk['target_text'] for chunk in translated_chunks]

        translated_text = " ".join(translated_chunks)

        output_language = request['target_language']
        output_file = input_file.split('.')[0] + '_' + output_language + '.' + input_file.split('.')[1]
        
        await write_file_(output_file,translated_text)
        return {"output_file":output_file}
    
class Rapid(Translator):
    success = 1
    failure = 1
    url = UrlEndPoints.RAPID_URL
    file = "rapid_log.txt"

    @classmethod
    def _build(cls,request):
        '''
        Build the parameter for Rapid API
        Args : 
            request: TranslatorRequest
        Return : headers,params,data,response
        '''
        data = {
            "source_language": get_code(request.source_language),
            "target_language": get_code(request.target_language),
            "text" : request.source_text
        }
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": config.rapid_api_key,
            "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
            }
        response = {"source_language" : request.source_language,
                         "source_text" : request.source_text,
                         "target_language" : request.target_language}
        return headers,None,data,response
    
    @classmethod
    def _build_response(cls,our_response,response):
        '''
        Build for response
        Args : 
            response : dict
        Return : TranslatorResponse
        '''
        our_response["target_text"] = response['data']['translatedText']
        return TranslatorResponse(**our_response)

class Lacto(Translator):
    success = 1
    failure = 1
    url = UrlEndPoints.LACTO_URL
    file = 'lacto_log.txt'

    @classmethod
    def _build(cls,request):
        '''
        Build the parameter for Rapid API
        Args : TranslatorRequest
        Return : headers,params,data,response
        '''
        headers = {
            'X-API-Key': config.lacto_api_key,
            'Content-Type': 'json',
            'Accept': 'json'}
        data = {'texts' : get_code(request.source_text),
                     "to" : get_code(request.target_language),
                    "from" : get_code(request.source_language)}
        response = {"source_language" : request.source_language,
                         "source_text" : request.source_text,
                         "target_language" : request.target_language}
        return headers,None,data,response
    
    @classmethod
    def _build_response(cls,our_response,response):
        '''
        Build for response
        Args : 
            response : dict
        Return : TranslatorResponse
        '''
        our_response["target_text"] = response['translations'][0]['translated'][0]
        return TranslatorResponse(**our_response)
    