from app.manager.client import Client
from app.model.response import DetectResponse
from app.model.request import DetectRequest
from app.utils.constants import UrlEndPoints
from app.utils.helper import get_language
from app.Config import config 
from sanic.log import logger

class DetectManager(Client):
    success = 1
    failure = 1
    url = UrlEndPoints.GOOGLE_URL + '/detect'

    @classmethod
    def _build(cls,request):
        '''
        Build the parameter for Language detector for google
        Args : DetectRequest
        Return : headers,params,data,response
        '''
        params = {
            "q": request.source_text,
            "key": config.google_api_key,
            }
        response = {"source_text":request.source_text}
        return None,params,None,response

    @classmethod   
    def _build_response(cls,our_response,response):
        '''
        Build for response
        Args : 
            response : dict
        Return : DetectReponse
        '''
        our_response['source_language'] = get_language(response.get('data').get('detections')[0][0].get('language'))   
        return DetectResponse(**our_response)
    
    @classmethod
    async def detect_language(cls, request):
        '''
        Detect language 
        Args : 
            request : dict
        Return : dict
        '''
        request = DetectRequest(**request)
        headers,params,data,our_response = cls._build(request)
        response = await cls.async_api_call(headers,params,data)
        return dict(cls._build_response(our_response,response))
    
## TODO 
##  Add exception handling

        