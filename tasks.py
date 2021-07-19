from celery import Celery
import asyncio
import os
from models import temperature

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
app = Celery('tasks', broker=broker_url, backend=result_backend)

WEATHER_ENDPOINT = 'https://api.data.gov.sg/v1/environment/air-temperature'

@app.task
def get_weather() -> str:
    data = asyncio.run(temperature.get_past_week_data())
    html_chart = temperature.plot(data)
    # Save to S3 and return the s3 url if you intend to keep it much longer.
    # However it doesn't really make sense and in fact we can just return
    # a cached chart using the truncated datetime of the request up to the
    # minute as the key instead of generating a new one, since the data
    # is not actually dynamic.
    return html_chart