# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import run_agent

app = FastAPI(title="ColumbusAI Agent API", version="1.0")

# Allow calls from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_methods=["*"],
    allow_headers=["*"]
)

class Prompt(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "ok", "message": "LangChain Agent API ready 🚀"}

@app.post("/chat")
def chat(prompt: Prompt):
    """Call the persistent agent."""
    response = run_agent(prompt.query)
    return {"response": response}
