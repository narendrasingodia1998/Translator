import time
from sanic.log import logger

def time_decorator(func):
    async def inner1(*args, **kwargs):
        st = time.ctime() 
        logger.info(f"Start time : {st}")
        returned_value = await func(*args, **kwargs)
        et = time.ctime()
        logger.info(f"End Time : {et}")
        return returned_value
         
    return inner1