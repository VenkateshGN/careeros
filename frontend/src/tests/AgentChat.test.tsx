import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import AgentChat from '../components/AgentChat';
import api from '../api';

// Mock the API client
vi.mock('../api', () => ({
    default: {
        post: vi.fn(),
    },
}));

describe('AgentChat Component', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('UI-04: AI Assistant loads correctly', () => {
        render(<AgentChat />);
        expect(screen.getByText('AI Career Assistant (Google Gemini)')).toBeInTheDocument();
        expect(screen.getByPlaceholderText('Message the agent...')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Send' })).toBeInTheDocument();
        expect(screen.getByText('Ask me about your saved memories, job matches, or career advice!')).toBeInTheDocument();
    });

    it('UI-05 & UI-06 & UI-07: Send question, loading state, and show response', async () => {
        // Mock successful api.post response
        (api.post as any).mockResolvedValueOnce({ data: { reply: 'FastAPI and Python are great SDE skills.' } });

        render(<AgentChat />);

        const input = screen.getByPlaceholderText('Message the agent...');
        const sendBtn = screen.getByRole('button', { name: 'Send' });

        // Enter message and click send
        fireEvent.change(input, { target: { value: 'What skills do I need?' } });
        fireEvent.click(sendBtn);

        // UI-05: Message appears in UI
        expect(screen.getByText('What skills do I need?')).toBeInTheDocument();

        // UI-07: Loading state is shown
        expect(screen.getByText('Agent is reasoning...')).toBeInTheDocument();

        // UI-06: AI response displays in UI
        await waitFor(() => {
            expect(screen.getByText('FastAPI and Python are great SDE skills.')).toBeInTheDocument();
        });

        expect(screen.queryByText('Agent is reasoning...')).not.toBeInTheDocument();
    });

    it('UI-08: Bedrock connection failure error display', async () => {
        // Mock api.post failure
        (api.post as any).mockRejectedValueOnce(new Error('Network Error'));

        render(<AgentChat />);

        const input = screen.getByPlaceholderText('Message the agent...');
        const sendBtn = screen.getByRole('button', { name: 'Send' });

        fireEvent.change(input, { target: { value: 'Hello?' } });
        fireEvent.click(sendBtn);

        await waitFor(() => {
            expect(screen.getByText('Error: Could not connect to AI Agent Memory.')).toBeInTheDocument();
        });
    });

    it('UI-09: Empty messages prevent API submission', () => {
        render(<AgentChat />);
        const sendBtn = screen.getByRole('button', { name: 'Send' });

        // Click send on empty input
        fireEvent.click(sendBtn);
        expect(api.post).not.toHaveBeenCalled();

        // Try whitespace only
        const input = screen.getByPlaceholderText('Message the agent...');
        fireEvent.change(input, { target: { value: '   ' } });
        fireEvent.click(sendBtn);
        expect(api.post).not.toHaveBeenCalled();
    });

    it('UI-10: Multiple messages maintain conversation context visually', async () => {
        (api.post as any)
            .mockResolvedValueOnce({ data: { reply: 'First answer' } })
            .mockResolvedValueOnce({ data: { reply: 'Second answer' } });

        render(<AgentChat />);

        const input = screen.getByPlaceholderText('Message the agent...');
        const sendBtn = screen.getByRole('button', { name: 'Send' });

        // First message
        fireEvent.change(input, { target: { value: 'First question' } });
        fireEvent.click(sendBtn);
        await waitFor(() => expect(screen.getByText('First answer')).toBeInTheDocument());

        // Second message
        fireEvent.change(input, { target: { value: 'Second question' } });
        fireEvent.click(sendBtn);
        await waitFor(() => expect(screen.getByText('Second answer')).toBeInTheDocument());

        // Both questions and answers remain visible
        expect(screen.getByText('First question')).toBeInTheDocument();
        expect(screen.getByText('First answer')).toBeInTheDocument();
        expect(screen.getByText('Second question')).toBeInTheDocument();
        expect(screen.getByText('Second answer')).toBeInTheDocument();
    });
});
