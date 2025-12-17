import React, {useEffect, useMemo, useRef, useState} from 'react';

// Minimal client-side Gemini call using fetch to the REST API.
// API key is read from process.env.DOCUSAURUS_GEMINI_API_KEY at build time.
// Docusaurus automatically exposes env variables prefixed with DOCUSAURUS_.
// Ensure DOCUSAURUS_GEMINI_API_KEY is set in .env before building/serving.

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatbotProps {
  maxMessages?: number; // anti-abuse limit per session
}

const SYS_PROMPT = `You are a documentation guide AI for a website about Humanoid Physical AI and Robotics.

ROLE

You act as a help assistant inside a documentation website.
Your job is to guide readers through the book and docs about Humanoid Physical AI.

STRICT SCOPE (VERY IMPORTANT)

You MUST:

Answer ONLY about:

- Humanoid robots
- Physical AI systems
- Sensors, actuators, perception, motion control
- AI cognition, control systems, hardware–software integration
- Concepts explained in this book / documentation

Guide users like a book assistant.
Explain concepts step-by-step.
Use simple language first, then technical details.

You MUST NOT:

- Answer unrelated questions (politics, religion, gossip, etc.)
- Act like a general chatbot
- Go outside the robotics / Physical AI domain

If a question is outside scope, you MUST reply with the following verbatim:
“I’m here to guide you through the Humanoid Physical AI documentation. Please ask a related question.”`;

