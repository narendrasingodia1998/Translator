from app.manager.client import Client
from app.manager.language_detect import DetectManager
from app.utils.helper import copy_data
from app.model.request import TranslatorRequest
from app.utils.constants import UrlEndPoints
from app.model.response import TranslatorResponse
from app.utils.helper import get_code
from app.Config import config

class Translator(Client):
    @classmethod
    async def translate(cls,request):
         '''
         Translate the text
         Args:
            request : dict 
         Return : dict
         '''
         # Checking source text language
         response = await DetectManager.detect_language(request)
         # if source language is not same as source text
         if 'source_language' in request and request['source_language'].lower() != response['source_language'].lower():
              print("Rasie  Condition is satisified")
         request = copy_data(request,response)
         request = TranslatorRequest(**request)
         headers,params,data,our_response =  cls._build(request)
         response = await cls.async_api_call(headers,params,data)
         return dict(cls._build_response(our_response,response))
    
class Google(Translator):
    success = 1
    failure = 1
    api_limit = 5000
    url = UrlEndPoints.GOOGLE_URL

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
    
    def file_translate(self,request):
        '''
        Translate the File
         Args:
            request : dict 
         Return : dict
        '''
        # input_file = request['input_file']
        # try:
        #     with open(input_file,'r') as file:
        #        input_text = file.read() 
        # except:
        #     print("Raise")
        # chucks = split_text_into_chunks(input_text,self.api_call_limit)
        # translated_chucks = []
        # pass
    
class Rapid(Translator):
    success = 1
    failure = 1
    url = UrlEndPoints.RAPID_URL

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
    