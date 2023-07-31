from typing import Optional
from pydantic import BaseModel,validator
from sanic.exceptions import  BadRequest
from app.utils.lang_code import lang_code

class TranslatorRequest(BaseModel):
    source_language : Optional[str]
    source_text : str
    target_language : str

    @validator('source_language')
    def validate_source_language(cls,value,values,**kwargs):
        if value and value.lower().strip() not in set(lang_code.keys()):
            raise ValueError(f"API does not support {value} language as Source language .")
        return value
    
    @validator('target_language')
    def validate_target_language(cls,value,values,**kwargs):
        print(f'values = {values}')
        if value.lower().strip() not in set(lang_code.keys()):
            raise BadRequest(f"API does not support {value} language as Target language .")
        if 'source_language' in values and value.lower().strip() == values['source_language'].lower().strip():
            raise BadRequest("Target language cannot be the same as the source language.")
        return value
    
class DetectRequest(BaseModel):
    source_text : str

