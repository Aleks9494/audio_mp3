import uvicorn
from fastapi import FastAPI
from app import routers

app = FastAPI()
app.include_router(routers.router)


if __name__ == '__main__':
    log_config = 'logging.conf'
    uvicorn.run(
        'main:app', host='0.0.0.0', port=8010, reload=True, debug=True, log_config=log_config
    )