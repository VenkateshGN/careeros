import { useState } from 'react';
import api from '../api';

const AgentChat = () => {
    const [messages, setMessages] = useState<{ role: 'user' | 'agent', text: string }[]>([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userText = input.trim();
        setMessages(prev => [...prev, { role: 'user', text: userText }]);
        setInput('');
        setLoading(true);

        try {
            console.log("Outgoing AI Chat Request URL:", { message: userText });
            const { data } = await api.post('/ai/agent/chat', {
                message: userText
            });
            setMessages(prev => [...prev, { role: 'agent', text: data.reply }]);
        } catch (error) {
            console.error("AI Chat connection error:", error);
            setMessages(prev => [...prev, { role: 'agent', text: "Error: Could not connect to AI Agent Memory." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '400px', background: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px', overflow: 'hidden' }}>
            <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-color)', background: 'var(--bg-card-hover)' }}>
                <h3 style={{ margin: 0, fontSize: '1rem' }}>AI Career Assistant (Google Gemini)</h3>
                <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', color: 'var(--text-muted)' }}>Powered by CockroachDB Vector Memory</p>
            </div>

            <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {messages.length === 0 && (
                    <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '2rem' }}>
                        Ask me about your saved memories, job matches, or career advice!
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div key={idx} style={{
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        background: msg.role === 'user' ? 'var(--primary-color)' : 'var(--glass-bg)',
                        color: msg.role === 'user' ? 'var(--bg-color)' : 'var(--text-color)',
                        padding: '0.75rem 1rem',
                        borderRadius: '12px',
                        maxWidth: '80%'
                    }}>
                        {msg.text}
                    </div>
                ))}
                {loading && <div style={{ alignSelf: 'flex-start', color: 'var(--text-muted)' }}>Agent is reasoning...</div>}
            </div>

            <div style={{ padding: '1rem', borderTop: '1px solid var(--border-color)', display: 'flex', gap: '0.5rem' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Message the agent..."
                    style={{ flex: 1, padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--border-color)', background: 'var(--bg-color)', color: 'var(--text-color)' }}
                />
                <button onClick={handleSend} disabled={loading} style={{ padding: '0.5rem 1rem', borderRadius: '4px', background: 'var(--primary-color)', color: 'var(--bg-color)', border: 'none', cursor: 'pointer' }}>
                    Send
                </button>
            </div>
        </div>
    );
};

export default AgentChat;
