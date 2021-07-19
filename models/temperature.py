import pandas as pd
import io
import plotly.express as px
from datetime import datetime, date, timedelta
import asyncio
import httpx
from httpx import Timeout
from typing import List, Dict
from pydantic import BaseModel

WEATHER_ENDPOINT = 'https://api.data.gov.sg/v1/environment/air-temperature'

class TemperatureStation(BaseModel):
    id: str
    name: str

class TemperatureMetaData(BaseModel):
    stations: List[TemperatureStation]

class Reading(BaseModel):
    station_id: str
    value: float

class Item(BaseModel):
    timestamp: datetime
    readings: List[Reading]

class DailyTemperatureData(BaseModel):
    metadata: TemperatureMetaData
    items: List[Item]

class ListOfDailyTemperature(BaseModel):
    data: List[DailyTemperatureData]

async def get_day_weather(day: datetime.date) -> Dict:
    async with httpx.AsyncClient() as client:
        resp = await client.get(WEATHER_ENDPOINT, params={'date': day}, timeout=Timeout(timeout=15.0))
    return resp.json()

async def get_past_week_data() -> List[Dict]:
    today = date.today()
    days = (today - timedelta(days=i) for i in reversed(range(7)))
    task_list = (get_day_weather(day) for day in days)
    data = await asyncio.gather(*task_list)
    return data

def plot(data: List[Dict]) -> str:
    dfs = []
    ListOfDailyTemperature(data=data) # Raises ValidationError
    for daily in data:
        df = pd.DataFrame(daily['items'])
        metadata = pd.DataFrame(daily['metadata']['stations'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.explode('readings').reset_index(drop=True)
        readings = pd.DataFrame(df['readings'].tolist())
        df = pd.concat((df, readings), axis=1)
        df = pd.merge(df, metadata[['id', 'name']], left_on='station_id', right_on='id')
        dfs.append(df)
    df = pd.concat(dfs)
    with io.StringIO() as buffer:
        fig = px.line(df, x="timestamp", y="value", color='name')
        fig.write_html(buffer,include_plotlyjs='cdn', config={'scrollZoom': True})
        html_chart = buffer.getvalue()
    return html_chart