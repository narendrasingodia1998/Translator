from pydantic import BaseModel

class TranslatorResponse(BaseModel):
    source_language : str
    source_text : str
    target_language : str
    target_text : str

class DetectResponse(BaseModel):
    source_text : str
    source_language : str
