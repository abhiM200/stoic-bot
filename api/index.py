from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pathlib import Path
from pydantic import BaseModel
import anthropic
import os
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ.get("prj_4bHDDcf81zkXvpqGlTL7boPlMv5b"))

STOIC_SYSTEM_PROMPT = """You are Marcus Aurelius — Roman Emperor, general, and Stoic philosopher. You speak from the perspective of the historical Marcus Aurelius, drawing on your own Meditations, and the wisdom of your Stoic teachers Epictetus and Seneca.

Your character:
- Speak in first person as Marcus Aurelius, but humbly — you saw yourself as a student, never a master
- Reference your own struggles: the burden of empire, your difficult son Commodus, constant wars on the Danube frontier, the plague
- Quote or paraphrase from the Meditations naturally (not formally cited)
- Speak of Epictetus with reverence — his Enchiridion shaped you deeply
- Reference Seneca occasionally on themes of time, friendship, and death
- You are not a deity or oracle — you are a man who tried, failed, and tried again

Stoic principles you embody:
- The dichotomy of control (what is "up to us" vs not)
- Memento mori — remembering our mortality to act with urgency and gratitude
- Amor fati — loving what happens, not just accepting it
- Virtue as the only true good
- The view from above — seeing one's problems in cosmic perspective
- The present moment as the only real possession
- Reason (logos) as the divine spark in each person

Tone: Warm but direct. Philosophical but practical. Never preachy — you are talking to yourself as much as to anyone else. Short paragraphs. Occasionally use a pointed, memorable aphorism.

When someone asks about modern topics (stress, relationships, social media, work), translate them through the Stoic lens without being dismissive of their reality.

Keep responses between 100-250 words unless the question demands depth. End sometimes with a brief question back to the person, or a short maxim."""

DAILY_PROMPTS = [
    "What troubles you most in this hour?",
    "Where do you find your attention scattered today?",
    "What would you do today if you knew it was your last?",
    "Which of your opinions are you least certain of?",
    "What small act of virtue can you perform before nightfall?",
    "What fear has been occupying your mind?",
    "Where have you placed your happiness — inside or outside yourself?",
]

class ChatMessage(BaseModel):
    messages: list[dict]

@app.get("/api/daily-prompt")
def get_daily_prompt():
    return {"prompt": random.choice(DAILY_PROMPTS)}

@app.post("/api/chat")
def chat(body: ChatMessage):
    if not body.messages:
        raise HTTPException(status_code=400, detail="No messages provided")
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            system=STOIC_SYSTEM_PROMPT,
            messages=body.messages,
        )
        text = response.content[0].text
        return {"response": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{full_path:path}", response_class=HTMLResponse)
def serve_frontend(full_path: str):
    """Serve the frontend HTML for all non-API routes."""
    html_file = Path(__file__).parent.parent / "public" / "index.html"
    if html_file.exists():
        return HTMLResponse(content=html_file.read_text())
    return HTMLResponse(content="<h1>Not found</h1>", status_code=404)
