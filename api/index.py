from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
- The dichotomy of control (what is up to us vs not)
- Memento mori — remembering our mortality to act with urgency and gratitude
- Amor fati — loving what happens, not just accepting it
- Virtue as the only true good
- The view from above — seeing problems in cosmic perspective
- The present moment as the only real possession
- Reason (logos) as the divine spark in each person

Tone: Warm but direct. Philosophical but practical. Never preachy. Short paragraphs. Occasionally use a pointed, memorable aphorism.

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

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Marcus — A Stoic Oracle</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Pro:ital,wght@0,300;0,400;1,300;1,400&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #0d0b08;
      --bg2: #13110d;
      --bg3: #1c1812;
      --gold: #c9a84c;
      --gold2: #e8c96e;
      --gold-dim: #8a6d2a;
      --text: #e8e0d0;
      --text-muted: #8a7d68;
      --text-dim: #5a5040;
      --border: #2a2318;
      --border2: #3a3020;
      --marble: #1a1610;
      --user-bg: #1e1a14;
      --marcus-bg: #141210;
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      height: 100%;
      background: var(--bg);
      color: var(--text);
      font-family: 'Crimson Pro', Georgia, serif;
      font-size: 18px;
      line-height: 1.7;
      overflow: hidden;
    }

    /* Subtle grain overlay */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
      pointer-events: none;
      z-index: 1000;
      opacity: 0.6;
    }

    .layout {
      display: grid;
      grid-template-columns: 280px 1fr;
      height: 100vh;
      max-width: 1400px;
      margin: 0 auto;
    }

    /* ── SIDEBAR ── */
    .sidebar {
      border-right: 1px solid var(--border2);
      display: flex;
      flex-direction: column;
      padding: 0;
      background: var(--bg2);
      position: relative;
      overflow: hidden;
    }

    .sidebar::after {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse at 50% 0%, rgba(201,168,76,0.06) 0%, transparent 60%);
      pointer-events: none;
    }

    .sidebar-header {
      padding: 40px 28px 32px;
      border-bottom: 1px solid var(--border);
    }

    .logo-mark {
      width: 48px;
      height: 48px;
      margin-bottom: 20px;
    }

    .logo-mark circle {
      fill: none;
      stroke: var(--gold-dim);
      stroke-width: 1;
    }

    .logo-mark path {
      fill: none;
      stroke: var(--gold);
      stroke-width: 1.5;
      stroke-linecap: round;
    }

    .sidebar-title {
      font-family: 'Cinzel', serif;
      font-size: 22px;
      font-weight: 600;
      color: var(--gold2);
      letter-spacing: 0.08em;
      line-height: 1.2;
    }

    .sidebar-sub {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 6px;
      letter-spacing: 0.04em;
      font-style: italic;
    }

    .sidebar-section {
      padding: 28px 28px 0;
    }

    .sidebar-label {
      font-family: 'Cinzel', serif;
      font-size: 9px;
      letter-spacing: 0.2em;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 16px;
    }

    .principle {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 14px;
      opacity: 0.75;
      transition: opacity 0.2s;
    }

    .principle:hover { opacity: 1; }

    .principle-dot {
      width: 5px;
      height: 5px;
      border-radius: 50%;
      background: var(--gold-dim);
      margin-top: 9px;
      flex-shrink: 0;
    }

    .principle-text {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    .sidebar-quote {
      margin: auto 0 0;
      padding: 28px;
      border-top: 1px solid var(--border);
    }

    .sidebar-quote blockquote {
      font-size: 13.5px;
      font-style: italic;
      color: var(--text-muted);
      line-height: 1.7;
      position: relative;
      padding-left: 16px;
    }

    .sidebar-quote blockquote::before {
      content: '';
      position: absolute;
      left: 0;
      top: 4px;
      bottom: 4px;
      width: 1px;
      background: var(--gold-dim);
    }

    .sidebar-quote cite {
      display: block;
      font-size: 11px;
      color: var(--text-dim);
      margin-top: 10px;
      font-style: normal;
      letter-spacing: 0.06em;
    }

    /* ── MAIN CHAT ── */
    .main {
      display: flex;
      flex-direction: column;
      height: 100vh;
      overflow: hidden;
    }

    .chat-header {
      padding: 24px 40px;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      background: var(--bg);
    }

    .chat-header-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: 1px solid var(--gold-dim);
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--bg3);
      font-family: 'Cinzel', serif;
      font-size: 15px;
      color: var(--gold);
      flex-shrink: 0;
    }

    .chat-persona {
      font-family: 'Cinzel', serif;
      font-size: 15px;
      color: var(--text);
      font-weight: 600;
    }

    .chat-persona-sub {
      font-size: 12px;
      color: var(--text-muted);
      font-style: italic;
    }

    .status-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #4a7c59;
      animation: pulse 2.5s ease-in-out infinite;
      margin-left: auto;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }

    .btn-new {
      font-family: 'Cinzel', serif;
      font-size: 10px;
      letter-spacing: 0.15em;
      color: var(--text-dim);
      border: 1px solid var(--border2);
      background: none;
      padding: 8px 16px;
      cursor: pointer;
      transition: all 0.2s;
      text-transform: uppercase;
    }

    .btn-new:hover {
      color: var(--gold);
      border-color: var(--gold-dim);
    }

    /* ── MESSAGES ── */
    .messages {
      flex: 1;
      overflow-y: auto;
      padding: 0;
      scroll-behavior: smooth;
    }

    .messages::-webkit-scrollbar { width: 3px; }
    .messages::-webkit-scrollbar-track { background: transparent; }
    .messages::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

    /* Empty state */
    .empty-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      padding: 40px;
      text-align: center;
      animation: fadeIn 0.8s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .empty-medallion {
      width: 80px;
      height: 80px;
      margin-bottom: 32px;
      opacity: 0.6;
    }

    .empty-title {
      font-family: 'Cinzel', serif;
      font-size: 20px;
      color: var(--text);
      font-weight: 600;
      margin-bottom: 10px;
    }

    .empty-sub {
      font-size: 15px;
      color: var(--text-muted);
      font-style: italic;
      max-width: 420px;
      margin-bottom: 40px;
      line-height: 1.8;
    }

    .daily-prompt-card {
      background: var(--bg3);
      border: 1px solid var(--border2);
      padding: 24px 32px;
      max-width: 480px;
      width: 100%;
      position: relative;
      cursor: pointer;
      transition: border-color 0.25s;
    }

    .daily-prompt-card::before {
      content: 'Today\'s Reflection';
      position: absolute;
      top: -10px;
      left: 24px;
      font-family: 'Cinzel', serif;
      font-size: 9px;
      letter-spacing: 0.2em;
      color: var(--gold-dim);
      background: var(--bg3);
      padding: 0 8px;
      text-transform: uppercase;
    }

    .daily-prompt-card:hover { border-color: var(--gold-dim); }

    .daily-prompt-text {
      font-size: 17px;
      font-style: italic;
      color: var(--text);
      line-height: 1.7;
    }

    .daily-prompt-cta {
      font-size: 12px;
      color: var(--text-dim);
      margin-top: 14px;
      letter-spacing: 0.05em;
    }

    .starter-prompts {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 28px;
      justify-content: center;
      max-width: 560px;
    }

    .starter-btn {
      font-family: 'Crimson Pro', serif;
      font-size: 14px;
      font-style: italic;
      color: var(--text-muted);
      border: 1px solid var(--border2);
      background: none;
      padding: 8px 18px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .starter-btn:hover {
      color: var(--gold2);
      border-color: var(--gold-dim);
      background: rgba(201,168,76,0.04);
    }

    /* Messages */
    .message {
      padding: 28px 40px;
      display: flex;
      gap: 18px;
      align-items: flex-start;
      border-bottom: 1px solid var(--border);
      animation: msgIn 0.35s ease;
    }

    @keyframes msgIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .message.user {
      background: var(--user-bg);
      flex-direction: row-reverse;
    }

    .message.marcus {
      background: var(--marcus-bg);
    }

    .msg-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: 'Cinzel', serif;
      font-size: 13px;
    }

    .message.marcus .msg-avatar {
      border: 1px solid var(--gold-dim);
      color: var(--gold);
      background: var(--bg3);
    }

    .message.user .msg-avatar {
      border: 1px solid var(--border2);
      color: var(--text-muted);
      background: var(--bg2);
      font-family: 'Crimson Pro', serif;
      font-size: 15px;
    }

    .msg-body {
      flex: 1;
      max-width: 680px;
    }

    .message.user .msg-body {
      text-align: right;
    }

    .msg-name {
      font-family: 'Cinzel', serif;
      font-size: 10px;
      letter-spacing: 0.15em;
      color: var(--text-dim);
      text-transform: uppercase;
      margin-bottom: 8px;
    }

    .msg-text {
      font-size: 17px;
      line-height: 1.8;
      color: var(--text);
    }

    .message.user .msg-text {
      color: #c8bfae;
    }

    .msg-text p + p { margin-top: 12px; }

    /* Typing indicator */
    .typing-indicator {
      display: flex;
      gap: 5px;
      align-items: center;
      padding: 6px 0;
    }

    .typing-indicator span {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--gold-dim);
      animation: typing 1.2s ease-in-out infinite;
    }

    .typing-indicator span:nth-child(2) { animation-delay: 0.15s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.3s; }

    @keyframes typing {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
      30% { transform: translateY(-6px); opacity: 1; }
    }

    /* ── INPUT AREA ── */
    .input-area {
      padding: 20px 40px 28px;
      border-top: 1px solid var(--border);
      flex-shrink: 0;
      background: var(--bg);
    }

    .input-wrap {
      display: flex;
      align-items: flex-end;
      gap: 14px;
      border: 1px solid var(--border2);
      padding: 14px 18px;
      background: var(--bg3);
      transition: border-color 0.2s;
      position: relative;
    }

    .input-wrap:focus-within {
      border-color: var(--gold-dim);
    }

    .input-wrap::before {
      content: '';
      position: absolute;
      inset: -1px;
      background: linear-gradient(135deg, rgba(201,168,76,0.1), transparent, rgba(201,168,76,0.05));
      opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
    }

    .input-wrap:focus-within::before { opacity: 1; }

    #msgInput {
      flex: 1;
      background: none;
      border: none;
      outline: none;
      color: var(--text);
      font-family: 'Crimson Pro', serif;
      font-size: 17px;
      line-height: 1.5;
      resize: none;
      max-height: 160px;
      min-height: 28px;
    }

    #msgInput::placeholder {
      color: var(--text-dim);
      font-style: italic;
    }

    .send-btn {
      width: 38px;
      height: 38px;
      background: var(--gold-dim);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: all 0.2s;
      color: var(--bg);
    }

    .send-btn:hover:not(:disabled) {
      background: var(--gold);
    }

    .send-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    .send-btn svg {
      width: 16px;
      height: 16px;
    }

    .input-footer {
      margin-top: 10px;
      font-size: 12px;
      color: var(--text-dim);
      text-align: center;
      font-style: italic;
    }

    /* Error state */
    .error-msg {
      padding: 16px 40px;
      font-size: 14px;
      color: #8a4a3a;
      font-style: italic;
      border-bottom: 1px solid var(--border);
      background: rgba(138,74,58,0.05);
    }

    /* Divider */
    .time-divider {
      text-align: center;
      padding: 16px 40px;
      font-size: 11px;
      color: var(--text-dim);
      letter-spacing: 0.1em;
      font-style: italic;
    }

    /* ── RESPONSIVE ── */
    @media (max-width: 768px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { display: none; }
      .message, .input-area, .chat-header { padding-left: 20px; padding-right: 20px; }
      .empty-state { padding: 24px 20px; }
    }
  </style>
