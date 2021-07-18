from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from tasks import get_weather
from celery.result import AsyncResult

app = FastAPI()

@app.get('/')
def home():
    return 'Use GET /chart_link.'

@app.get('/chart_link', status_code=201)
async def generate_chart(request: Request):
    task = get_weather.delay()
    chart_url = request.url_for('get_chart', **{'id': task.id})
    return {
        'chart_url': chart_url
    }


@app.get("/chart/{id}", status_code=200, response_class=HTMLResponse)
def get_chart(id: str, response: Response):
    result = AsyncResult(id)
    if result.ready():
        return result.get()
    else:
        response.status_code = 202
        return "Oops! We are still drawing your chart. Please" + \
            " come back in a minute."
