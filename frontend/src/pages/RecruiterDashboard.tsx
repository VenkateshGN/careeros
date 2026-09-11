import { useState, useEffect } from 'react';
// Removed useUserStore for TS cleanliness
import { Briefcase, Users, PlusCircle, BarChart2, CheckCircle, ChevronRight } from 'lucide-react';
import api from '../api';

interface Job {
    id: string;
    title: string;
    location: string;
    posted_at: string;
}

const RecruiterDashboard = () => {
    const [jobs, setJobs] = useState<Job[]>([]);

    // New Job Form State
    const [showPostJob, setShowPostJob] = useState(false);
    const [newJob, setNewJob] = useState({ title: '', location: '', description: '', salary_min: 0, salary_max: 0 });

    useEffect(() => {
        const fetchRecruiterJobs = async () => {
            try {
                const res = await api.get('/jobs/');
                setJobs(res.data);
            } catch (err) {
                console.error("Failed fetching jobs", err);
            }
        };
        fetchRecruiterJobs();
    }, []);

    const handleCreateJob = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            // Hardcode a mock company_id uuid to bypass strict constraints for now
            const mockCompanyId = '00000000-0000-0000-0000-000000000000';
            await api.post('/jobs/', { ...newJob, company_id: mockCompanyId }, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } });
            setShowPostJob(false);
            // Refresh
            const res = await api.get('/jobs/');
            setJobs(res.data);
        } catch (error) {
            console.error("Failed to post job");
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <div>
                    <h1 style={{ marginBottom: '0.5rem' }}>Recruiter Command Center</h1>
                    <p style={{ color: 'var(--text-muted)', margin: 0 }}>Manage your job listings and review top applicants natively.</p>
                </div>
                <button onClick={() => setShowPostJob(!showPostJob)} className="btn btn-primary" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <PlusCircle size={18} />
                    {showPostJob ? 'Back to Dashboard' : 'Post New Job'}
                </button>
            </div>

            {showPostJob ? (
                <div className="card fade-in" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
                    <h2 style={{ marginBottom: '2rem' }}>Create Job Listing</h2>
                    <form onSubmit={handleCreateJob} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Job Title</label>
                            <input type="text" required value={newJob.title} onChange={e => setNewJob({ ...newJob, title: e.target.value })} style={{ width: '100%', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }} placeholder="e.g. Senior Frontend Engineer" />
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Location</label>
                                <input type="text" required value={newJob.location} onChange={e => setNewJob({ ...newJob, location: e.target.value })} style={{ width: '100%', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }} placeholder="e.g. Remote, NY" />
                            </div>
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <div style={{ flex: 1 }}>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Min Salary (₹)</label>
                                    <input type="number" value={newJob.salary_min} onChange={e => setNewJob({ ...newJob, salary_min: parseInt(e.target.value) })} style={{ width: '100%', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }} />
                                </div>
                                <div style={{ flex: 1 }}>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Max Salary (₹)</label>
                                    <input type="number" value={newJob.salary_max} onChange={e => setNewJob({ ...newJob, salary_max: parseInt(e.target.value) })} style={{ width: '100%', padding: '0.875rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }} />
                                </div>
                            </div>
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Job Description</label>
                            <textarea required value={newJob.description} onChange={e => setNewJob({ ...newJob, description: e.target.value })} style={{ width: '100%', padding: '1rem', minHeight: '200px', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box', resize: 'vertical' }} placeholder="Outline responsibilities and requirements..." />
                        </div>

                        <div style={{ marginTop: '1rem' }}>
                            <button type="submit" className="btn btn-primary" style={{ padding: '1rem 2rem', width: '100%' }}>Publish Listing</button>
                        </div>
                    </form>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    {/* Metrics Row */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem' }}>
                        <div className="card fade-in" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                            <div style={{ width: '56px', height: '56px', borderRadius: '12px', background: 'rgba(99, 102, 241, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <Briefcase size={28} color="var(--primary-light)" />
                            </div>
                            <div>
                                <p style={{ margin: '0 0 0.25rem 0', color: 'var(--text-muted)', fontSize: '0.875rem' }}>Active Listings</p>
                                <h2 style={{ margin: 0, fontSize: '1.75rem' }}>{jobs.length}</h2>
                            </div>
                        </div>
                        <div className="card fade-in" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.5rem', animationDelay: '0.1s' }}>
                            <div style={{ width: '56px', height: '56px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <Users size={28} color="var(--success)" />
                            </div>
                            <div>
                                <p style={{ margin: '0 0 0.25rem 0', color: 'var(--text-muted)', fontSize: '0.875rem' }}>Total Applicants</p>
                                <h2 style={{ margin: 0, fontSize: '1.75rem' }}>0</h2>
                            </div>
                        </div>
                        <div className="card fade-in" style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1.5rem', animationDelay: '0.2s' }}>
                            <div style={{ width: '56px', height: '56px', borderRadius: '12px', background: 'rgba(236, 72, 153, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <CheckCircle size={28} color="#ec4899" />
                            </div>
                            <div>
                                <p style={{ margin: '0 0 0.25rem 0', color: 'var(--text-muted)', fontSize: '0.875rem' }}>Hires Made</p>
                                <h2 style={{ margin: 0, fontSize: '1.75rem' }}>0</h2>
                            </div>
                        </div>
                    </div>

                    {/* Listings Table */}
                    <div className="card fade-in" style={{ padding: '2rem' }}>
                        <h3 style={{ marginBottom: '1.5rem' }}>Your Listings</h3>
                        {jobs.length === 0 ? (
                            <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                                <BarChart2 size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                                <p>You have no active job postings.</p>
                            </div>
                        ) : (
                            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                                        <th style={{ padding: '1rem 0' }}>Job Title</th>
                                        <th style={{ padding: '1rem 0' }}>Location</th>
                                        <th style={{ padding: '1rem 0' }}>Posted</th>
                                        <th style={{ padding: '1rem 0', textAlign: 'right' }}>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {jobs.map((job) => (
                                        <tr key={job.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                            <td style={{ padding: '1rem 0', fontWeight: 500 }}>{job.title}</td>
                                            <td style={{ padding: '1rem 0', color: 'var(--text-muted)' }}>{job.location}</td>
                                            <td style={{ padding: '1rem 0', color: 'var(--text-muted)' }}>{new Date(job.posted_at).toLocaleDateString()}</td>
                                            <td style={{ padding: '1rem 0', textAlign: 'right' }}>
                                                <button className="btn" style={{ background: 'transparent', border: '1px solid var(--border-color)', color: 'var(--text-light)', padding: '0.5rem 1rem', display: 'inline-flex', alignItems: 'center', gap: '0.5rem' }}>
                                                    View Apps <ChevronRight size={14} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default RecruiterDashboard;