</head>
<body>
<div class="layout">

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-header">
      <svg class="logo-mark" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="22"/>
        <path d="M24 8 L24 40 M12 16 L36 16 M10 24 L38 24 M14 32 L34 32"/>
        <path d="M24 6 L28 14 L24 12 L20 14 Z" style="fill:var(--gold-dim);stroke:none"/>
      </svg>
      <div class="sidebar-title">MARCUS</div>
      <div class="sidebar-sub">Stoic philosopher · Roman Emperor · 161–180 AD</div>
    </div>

    <div class="sidebar-section">
      <div class="sidebar-label">Pillars of Stoicism</div>

      <div class="principle">
        <div class="principle-dot"></div>
        <div class="principle-text">The Dichotomy of Control — distinguish what is yours to change</div>
      </div>
      <div class="principle">
        <div class="principle-dot"></div>
        <div class="principle-text">Memento Mori — hold death in mind to live fully</div>
      </div>
      <div class="principle">
        <div class="principle-dot"></div>
        <div class="principle-text">Amor Fati — love what happens, not merely endure it</div>
      </div>
      <div class="principle">
        <div class="principle-dot"></div>
        <div class="principle-text">Virtue as the highest good — all else is preferred indifferent</div>
      </div>
      <div class="principle">
        <div class="principle-dot"></div>
        <div class="principle-text">The View from Above — see your troubles in cosmic perspective</div>
      </div>
    </div>

    <div class="sidebar-quote">
      <blockquote id="sidebarQuote">
        You have power over your mind, not outside events. Realize this, and you will find strength.
      </blockquote>
      <cite>— Meditations, Marcus Aurelius</cite>
    </div>
  </aside>

  <!-- Main Chat -->
  <main class="main">
    <header class="chat-header">
      <div class="chat-header-left">
        <div class="avatar">M</div>
        <div>
          <div class="chat-persona">Marcus Aurelius</div>
          <div class="chat-persona-sub">Emperor · Philosopher · Reluctant ruler</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:16px;">
        <div class="status-dot"></div>
        <button class="btn-new" onclick="newConversation()">New Dialogue</button>
      </div>
    </header>

    <div class="messages" id="messages">
      <div class="empty-state" id="emptyState">
        <svg class="empty-medallion" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="40" r="38" fill="none" stroke="#3a3020" stroke-width="1"/>
          <circle cx="40" cy="40" r="30" fill="none" stroke="#c9a84c" stroke-width="0.75" stroke-dasharray="3,4"/>
          <text x="40" y="45" text-anchor="middle" font-family="Cinzel, serif" font-size="18" fill="#c9a84c" opacity="0.8">M</text>
          <circle cx="40" cy="40" r="22" fill="none" stroke="#8a6d2a" stroke-width="0.5"/>
        </svg>
        <div class="empty-title">Seek counsel from the Meditations</div>
        <div class="empty-sub">
          Ask Marcus about Stoic philosophy, how to handle adversity, find purpose, or simply how to live a good life.
        </div>

        <div class="daily-prompt-card" id="dailyPromptCard" onclick="useDailyPrompt()">
          <div class="daily-prompt-text" id="dailyPromptText">Loading today's reflection…</div>
          <div class="daily-prompt-cta">Click to begin with this prompt →</div>
        </div>

        <div class="starter-prompts">
          <button class="starter-btn" onclick="useStarter(this)">How do I stop worrying?</button>
          <button class="starter-btn" onclick="useStarter(this)">What is a good life?</button>
          <button class="starter-btn" onclick="useStarter(this)">On dealing with anger</button>
          <button class="starter-btn" onclick="useStarter(this)">How to face death?</button>
          <button class="starter-btn" onclick="useStarter(this)">I feel like a failure</button>
          <button class="starter-btn" onclick="useStarter(this)">The nature of time</button>
        </div>
      </div>
    </div>

    <div class="input-area">
      <div class="input-wrap">
        <textarea
          id="msgInput"
          rows="1"
          placeholder="Ask Marcus anything…"
          onkeydown="handleKey(event)"
          oninput="autoResize(this)"
        ></textarea>
        <button class="send-btn" id="sendBtn" onclick="sendMessage()" disabled>
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14 8L2 2l2.5 6L2 14l12-6z" fill="currentColor"/>
          </svg>
        </button>
      </div>
      <div class="input-footer">Meditations, Book II — "Waste no more time arguing what a good man should be. Be one."</div>
    </div>
  </main>
