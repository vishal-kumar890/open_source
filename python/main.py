from fastapi import FastAPI
from .views import solveApi
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

# origins = [
#     settings.client_url,
# ]

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://127.0.0.1',
    'http://127.0.0.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"], 
    allow_credentials=True,
    allow_headers=["*"],    
)



app.include_router(solveApi.router, tags=["solve"])

