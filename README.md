
## test service for https://heyling.net/
* * *
#### This solution used technologies such as:
* FastApi
* RabbitMQ
#### The task was:
* create broker queue via rabbitmq
* create service with one router
* add websocket router which gets msg from broker
* scripts for console IO

* * *

## Set Up the app

#### 1) Download the code
```
git clone https://github.com/Svogg/xakaton
```
#### 2) Run docker-compose
```
docker-compose up --build
```

#### 3) Open your browser at: 
```
http://localhost:8000/docs
```

#### 4) Run listen_results.py
```
python3 listen_results.py
```
#### 5) Run queue_reverse_text.py
```
python3 queue_reverse_text.py
```

* * *