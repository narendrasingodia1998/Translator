import asyncio
import aiohttp
from sanic.exceptions import NotFound, BadRequest
from aiohttp_client_cache import CachedSession, SQLiteBackend

class Client:
    # def __init__(self) -> None:
    #     self.url = None
    #     self.params  = None
    #     self.headers = None
    #     self.data = None
    
    @classmethod
    async def async_api_call(cls,headers,params,data):
        '''
        Make the async api call
        return : dict
        '''
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with CachedSession(cache=SQLiteBackend('cache/demo_cache',allowed_methods=('GET', 'POST')),allowable_methods = ['GET','POST']) as session:
                async with session.post(cls.url,headers=headers,
                                        params=params,data=data,timeout=timeout) as response:
                        if response.status == 400:
                             cls.failure += 1
                             raise BadRequest()
                        elif response.status == 404:
                             cls.failure += 1
                             raise NotFound()             
                        response = await response.json()
                        cls.success += 1
                        return response
        except asyncio.TimeoutError:
             cls.failure += 1
             pass
        
    
    def _build(self,request):
         pass
    
    def _build_response(self,response):
         pass   
