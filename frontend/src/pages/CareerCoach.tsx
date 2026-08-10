import { useState } from 'react';
import { Target, ArrowRight, Route, Clock, Award } from 'lucide-react';
import api from '../api';

const CareerCoach = () => {
    const [currentRole, setCurrentRole] = useState('');
    const [targetRole, setTargetRole] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [errorMsg, setErrorMsg] = useState('');

    const handleGenerate = async () => {
        if (!currentRole.trim() || !targetRole.trim()) {
            setErrorMsg("Please provide both tracking roles to generate a roadmap.");
            return;
        }

        setErrorMsg('');
        setLoading(true);
        setResult(null);

        try {
            const res = await api.post('/ai/career-roadmap', {
                current_role: currentRole,
                target_role: targetRole
            }, {
                baseURL: 'http://localhost:8000'
            });
            setResult(res.data);
        } catch (error: any) {
            setErrorMsg("AI roadmap generation failed: " + (error.response?.data?.detail || "Network error."));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h1 style={{ marginBottom: '0.5rem' }}>AI Career Coach</h1>
                    <p style={{ color: 'var(--text-muted)', margin: 0 }}>Discover the exact roadmap needed to reach your dream role.</p>
                </div>
            </div>

            {errorMsg && (
                <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', color: 'var(--danger)', borderRadius: '8px', marginBottom: '1.5rem' }}>
                    {errorMsg}
                </div>
            )}

            <div className="card fade-in" style={{ padding: '2rem', marginBottom: '2rem', display: 'flex', gap: '1.5rem', alignItems: 'center', background: 'linear-gradient(to right, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8))' }}>
                <div style={{ flex: 1 }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Current Role</label>
                    <input
                        type="text" value={currentRole} onChange={(e) => setCurrentRole(e.target.value)}
                        placeholder="e.g. Junior Developer"
                        style={{ width: '100%', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                    />
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', paddingTop: '1.5rem' }}>
                    <ArrowRight color="var(--primary-light)" size={32} />
                </div>

                <div style={{ flex: 1 }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Target Role</label>
                    <input
                        type="text" value={targetRole} onChange={(e) => setTargetRole(e.target.value)}
                        placeholder="e.g. Senior Architecture Lead"
                        style={{ width: '100%', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                    />
                </div>

                <div style={{ paddingTop: '1.5rem' }}>
                    <button
                        onClick={handleGenerate}
                        className="btn btn-primary"
                        disabled={loading}
                        style={{ padding: '1rem 2rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
                    >
                        <Route size={20} />
                        {loading ? 'Synthesizing...' : 'Build Roadmap'}
                    </button>
                </div>
            </div>

            {loading && (
                <div style={{ textAlign: 'center', padding: '4rem' }}>
                    <div style={{ width: '40px', height: '40px', border: '3px solid rgba(99,102,241,0.2)', borderTopColor: 'var(--primary-color)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1rem auto' }}></div>
                    <p style={{ color: 'var(--text-muted)' }}>Gemini is engineering your structural trajectory...</p>
                </div>
            )}

            {result && (
                <div className="card fade-in" style={{ padding: '3rem', animationDelay: '0.1s' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '3rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1.5rem' }}>
                        <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <Target color="var(--primary-light)" size={24} />
                        </div>
                        <div>
                            <h2 style={{ margin: 0, color: 'var(--text-light)' }}>Path to {result.target_role}</h2>
                            <p style={{ margin: 0, color: 'var(--text-muted)' }}>Estimated trajectory computed successfully</p>
                        </div>
                    </div>

                    {/* Roadmap Timeline */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', position: 'relative' }}>
                        {/* Connecting line */}
                        <div style={{ position: 'absolute', left: '23px', top: '24px', bottom: '24px', width: '2px', background: 'var(--border-color)', zIndex: 0 }}></div>

                        {result.steps.map((step: any, idx: number) => (
                            <div key={idx} style={{ display: 'flex', gap: '2rem', position: 'relative', zIndex: 1 }}>
                                {/* Node */}
                                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                    <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'var(--bg-dark)', border: '2px solid var(--primary-light)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary-light)', fontWeight: 'bold' }}>
                                        {step.step_number}
                                    </div>
                                </div>

                                {/* Content Box */}
                                <div style={{ flex: 1, background: 'var(--bg-lighter)', padding: '1.5rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                                        <h3 style={{ margin: 0, fontSize: '1.25rem' }}>{step.title}</h3>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--primary-color)', background: 'rgba(99, 102, 241, 0.1)', padding: '0.4rem 0.8rem', borderRadius: '50px', fontSize: '0.85rem' }}>
                                            <Clock size={16} />
                                            {step.timeline}
                                        </div>
                                    </div>
                                    <p style={{ color: 'var(--text-muted)', lineHeight: '1.6', margin: 0 }}>
                                        {step.description}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div style={{ marginTop: '3rem', padding: '2rem', background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1))', borderRadius: '12px', border: '1px solid var(--primary-color)', textAlign: 'center' }}>
                        <Award size={48} color="var(--primary-light)" style={{ marginBottom: '1rem' }} />
                        <h3 style={{ marginBottom: '0.5rem' }}>Ready to step up?</h3>
                        <p style={{ color: 'var(--text-muted)', margin: 0 }}>Access your Learning Hub to find targeted courses matching step 1 of your roadmap.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CareerCoach;