</div>

<script>
  // ── State ──
  let conversationHistory = [];
  let isLoading = false;
  let dailyPrompt = '';

  const SIDEBAR_QUOTES = [
    { text: "The impediment to action advances action. What stands in the way becomes the way.", cite: "Meditations V.20" },
    { text: "Never esteem anything as of advantage to you that will make you break your word or lose your self-respect.", cite: "Meditations III.7" },
    { text: "Our life is what our thoughts make it.", cite: "Meditations IV.3" },
    { text: "Do not indulge in dreams of what you have failed to accomplish.", cite: "Meditations IV.4" },
  ];

  // ── Init ──
  (async function init() {
    // Rotate sidebar quote
    const q = SIDEBAR_QUOTES[Math.floor(Math.random() * SIDEBAR_QUOTES.length)];
    document.getElementById('sidebarQuote').textContent = q.text;
    document.querySelector('.sidebar-quote cite').textContent = `— ${q.cite}`;

    // Fetch daily prompt
    try {
      const res = await fetch('/api/daily-prompt');
      const data = await res.json();
      dailyPrompt = data.prompt;
      document.getElementById('dailyPromptText').textContent = `"${dailyPrompt}"`;
    } catch {
      dailyPrompt = 'What troubles you most in this moment?';
      document.getElementById('dailyPromptText').textContent = `"${dailyPrompt}"`;
    }
  })();

  // ── Input handling ──
  const input = document.getElementById('msgInput');
  const sendBtn = document.getElementById('sendBtn');

  input.addEventListener('input', () => {
    sendBtn.disabled = input.value.trim() === '' || isLoading;
  });

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 160) + 'px';
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!sendBtn.disabled) sendMessage();
    }
  }

  function useDailyPrompt() {
    input.value = dailyPrompt;
    autoResize(input);
    sendBtn.disabled = false;
    input.focus();
    sendMessage();
  }

  function useStarter(btn) {
    input.value = btn.textContent;
    autoResize(input);
    sendBtn.disabled = false;
    sendMessage();
  }

  function newConversation() {
    conversationHistory = [];
    const messages = document.getElementById('messages');
    messages.innerHTML = `
      <div class="empty-state" id="emptyState">
        <svg class="empty-medallion" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
          <circle cx="40" cy="40" r="38" fill="none" stroke="#3a3020" stroke-width="1"/>
          <circle cx="40" cy="40" r="30" fill="none" stroke="#c9a84c" stroke-width="0.75" stroke-dasharray="3,4"/>
          <text x="40" y="45" text-anchor="middle" font-family="Cinzel, serif" font-size="18" fill="#c9a84c" opacity="0.8">M</text>
          <circle cx="40" cy="40" r="22" fill="none" stroke="#8a6d2a" stroke-width="0.5"/>
        </svg>
        <div class="empty-title">Seek counsel from the Meditations</div>
        <div class="empty-sub">Ask Marcus about Stoic philosophy, how to handle adversity, find purpose, or simply how to live a good life.</div>
        <div class="daily-prompt-card" onclick="useDailyPrompt()">
          <div class="daily-prompt-text">"${dailyPrompt}"</div>
          <div class="daily-prompt-cta">Click to begin with this prompt →</div>
        </div>
        <div class="starter-prompts">
          <button class="starter-btn" onclick="useStarter(this)">How do I stop worrying?</button>
          <button class="starter-btn" onclick="useStarter(this)">What is a good life?</button>
          <button class="starter-btn" onclick="useStarter(this)">On dealing with anger</button>
          <button class="starter-btn" onclick="useStarter(this)">How to face death?</button>
          <button class="starter-btn" onclick="useStarter(this)">I feel like a failure</button>
          <button class="starter-btn" onclick="useStarter(this)">The nature of time</button>
        </div>
      </div>
    `;
    input.value = '';
    autoResize(input);
    sendBtn.disabled = true;
  }

  // ── Rendering ──
  function hideEmpty() {
    const e = document.getElementById('emptyState');
    if (e) e.remove();
  }

  function appendMessage(role, text) {
    hideEmpty();
    const messages = document.getElementById('messages');

    const div = document.createElement('div');
    div.className = `message ${role}`;

    const avatarTxt = role === 'marcus' ? 'M' : '✦';
    const nameLabel = role === 'marcus' ? 'Marcus Aurelius' : 'You';

    // Convert line breaks to paragraphs
    const formatted = text.split('\n').filter(l => l.trim()).map(l => `<p>${l}</p>`).join('');

    div.innerHTML = `
      <div class="msg-avatar">${avatarTxt}</div>
      <div class="msg-body">
        <div class="msg-name">${nameLabel}</div>
        <div class="msg-text">${formatted}</div>
      </div>
    `;

    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
  }

  function showTyping() {
    hideEmpty();
    const messages = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'message marcus';
    div.id = 'typingIndicator';
    div.innerHTML = `
      <div class="msg-avatar">M</div>
      <div class="msg-body">
        <div class="msg-name">Marcus Aurelius</div>
        <div class="typing-indicator"><span></span><span></span><span></span></div>
      </div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById('typingIndicator');
    if (t) t.remove();
  }

  function showError(msg) {
    const messages = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'error-msg';
    div.textContent = `⚠ ${msg}`;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // ── Send ──
  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isLoading) return;

    isLoading = true;
    sendBtn.disabled = true;
    input.value = '';
    autoResize(input);
    input.style.height = '';

    // Add to history & render
    conversationHistory.push({ role: 'user', content: text });
    appendMessage('user', text);
    showTyping();

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: conversationHistory }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'The oracle is silent. Try again shortly.');
      }

      const data = await res.json();
      removeTyping();

      conversationHistory.push({ role: 'assistant', content: data.response });
      appendMessage('marcus', data.response);

    } catch (err) {
      removeTyping();
      showError(err.message || 'Something went wrong. Even Marcus faced setbacks.');
    } finally {
      isLoading = false;
      sendBtn.disabled = input.value.trim() === '';
    }
  }
</script>
</body>
</html>
'''

@app.get("/{full_path:path}", response_class=HTMLResponse)
def serve_frontend(full_path: str):
    return HTMLResponse(content=HTML_CONTENT)