const GEMINI_API_KEY = process.env.DOCUSAURUS_GEMINI_API_KEY;
const GEMINI_MODEL = 'gemini-1.5-flash'; // fast & free-tier friendly
const GEMINI_URL = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`;

function sanitize(input: string): string {
  // Very basic sanitization. We rely on React escaping; strip control chars + trim.
  return input.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '').trim();
}

function ChatMessage({msg}: {msg: Message}) {
  return (
    <div
      role="listitem"
      className={`chat-msg chat-msg--${msg.role}`}
      style={{
        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
        background: 'var(--bg)',
        border: '1px solid var(--border)',
        borderRadius: 10,
        padding: '8px 10px',
        maxWidth: '85%',
        boxShadow: '0 1px 0 rgba(16,24,40,0.02)'
      }}
    >
      <div style={{fontSize: 12, color: 'var(--text-muted)', marginBottom: 4}}>
        {msg.role === 'user' ? 'You' : msg.role === 'assistant' ? 'Assistant' : 'System'}
      </div>
      <div style={{whiteSpace: 'pre-wrap'}}>{msg.content}</div>
    </div>
  );
}

export default function Chatbot({maxMessages = 15}: ChatbotProps) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {id: 'sys', role: 'system', content: SYS_PROMPT},
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bodyRef = useRef<HTMLDivElement>(null);

  const canSend = useMemo(() => {
    if (loading) return false;
    const userMsgs = messages.filter(m => m.role === 'user').length;
    return userMsgs < maxMessages && sanitize(input).length > 0;
  }, [input, loading, messages, maxMessages]);

  useEffect(() => {
    // Scroll to bottom on new messages
    bodyRef.current?.scrollTo({top: bodyRef.current.scrollHeight, behavior: 'smooth'});
  }, [messages, open]);

  async function generateAnswer(history: Message[]): Promise<string> {
    // Construct Gemini prompt: Use last N messages, include system as preface
    // Gemini generateContent schema
    const userVisibleHistory = history.filter(m => m.role !== 'system');

    const contents = [
      // System prompt as the first turn
      {role: 'user', parts: [{text: history.find(m => m.role === 'system')?.content || SYS_PROMPT}]},
      // Then alternate user/assistant turns
      ...userVisibleHistory.map(m => ({
        role: m.role === 'user' ? 'user' : 'model',
        parts: [{text: m.content}],
      })),
    ];

    const body = { contents, generationConfig: { temperature: 0.3, maxOutputTokens: 1024 } };

    const res = await fetch(GEMINI_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    if (res.status === 429) {
      throw new Error('Rate limit reached. Please wait a moment and try again.');
    }

    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`Gemini error: ${res.status} ${txt}`);
    }

    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.[0]?.text ?? '';
    return text || 'I could not generate a response right now.';
  }

  async function onSend(e?: React.FormEvent) {
    e?.preventDefault();
    setError(null);
    const userText = sanitize(input);
    if (!userText) return;

    const userMsgs = messages.filter(m => m.role === 'user').length;
    if (userMsgs >= maxMessages) {
      setError('Message limit reached for this session.');
      return;
    }

    const nextMessages: Message[] = [
      ...messages,
      {id: `u-${Date.now()}`, role: 'user', content: userText},
    ];
    setMessages(nextMessages);
    setInput('');
    setLoading(true);
    try {
      const answer = await generateAnswer(nextMessages);
      setMessages(prev => [...prev, {id: `a-${Date.now()}`, role: 'assistant', content: answer}]);
    } catch (err: any) {
      const fallback = err?.message?.includes('API key')
        ? 'Missing or invalid API key. Please configure DOCUSAURUS_GEMINI_API_KEY in .env.'
        : err?.message || 'Unexpected error.';
      setError(fallback);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* Floating button */}
      <button
        aria-label={open ? 'Close chat' : 'Open chat'}
        onClick={() => setOpen(v => !v)}
        className="button button--primary"
        style={{
          position: 'fixed',
          right: 20,
          bottom: 20,
          zIndex: 999,
          borderRadius: 999,
          padding: '10px 14px',
          boxShadow: '0 6px 20px rgba(0,0,0,0.12)'
        }}
      >
        {open ? '×' : 'Ask AI'}
      </button>

      {/* Panel */}
      {open && (
        <div
          role="dialog"
          aria-label="AI Documentation Assistant"
          aria-modal="false"
          style={{
            position: 'fixed',
            right: 20,
            bottom: 70,
            width: 'min(420px, 92vw)',
            height: 520,
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: 14,
            boxShadow: '0 20px 40px rgba(2,10,20,0.18)',
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
            zIndex: 998,
          }}
        >
          <div style={{
            padding: '10px 12px',
            background: 'var(--surface)',
            borderBottom: '1px solid var(--border)'
          }}>
            <div style={{fontWeight: 600}}>Robotics Assistant</div>
            <div style={{fontSize: 12, color: 'var(--text-muted)'}}>Humanoid Robotics • Sensors • Perception • Cognition</div>
          </div>

          <div
            ref={bodyRef}
            role="list"
            style={{
              flex: 1,
              padding: 12,
              display: 'flex',
              flexDirection: 'column',
              gap: 8,
              overflowY: 'auto',
              background: 'var(--elev)'
            }}
          >
            {messages
              .filter(m => m.role !== 'system')
              .map(m => (
                <ChatMessage key={m.id} msg={m} />
              ))}
            {loading && (
              <div style={{alignSelf: 'flex-start', color: 'var(--text-muted)'}}>Assistant is typing…</div>
            )}
            {error && (
              <div style={{alignSelf: 'stretch', color: '#b91c1c'}}>Error: {error}</div>
            )}
          </div>

          <form onSubmit={onSend} style={{ padding: 8, borderTop: '1px solid var(--border)', background: 'var(--surface)' }}>
            <label htmlFor="chatbot-input" className="sr-only">Type your question</label>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                id="chatbot-input"
                name="q"
                type="text"
                autoComplete="off"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about sensors, actuators, AI…"
                aria-label="Ask a question"
                style={{
                  flex: 1,
                  background: 'var(--bg)',
                  border: '1px solid var(--border)',
                  borderRadius: 10,
                  padding: '8px 10px'
                }}
              />
              <button className="button button--secondary button--sm" type="submit" disabled={!canSend}>
                {loading ? '…' : 'Send'}
              </button>
            </div>
            <div style={{ marginTop: 6, fontSize: 11, color: 'var(--text-muted)' }}>
              Do not share secrets. Subject to rate limits. {messages.filter(m => m.role === 'user').length}/{maxMessages}
            </div>
          </form>
        </div>
      )}
    </>
  );
}
