import { useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Lock, ArrowRight } from 'lucide-react';
import api from '../api';

const ResetPassword = () => {
    const [searchParams] = useSearchParams();
    const token = searchParams.get('token') || '';
    const email = searchParams.get('email') || '';

    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        if (password.length < 6) {
            setError("Password must be at least 6 characters long.");
            return;
        }

        setLoading(true);
        setError('');
        try {
            await api.post('/auth/reset-password', {
                email,
                token,
                new_password: password
            });
            setSubmitted(true);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Invalid or expired reset token. Please request another link.");
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
                        <h3 style={{ marginBottom: '1rem' }}>Choose a New Password</h3>
                        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
                            Please enter your new password below.
                        </p>

                        {!submitted ? (
                            <form onSubmit={handleSubmit} style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                                {error && (
                                    <div style={{ padding: '0.75rem', borderRadius: '8px', background: 'rgba(239,68,68,0.15)', color: '#f87171', border: '1px solid rgba(239,68,68,0.3)', fontSize: '0.875rem' }}>
                                        {error}
                                    </div>
                                )}
                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>New Password</label>
                                    <div style={{ position: 'relative' }}>
                                        <Lock size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                        <input
                                            type="password"
                                            required
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            placeholder="••••••••"
                                            style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-lighter)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Confirm New Password</label>
                                    <div style={{ position: 'relative' }}>
                                        <Lock size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                        <input
                                            type="password"
                                            required
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                            placeholder="••••••••"
                                            style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-lighter)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                        />
                                    </div>
                                </div>

                                <button type="submit" disabled={loading} className="btn btn-primary" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', padding: '0.875rem' }}>
                                    {loading ? 'Resetting Password...' : 'Reset Password'}
                                    <ArrowRight size={18} />
                                </button>
                            </form>
                        ) : (
                            <div style={{ padding: '2rem', background: 'var(--bg-lighter)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                                <p style={{ color: '#10b981', marginBottom: '1rem', fontWeight: 600 }}>Password updated!</p>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '1.5rem' }}>Your password has been successfully reset. You can now log in with your new credentials.</p>
                                <Link to="/login" className="btn btn-primary" style={{ display: 'inline-flex', padding: '0.75rem 1.5rem', textDecoration: 'none' }}>
                                    Go to Login
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResetPassword;
