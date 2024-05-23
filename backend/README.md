# Chatbot Backend

**IMPORTANT NOTE**: This implementation requieres a redis instance for session cache storage and a mongodb instance for final persistence of the data. Check the docker compose file in the root folder for an easy implementation.

# Weather AI Assistant

This is a FastAPI application that runs on Uvicorn at port 8000. It provides an AI-powered weather assistant that can answer questions and provide information about weather conditions.

## Prerequisites

- Tested in Python 3.10
- Docker (optional, for running the application in containers)

## Dependencies
```python
pydantic==2.3.0
pydantic-settings==2.0.3
redis==5.0.1
pymongo==4.5.0
langchain==0.1.13
langchain-community==0.0.29
langchain-core==0.1.34
langchain-openai==0.1.1
langchain-text-splitters==0.0.1
openai==1.14.3
uvicorn==0.23.2
pandas==2.1.0
fastapi==0.103.2
```
## Installation

Run `pip install -r requirements.txt`. It is recommended to use a virtual environment tool such as `venv` or `conda`.

## Env Variables

By security reasons and to avoid hardcoding secrets, the project is designed to take the environment variables availabe in your environment, thus, any env var needs to be defined with:

```cmd
export ENVAR=VALUE
```
### Env vars
```
- MONGO_HOST=mongodb
- MONGO_PORT=27017
- MONGO_DB=chatbot
- MONGO_USER=root
- MONGO_PASSWORD=secret
- MONGO_AUTH_DB=admin
- MONGO_SESSIONS_COLLECTION=sessions
- REDIS_HOST=redis
- REDIS_PORT=6379
- REDIS_DB=0
- REDIS_PASSWORD=""
- REDIS_EXPIRE=3600
- API_KEY=
- OPENAI_API_KEY=
```

**You can modify the script in `utils.settings` with `python_dotenv` to load env variables from a .env file**

```python
from dotenv import load_dotenv
load_dotenv()
```
## Running the chatbot

Start the Uvicorn server:

`uvicorn backend.app.main:app --reload`


## Usage
A Swagger UI is available as part of FastAPI implementation. Once running check `http://localhost:8000/docs#/` for a detailed explanation of the available endpoints and schemas.


## Folder Structure

```
.
├── app
│   ├── main.py
│   └── v1
│       ├── handlers
│       │   ├── sessions_handler_base.py
│       │   └── sessions_handler.py
│       ├── routers
│       │   └── sessions_router.py
│       └── v1.py
├── core
│   └── dtos
│       ├── base_dto.py
│       ├── messages_dto.py
│       └── sessions_dto.py
├── dockerfile
├── EDA.ipynb
├── README.md
├── requirements.txt
├── src
│   ├── agents
│   │   ├── agent_base.py
│   │   ├── agent_langchain.py
│   │   ├── __init__.py
│   │   ├── prompts.py
│   │   └── tools.py
│   ├── __init__.py
│   ├── session_repository
│   │   ├── sesion_repository_mongo.py
│   │   ├── session_repository_base.py
│   │   └── session_repository_redis.py
│   └── weather_api
│       ├── __init__.py
│       ├── open_weather_wrapper.py
│       └── weather_api_base.py
├── tree.txt
└── utils
    ├── custom_logger.py
    └── settings.py

11 directories, 27 files

```