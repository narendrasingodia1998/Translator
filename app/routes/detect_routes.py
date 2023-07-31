from sanic import Blueprint
from app.manager.language_detect import DetectManager
from app.model.request import DetectRequest
from sanic.response import json
from sanic_ext import validate

detect_bp = Blueprint('detect', url_prefix='/detect')

@detect_bp.post('/')
@validate(json=DetectRequest)
async def detect(request,body:DetectRequest):
    request = request.json
    response = await DetectManager.detect_language(request)
    return  json(response)