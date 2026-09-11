import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useUserStore } from '../store';
import { User, Lock, ArrowRight } from 'lucide-react';
import api from '../api';

const Login = () => {
    const navigate = useNavigate();
    const { setUser } = useUserStore();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [errorMsg, setErrorMsg] = useState('');

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setErrorMsg('');

        try {
            // Backend auth is outside of /api/v1 prefix
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const res = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            const token = res.data.access_token;
            localStorage.setItem('token', token);

            // Now fetch the user identity
            const userRes = await api.get('/users/me', {
                headers: { Authorization: `Bearer ${token}` }
            });

            const userData = userRes.data;
            setUser({ id: userData.id, name: userData.full_name, role: userData.role, email: userData.email });

            navigate('/dashboard');
        } catch (error: any) {
            setErrorMsg(error.response?.data?.detail || "Invalid credentials. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', background: 'var(--bg-dark)' }}>
            <div className="card glass-panel fade-in" style={{ width: '100%', maxWidth: '400px', padding: '3rem 2rem', textAlign: 'center' }}>
                <div style={{ paddingBottom: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{ width: '40px', height: '40px', background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))', borderRadius: '8px' }}></div>
                    <h2 style={{ marginBottom: 0 }} className="text-gradient">CareerOS</h2>
                </div>

                <h3 style={{ marginBottom: '2rem' }}>Welcome Back</h3>

                {errorMsg && (
                    <div style={{ padding: '0.75rem', marginBottom: '1.5rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--danger)', color: 'var(--danger)', borderRadius: '8px', fontSize: '0.875rem' }}>
                        {errorMsg}
                    </div>
                )}

                <form onSubmit={handleLogin} style={{ textAlign: 'left', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div>
                        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Email Address</label>
                        <div style={{ position: 'relative' }}>
                            <User size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                            <input
                                type="email"
                                className="form-input"
                                style={{ width: '100%', paddingLeft: '2.5rem' }}
                                placeholder="name@example.com"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <label style={{ margin: 0, fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Password</label>
                            <Link to="/forgot-password" style={{ fontSize: '0.75rem', color: 'var(--primary-color)', textDecoration: 'none', fontWeight: 500 }}>Forgot Password?</Link>
                        </div>
                        <div style={{ position: 'relative' }}>
                            <Lock size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                            <input
                                type="password"
                                className="form-input"
                                style={{ width: '100%', paddingLeft: '2.5rem' }}
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                        </div>
                    </div>

                    <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '1rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem' }} disabled={loading}>
                        {loading ? 'Authenticating...' : (
                            <>Sign In <ArrowRight size={18} /></>
                        )}
                    </button>
                </form>

                <p style={{ marginTop: '2rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                    Don't have an account? <Link to="/register" style={{ color: 'var(--primary-color)', textDecoration: 'none', fontWeight: 600 }}>Create one</Link>
                </p>
            </div>
        </div>
    );
};

export default Login;
