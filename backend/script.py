from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from service.handle_data import handle_data
from models.Settings import Settings
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post('/req/handle-dialog')
def handle_dialog(data: dict):
    settings = Settings(**data['settings'])
    handle_data(settings, data['dialog'])
    return {'res': 'hi'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5200, reload=False)
