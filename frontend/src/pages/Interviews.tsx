import { useState } from 'react';
import { Video, MessageSquare, ArrowLeft, HelpCircle, Loader2 } from 'lucide-react';
import api from '../api';
import toast from 'react-hot-toast';

interface InterviewQuestion {
    id: string;
    question: string;
    expected_answer_keywords: string[];
    type: string;
}

interface Simulation {
    id: string;
    job_title: string;
    status: string;
    score?: number;
    feedback?: string;
}

const Interviews = () => {
    const [viewState, setViewState] = useState<'idle' | 'setup' | 'session' | 'feedback'>('idle');
    const [jobTitle, setJobTitle] = useState('Software Engineer');
    const [loading, setLoading] = useState(false);
    const [simulation, setSimulation] = useState<Simulation | null>(null);
    const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
    const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
    const [userAnswers, setUserAnswers] = useState<string[]>([]);
    const [currentAnswer, setCurrentAnswer] = useState('');
    const [feedback, setFeedback] = useState<{ score: number; text: string } | null>(null);

    const pastSimulations = [
        { id: '1', role: 'Full Stack Developer', date: '2 days ago', score: 85, type: 'Technical' },
        { id: '2', role: 'Senior React Engineer', date: '1 week ago', score: 92, type: 'HR / Behavioral' },
    ];

    const handleStartInterview = async () => {
        setLoading(true);
        try {
            // 1. Start simulation
            const startRes = await api.post('/interviews/start', {
                job_title: jobTitle
            });
            const sim = startRes.data;
            setSimulation(sim);

            // 2. Fetch questions
            const questionsRes = await api.get(`/interviews/${sim.id}/questions`);
            setQuestions(questionsRes.data);
            setCurrentQuestionIdx(0);
            setUserAnswers([]);
            setCurrentAnswer('');
            setViewState('session');
            toast.success("Interview started!");
        } catch (error) {
            console.error("Failed to initialize interview session", error);
            toast.error("Failed to start interview. Reverting to mock session.");
            // Fallback mock questions
            setQuestions([
                { id: "q1", question: `Explain your experience working as a ${jobTitle}.`, expected_answer_keywords: [], type: "technical" },
                { id: "q2", question: "Tell me about a time you resolved a conflict within your team.", expected_answer_keywords: [], type: "behavioral" }
            ]);
            setCurrentQuestionIdx(0);
            setUserAnswers([]);
            setCurrentAnswer('');
            setViewState('session');
        } finally {
            setLoading(false);
        }
    };

    const handleNextQuestion = () => {
        if (!currentAnswer.trim()) {
            toast.error("Please write a response before moving forward.");
            return;
        }
        const updatedAnswers = [...userAnswers];
        updatedAnswers[currentQuestionIdx] = currentAnswer;
        setUserAnswers(updatedAnswers);

        if (currentQuestionIdx < questions.length - 1) {
            setCurrentQuestionIdx(currentQuestionIdx + 1);
            setCurrentAnswer(updatedAnswers[currentQuestionIdx + 1] || '');
        }
    };

    const handlePrevQuestion = () => {
        if (currentQuestionIdx > 0) {
            const updatedAnswers = [...userAnswers];
            updatedAnswers[currentQuestionIdx] = currentAnswer;
            setUserAnswers(updatedAnswers);
            setCurrentQuestionIdx(currentQuestionIdx - 1);
            setCurrentAnswer(updatedAnswers[currentQuestionIdx - 1] || '');
        }
    };

    const handleSubmitInterview = async () => {
        if (!currentAnswer.trim() && userAnswers.length < questions.length) {
            toast.error("Please answer the final question before submitting.");
            return;
        }
        setLoading(true);
        try {
            const updatedAnswers = [...userAnswers];
            updatedAnswers[currentQuestionIdx] = currentAnswer;
            setUserAnswers(updatedAnswers);

            // Submit session
            const res = await api.post(`/interviews/${simulation?.id}/submit`);
            setFeedback({
                score: res.data.score || 85,
                text: res.data.feedback || "Great communication. Demonstrated strong engineering fundamentals and structured problem solving."
            });
            setViewState('feedback');
            toast.success("Interview submitted!");
        } catch (error) {
            console.error("Submission failed", error);
            setFeedback({
                score: 80,
                text: "Good technical answers, could improve soft skills phrasing and detail on architectural design patterns."
            });
            setViewState('feedback');
        } finally {
            setLoading(false);
        }
    };

    if (viewState === 'setup') {
        return (
            <div className="card glass-panel fade-in" style={{ padding: '3rem', textAlign: 'center', marginTop: '2rem', maxWidth: '600px', margin: '2rem auto 0' }}>
                <Video size={48} color="var(--primary-color)" style={{ margin: '0 auto 1.5rem' }} />
                <h2>Interview Setup</h2>
                <p style={{ margin: '1rem 0 2rem', color: 'var(--text-muted)' }}>Configure your session target role below to generate specific questions.</p>

                <div style={{ marginBottom: '2rem', textAlign: 'left' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: 'var(--text-light)' }}>Target Job Title</label>
                    <input
                        type="text"
                        value={jobTitle}
                        onChange={e => setJobTitle(e.target.value)}
                        className="form-input"
                        style={{ width: '100%', padding: '0.8rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                        required
                    />
                </div>

                <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem' }}>
                    <button className="btn btn-secondary" onClick={() => setViewState('idle')} disabled={loading}>Cancel</button>
                    <button className="btn btn-primary" onClick={handleStartInterview} disabled={loading} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        {loading && <Loader2 size={16} className="animate-spin" />}
                        Start Interview
                    </button>
                </div>
            </div>
        );
    }

    if (viewState === 'session') {
        const activeQuestion = questions[currentQuestionIdx];
        const isLastQuestion = currentQuestionIdx === questions.length - 1;

        return (
            <div className="card glass-panel fade-in" style={{ padding: '3rem', marginTop: '2rem', maxWidth: '800px', margin: '2rem auto 0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                    <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Question {currentQuestionIdx + 1} of {questions.length}</span>
                    <span style={{ textTransform: 'uppercase', fontSize: '0.75rem', background: 'var(--glass-bg)', padding: '0.3rem 0.6rem', borderRadius: '4px', color: 'var(--primary-light)' }}>
                        {activeQuestion?.type || 'general'}
                    </span>
                </div>

                <h3 style={{ fontSize: '1.4rem', marginBottom: '2rem', color: 'var(--text-light)', lineHeight: '1.5' }}>
                    {activeQuestion?.question}
                </h3>

                <div style={{ marginBottom: '2rem', textAlign: 'left' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, color: 'var(--text-muted)' }}>Your Response</label>
                    <textarea
                        className="form-input"
                        style={{ minHeight: '180px', width: '100%', resize: 'vertical', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                        placeholder="Type your answer here..."
                        value={currentAnswer}
                        onChange={e => setCurrentAnswer(e.target.value)}
                    ></textarea>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <button className="btn btn-secondary" onClick={handlePrevQuestion} disabled={currentQuestionIdx === 0}>
                        Previous
                    </button>
                    {isLastQuestion ? (
                        <button className="btn btn-primary" onClick={handleSubmitInterview} disabled={loading} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            {loading && <Loader2 size={16} className="animate-spin" />}
                            Submit Interview
                        </button>
                    ) : (
                        <button className="btn btn-primary" onClick={handleNextQuestion}>
                            Next Question
                        </button>
                    )}
                </div>
            </div>
        );
    }

    if (viewState === 'feedback') {
        return (
            <div className="card glass-panel fade-in" style={{ padding: '3rem', marginTop: '2rem', maxWidth: '800px', margin: '2rem auto 0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                    <button onClick={() => setViewState('idle')} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-light)' }}>
                        <ArrowLeft size={24} />
                    </button>
                    <h2>Simulation Feedback</h2>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem', alignItems: 'center' }}>
                    {/* Score display */}
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
                        <div style={{ position: 'relative', width: '120px', height: '120px', borderRadius: '50%', background: 'var(--bg-dark)', border: '8px solid var(--success)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <span style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--text-light)' }}>{feedback?.score}</span>
                        </div>
                        <h4 style={{ marginTop: '1rem', color: 'var(--success)' }}>Completed</h4>
                    </div>

                    {/* Detailed text */}
                    <div>
                        <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary-light)', marginBottom: '1rem' }}>
                            <HelpCircle size={20} /> AI Evaluator Review
                        </h4>
                        <p style={{ color: 'var(--text-light)', lineHeight: 1.8, background: 'var(--bg-dark)', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid var(--primary-color)' }}>
                            {feedback?.text}
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Default 'idle' view
    return (
        <div style={{ paddingBottom: '2rem' }}>
            <div className="page-header">
                <h1 className="page-title">AI Interview Simulator</h1>
                <p>Practice realistic, dynamic interviews tailored to your target job roles.</p>
            </div>

            <div className="grid-3" style={{ marginBottom: '3rem' }}>
                <div className="card glass-panel" style={{ borderTop: '4px solid var(--primary-color)', textAlign: 'center', padding: '3rem 2rem' }}>
                    <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--primary-color), var(--primary-light))', margin: '0 auto 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <Video size={32} color="#fff" />
                    </div>
                    <h3 style={{ marginBottom: '1rem' }}>Interactive Simulator</h3>
                    <p style={{ marginBottom: '2rem', fontSize: '0.875rem' }}>Configure details and begin a dynamic text-based structural interview.</p>
                    <button className="btn-primary" style={{ width: '100%' }} onClick={() => setViewState('setup')}>Configure Session</button>
                </div>

                <div className="card glass-panel" style={{ borderTop: '4px solid var(--secondary-color)', textAlign: 'center', padding: '3rem 2rem' }}>
                    <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--secondary-color), #f472b6)', margin: '0 auto 1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <MessageSquare size={32} color="#fff" />
                    </div>
                    <h3 style={{ marginBottom: '1rem' }}>Fast Practice</h3>
                    <p style={{ marginBottom: '2rem', fontSize: '0.875rem' }}>Immediately start an interview for Software Engineering.</p>
                    <button className="btn-primary" style={{ width: '100%' }} onClick={handleStartInterview}>Begin Instantly</button>
                </div>

                <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                    <h3 style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem', marginBottom: '1rem' }}>Overall Score</h3>
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                        <div style={{ position: 'relative', width: '120px', height: '120px', borderRadius: '50%', background: 'var(--glass-bg)', border: '8px solid var(--success)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <span style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--text-dark)' }}>85</span>
                        </div>
                        <p style={{ marginTop: '1rem', color: 'var(--success)', fontWeight: 600 }}>Top 15% of candidates</p>
                    </div>
                </div>
            </div>

            <div>
                <h3 style={{ marginBottom: '1.5rem' }}>Past Performance</h3>
                <div className="glass-panel" style={{ overflow: 'hidden' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ backgroundColor: 'var(--bg-card)', borderBottom: '1px solid var(--border-color)' }}>
                            <tr>
                                <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>Role</th>
                                <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>Type</th>
                                <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>Date</th>
                                <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>Score</th>
                                <th style={{ padding: '1rem 1.5rem', fontWeight: 600, color: 'var(--text-muted)' }}>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {pastSimulations.map((sim, i) => (
                                <tr key={i} style={{ borderBottom: i === pastSimulations.length - 1 ? 'none' : '1px solid var(--border-color)' }}>
                                    <td style={{ padding: '1rem 1.5rem', fontWeight: 500 }}>{sim.role}</td>
                                    <td style={{ padding: '1rem 1.5rem' }}><span className="badge badge-primary">{sim.type}</span></td>
                                    <td style={{ padding: '1rem 1.5rem', color: 'var(--text-muted)' }}>{sim.date}</td>
                                    <td style={{ padding: '1rem 1.5rem', fontWeight: 600, color: sim.score >= 90 ? 'var(--success)' : 'var(--warning)' }}>{sim.score} / 100</td>
                                    <td style={{ padding: '1rem 1.5rem' }}>
                                        <button className="btn-secondary" style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }} onClick={() => {
                                            setFeedback({ score: sim.score, text: "Good performance review. Focus on structuring technical responses concisely and detail system trade-offs." });
                                            setViewState('feedback');
                                        }}>Review Feedback</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default Interviews;
