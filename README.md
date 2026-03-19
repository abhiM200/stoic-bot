# Marcus — A Stoic Oracle Chatbot

A purpose-built chatbot that lets you converse with **Marcus Aurelius**, Roman Emperor and Stoic philosopher. Ask about Stoicism, how to handle adversity, find purpose, or simply how to live well.

## Why This Topic?

Stoic philosophy is one of the most _practical_ philosophical traditions — it's not abstract theory but a daily practice for handling anxiety, loss, anger, and uncertainty. Marcus Aurelius wrote the *Meditations* not for publication but as personal notes to himself, making him uniquely conversational as a persona.

The subject has a defined, rich knowledge base (Meditations, Enchiridion, Letters to Lucilius) that gives the chatbot a clear voice and deep context — it's not a generic wrapper, it _is_ Marcus.

## What I Built

- **Backend**: FastAPI (Python) with an Anthropic API integration
- **Frontend**: Custom HTML/CSS/JS with no framework — dark editorial aesthetic with Cinzel serif typography, gold accents, and grain textures
- **Persona**: A carefully engineered system prompt that channels Marcus Aurelius's voice, references his historical context (Danube wars, the plague, Commodus), and draws on all three major Stoic texts

## UX Decisions

- **Empty state** loads a randomized "daily reflection prompt" from the API — gives first-time users immediate direction
- **Starter prompts** cover common entry points ("How do I stop worrying?", "On dealing with anger") — reduces blank-page anxiety
- **Typing indicator** uses a subtle animated dots pattern in gold — communicates loading without feeling generic
- **Sidebar** shows the five pillars of Stoicism and a rotating Meditations quote — contextual education without interrupting flow
- **Error states** have character — "The oracle is silent" rather than generic "500 error"

## Stack

- Python 3.11 + FastAPI
- Anthropic `claude-sonnet-4-20250514` model
- Vanilla HTML/CSS/JS (no build step needed)
- Deployed on Vercel

## Local Development

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
cd api && uvicorn index:app --reload --port 8000
```

Then open `http://localhost:8000`

## Deploying to Vercel

1. Push to GitHub
2. Import repo in Vercel
3. Set environment variable: `ANTHROPIC_API_KEY`
4. Deploy — Vercel auto-detects Python via `vercel.json`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
