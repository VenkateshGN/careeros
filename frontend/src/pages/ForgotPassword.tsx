import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Mail, ArrowRight } from 'lucide-react';
import api from '../api';

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            await api.post('/auth/forgot-password', { email });
            setSubmitted(true);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Something went wrong. Please check your network and try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--bg-dark)' }}>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '2rem' }}>
                <div style={{ padding: '2rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '4rem' }}>
                        <div style={{ width: '40px', height: '40px', background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))', borderRadius: '8px' }}></div>
                        <h2 style={{ marginBottom: 0 }} className="text-gradient">CareerOS</h2>
                    </div>

                    <div style={{ maxWidth: '400px', margin: '0 auto', textAlign: 'center' }}>
                        <h3 style={{ marginBottom: '1rem' }}>Reset Password</h3>
                        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
                            Enter your email address and we'll send you a link to reset your password.
                        </p>

                        {!submitted ? (
                            <form onSubmit={handleSubmit} style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                                {error && (
                                    <div style={{ padding: '0.75rem', borderRadius: '8px', background: 'rgba(239,68,68,0.15)', color: '#f87171', border: '1px solid rgba(239,68,68,0.3)', fontSize: '0.875rem' }}>
                                        {error}
                                    </div>
                                )}
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Email Address</label>
                                    <div style={{ position: 'relative' }}>
                                        <Mail size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                        <input
                                            type="email"
                                            required
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                            placeholder="john@example.com"
                                            style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-lighter)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                        />
                                    </div>
                                </div>

                                <button type="submit" disabled={loading} className="btn btn-primary" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', padding: '0.875rem' }}>
                                    {loading ? 'Sending...' : 'Send Reset Link'}
                                    <ArrowRight size={18} />
                                </button>
                            </form>
                        ) : (
                            <div style={{ padding: '2rem', background: 'var(--bg-lighter)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                                <p style={{ color: 'var(--primary-light)', marginBottom: '1rem', fontWeight: 600 }}>Check your inbox!</p>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>We've sent password reset instructions to {email}</p>
                            </div>
                        )}

                        <div style={{ marginTop: '2rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                            Remember your password? <Link to="/login" style={{ color: 'var(--primary-color)', textDecoration: 'none', fontWeight: 600 }}>Back to log in</Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
