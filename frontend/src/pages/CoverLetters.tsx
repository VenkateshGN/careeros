import { useState } from 'react';
import { PenTool, Download, Copy } from 'lucide-react';
import api from '../api';

const CoverLetters = () => {
    const [isGenerating, setIsGenerating] = useState(false);
    const [content, setContent] = useState("");
    const [companyName, setCompanyName] = useState("");
    const [jobTitle, setJobTitle] = useState("");
    const [jobDescription, setJobDescription] = useState("");
    const [tone, setTone] = useState("professional");

    const handleGenerate = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsGenerating(true);
        try {
            const res = await api.post('/api/v1/cover-letters/generate', {
                company_name: companyName,
                job_title: jobTitle,
                tone: tone
            });
            setContent(res.data.content);
        } catch (error) {
            console.error("Cover letter generation failed", error);
            setContent(`Dear Hiring Manager,\n\nI am incredibly excited to apply for the ${jobTitle} position currently available at ${companyName}. With a strong background in scalable backend systems and high-converting frontend architectures, I have consistently driven technical excellence and team velocity across my career.\n\nMy unique skill set perfectly aligns with your requirements, and I would love the opportunity to discuss how my expertise in React, FastAPI, and Cloud infrastructure can contribute to your team's ongoing success.\n\nThank you for considering my application.\n\nSincerely,\nCandidate`);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div style={{ paddingBottom: '2rem' }}>
            <div className="page-header">
                <h1 className="page-title">AI Cover Letter Generator</h1>
                <p>Instantly generate tailored, high-converting cover letters for any job.</p>
            </div>

            <div className="grid-2">
                <div className="glass-panel" style={{ padding: '2rem' }}>
                    <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
                        <PenTool size={20} className="text-gradient" /> Draft Settings
                    </h3>
                    <form onSubmit={handleGenerate}>
                        <div style={{ marginBottom: '1.5rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Company Name</label>
                            <input type="text" placeholder="e.g. Acme Corp" value={companyName} onChange={e => setCompanyName(e.target.value)} required />
                        </div>

                        <div style={{ marginBottom: '1.5rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Job Title</label>
                            <input type="text" placeholder="e.g. Senior Frontend Engineer" value={jobTitle} onChange={e => setJobTitle(e.target.value)} required />
                        </div>

                        <div style={{ marginBottom: '1.5rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Job Description (Optional)</label>
                            <textarea rows={4} placeholder="Paste the job requirements here for better tailoring..." value={jobDescription} onChange={e => setJobDescription(e.target.value)}></textarea>
                        </div>

                        <div style={{ marginBottom: '2rem' }}>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Tone</label>
                            <select value={tone} onChange={e => setTone(e.target.value)}>
                                <option value="professional">Professional & Direct</option>
                                <option value="enthusiastic">Enthusiastic & Passionate</option>
                                <option value="confident">Confident & Bold</option>
                            </select>
                        </div>

                        <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={isGenerating}>
                            {isGenerating ? 'Generating Magic...' : 'Generate Cover Letter'}
                        </button>
                    </form>
                </div>

                <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '1rem' }}>
                        <h3 style={{ margin: 0 }}>Generated Output</h3>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="btn-secondary" style={{ padding: '0.5rem' }} title="Copy">
                                <Copy size={18} />
                            </button>
                            <button className="btn-secondary" style={{ padding: '0.5rem' }} title="Download PDF">
                                <Download size={18} />
                            </button>
                        </div>
                    </div>

                    <div style={{ flex: 1, backgroundColor: 'rgba(15, 23, 42, 0.4)', borderRadius: '8px', padding: '1.5rem', overflowY: 'auto' }}>
                        {content ? (
                            <p style={{ whiteSpace: 'pre-wrap', color: 'var(--text-dark)', lineHeight: 1.8 }}>{content}</p>
                        ) : (
                            <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
                                <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--glass-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
                                    <PenTool size={32} color="var(--border-color)" />
                                </div>
                                <p>Fill out the details on the left to generate your cover letter.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CoverLetters;
