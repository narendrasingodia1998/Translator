from sanic import Blueprint
from sanic.response import json
from app.model.request import TranslatorRequest
from app.manager.auto_select import AutoSelectManager
from app.manager.translator import Lacto,Rapid,Google
from sanic_ext import validate

trans_bp = Blueprint('translator', url_prefix='/translator')

@trans_bp.post('/')
@validate(json=TranslatorRequest)
async def auto(request,body:TranslatorRequest):
    '''
    For auto detect the server
    '''
    request = request.json
    response = await AutoSelectManager.findserver(request)
    return json(response)

@trans_bp.post('/google')
@validate(json=TranslatorRequest)
async def google(request,body:TranslatorRequest):
    request = request.json
    response = await Google.translate(request)
    return json(response)

@trans_bp.post('/lacto')
@validate(json=TranslatorRequest)
async def lacto(request,body:TranslatorRequest):
    request = request.json
    response = await Lacto.translate(request)
    return json(response)

@trans_bp.post('/rapid')
@validate(json=TranslatorRequest)
async def rapid(request,body:TranslatorRequest):
    request = request.json
    response = await Rapid.translate(request)
    return json(response)

@trans_bp.post('/file')
async def file(request):
    request = request.json
    response = await Google.file_translate(request)
    return json(response)
