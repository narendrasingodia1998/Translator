from sanic import Sanic

from app.routes.detect_routes import detect_bp
from app.routes.translate_routes import trans_bp


app = Sanic('Translator')

app.blueprint(detect_bp)
app.blueprint(trans_bp)

if __name__ == '__main__':
    app.run(auto_reload=True)

##TODO
## Error handling of language detector
## Error handling in Client api call
## Error handling in Translator
## Add listener such that it check all three api if they did not responed it doesnot start
## Add listener which send call google api to get avialable language the language 
## Use get command
## Use 
