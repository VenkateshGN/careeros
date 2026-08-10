import { useState } from 'react';
import { Target, CheckCircle, XCircle, Briefcase, FileText, Zap } from 'lucide-react';
import api from '../api';

const JobMatching = () => {
    const [resumeText, setResumeText] = useState('');
    const [jobDescription, setJobDescription] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [errorMsg, setErrorMsg] = useState('');

    const handleAnalyze = async () => {
        if (!resumeText.trim() || !jobDescription.trim()) {
            setErrorMsg("Please provide both your resume and the job description.");
            return;
        }

        setErrorMsg('');
        setLoading(true);
        setResult(null);

        try {
            const res = await api.post('/ai/job-matching', {
                resume_text: resumeText,
                job_description: jobDescription
            }, {
                baseURL: 'http://localhost:8000'
            });
            setResult(res.data);
        } catch (error: any) {
            setErrorMsg("AI analysis failed: " + (error.response?.data?.detail || "Network error."));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ marginBottom: 0 }}>AI Job Matcher</h1>
                <p style={{ color: 'var(--text-muted)' }}>Powered by Gemini 1.5</p>
            </div>

            {errorMsg && (
                <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', color: 'var(--danger)', borderRadius: '8px', marginBottom: '1.5rem' }}>
                    {errorMsg}
                </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                <div className="card fade-in" style={{ padding: '2rem', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                        <div style={{ padding: '0.5rem', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '8px' }}>
                            <FileText color="var(--primary-light)" size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>Your Resume</h3>
                    </div>
                    <textarea
                        value={resumeText}
                        onChange={(e) => setResumeText(e.target.value)}
                        placeholder="Paste your plain text resume here..."
                        style={{ flex: 1, minHeight: '300px', padding: '1rem', background: 'var(--bg-dark)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-light)', resize: 'vertical' }}
                    />
                </div>

                <div className="card fade-in" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', animationDelay: '0.1s' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
                        <div style={{ padding: '0.5rem', background: 'rgba(236, 72, 153, 0.1)', borderRadius: '8px' }}>
                            <Briefcase color="#ec4899" size={20} />
                        </div>
                        <h3 style={{ margin: 0 }}>Job Description</h3>
                    </div>
                    <textarea
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        placeholder="Paste the target job description here..."
                        style={{ flex: 1, minHeight: '300px', padding: '1rem', background: 'var(--bg-dark)', border: '1px solid var(--border-color)', borderRadius: '8px', color: 'var(--text-light)', resize: 'vertical' }}
                    />
                </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '3rem' }}>
                <button
                    onClick={handleAnalyze}
                    className="btn btn-primary"
                    disabled={loading}
                    style={{ padding: '1rem 2rem', fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', minWidth: '250px', justifyContent: 'center' }}
                >
                    <Zap size={20} />
                    {loading ? 'Analyzing Syntactics...' : 'Run Analysis Mapping'}
                </button>
            </div>

            {loading && (
                <div style={{ textAlign: 'center', padding: '3rem' }}>
                    <div style={{ width: '40px', height: '40px', border: '3px solid rgba(99,102,241,0.2)', borderTopColor: 'var(--primary-color)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1rem auto' }}></div>
                    <p style={{ color: 'var(--text-muted)' }}>Querying Google Knowledge Graph...</p>
                </div>
            )}

            {result && (
                <div className="card fade-in" style={{ padding: '3rem', borderTop: '4px solid var(--primary-light)' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(200px, 1fr) 3fr', gap: '3rem' }}>

                        {/* Score Gauge */}
                        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center' }}>
                            <div style={{ position: 'relative', width: '150px', height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '50%', border: `8px solid ${result.match_score > 70 ? 'var(--success)' : result.match_score > 40 ? '#f59e0b' : 'var(--danger)'}` }}>
                                <h1 style={{ fontSize: '3rem', margin: 0, color: 'var(--text-light)' }}>{result.match_score}%</h1>
                            </div>
                            <h3 style={{ marginTop: '1.5rem', color: 'var(--text-muted)' }}>Match Accuracy</h3>
                        </div>

                        {/* Analysis Data */}
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                            <div>
                                <h3 style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    <Target size={20} color="var(--primary-light)" />
                                    AI Recommendation
                                </h3>
                                <p style={{ lineHeight: '1.6', color: 'var(--text-light)', background: 'rgba(99, 102, 241, 0.05)', padding: '1.5rem', borderRadius: '8px', borderLeft: '4px solid var(--primary-color)' }}>
                                    {result.recommendation}
                                </p>
                            </div>

                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                                {/* Parsed Skills Found */}
                                <div>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--success)', marginBottom: '1rem' }}>
                                        <CheckCircle size={18} /> Matched Skills
                                    </h4>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        {result.matched_skills.map((skill: string, idx: number) => (
                                            <span key={idx} style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', padding: '0.4rem 0.8rem', borderRadius: '50px', fontSize: '0.85rem', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>

                                {/* Skills Gap */}
                                <div>
                                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)', marginBottom: '1rem' }}>
                                        <XCircle size={18} /> Missing Attributes
                                    </h4>
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        {result.missing_skills.map((skill: string, idx: number) => (
                                            <span key={idx} style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', padding: '0.4rem 0.8rem', borderRadius: '50px', fontSize: '0.85rem', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            )}
        </div>
    );
};

export default JobMatching;
