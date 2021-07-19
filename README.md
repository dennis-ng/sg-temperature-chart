To start the app locally, run:
```
docker-compose up --build
```
To run the unit tests using pytest, run:
```
docker-compose build && docker-compose run web pytest
```

##### To start the task and get a url for the chart
```http
Method:   GET
Endpoint: /chart_link
Response: { "chart_url": str }
```
The chart_url from the above endpoint should lead you to the following endpoint:
##### To view the chart
```http
Method:   GET
Endpoint: /chart/{id}
```
##### If the chart is ready, it will return
```
Response: 200, HTML of a chart
```
##### If the chart is not ready, it will return
```
Response: 202, HTML Message to wait
```