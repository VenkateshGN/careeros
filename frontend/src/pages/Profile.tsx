import { useState, useEffect } from 'react';
import { useUserStore } from '../store';
import { User, Mail, Globe, Code, Camera, Save } from 'lucide-react';
import api from '../api';
import toast from 'react-hot-toast';

const Profile = () => {
    const { user, setUser } = useUserStore();
    const [loading, setLoading] = useState(false);

    // Form state
    const [formData, setFormData] = useState({
        name: user?.name || '',
        email: user?.email || '',
        bio: '',
        skills: '',
        github: '',
        linkedin: ''
    });

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const res = await api.get('/users/me');
                const data = res.data;
                setFormData({
                    name: data.full_name || '',
                    email: data.email || '',
                    bio: data.bio || '',
                    skills: data.skills || '',
                    github: data.github_url || '',
                    linkedin: data.linkedin_url || ''
                });
            } catch (error) {
                console.error("Failed to fetch profile", error);
            }
        };
        fetchProfile();
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async (e: React.FormEvent) => {
        if (e) e.preventDefault();
        setLoading(true);
        try {
            const parseUrl = (val: string) => {
                if (!val || val.trim() === '') return undefined;
                return val.trim();
            };

            const payload = {
                full_name: formData.name,
                bio: formData.bio,
                skills: formData.skills,
                github_url: parseUrl(formData.github),
                linkedin_url: parseUrl(formData.linkedin)
            };

            const res = await api.put('/users/me', payload);
            setUser({ ...user, name: res.data.full_name, email: res.data.email });
            toast.success("Profile updated successfully!");
        } catch (error) {
            console.error("Failed to update profile", error);
            toast.error("Failed to update profile. Please ensure URLs are valid format.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ marginBottom: 0 }}>My Profile</h1>
                <button
                    onClick={handleSave}
                    className="btn btn-primary"
                    disabled={loading}
                    style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem 1rem' }}
                >
                    <Save size={16} />
                    {loading ? 'Saving...' : 'Save Changes'}
                </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
                {/* Left Column: Avatar & Quick Info */}
                <div className="card fade-in" style={{ animationDelay: '0.1s', display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', padding: '3rem 2rem' }}>
                    <div style={{ position: 'relative', marginBottom: '1.5rem' }}>
                        <div style={{ width: '120px', height: '120px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <User size={50} color="white" />
                        </div>
                        <button style={{ position: 'absolute', bottom: 0, right: 0, width: '36px', height: '36px', borderRadius: '50%', background: 'var(--bg-lighter)', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
                            <Camera size={16} color="var(--text-light)" />
                        </button>
                    </div>
                    <h3 style={{ marginBottom: '0.5rem' }}>{formData.name}</h3>
                    <p style={{ color: 'var(--text-muted)', textTransform: 'capitalize' }}>{user?.role}</p>
                </div>

                {/* Right Column: Settings Form */}
                <div className="card fade-in" style={{ animationDelay: '0.2s', padding: '2rem' }}>
                    <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Personal Information</h3>

                    <form style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Full Name</label>
                                <div style={{ position: 'relative' }}>
                                    <User size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                    <input
                                        type="text" name="name" value={formData.name} onChange={handleChange}
                                        style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                    />
                                </div>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Email Address</label>
                                <div style={{ position: 'relative' }}>
                                    <Mail size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                    <input
                                        type="email" name="email" value={formData.email} disabled
                                        style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-muted)', boxSizing: 'border-box', opacity: 0.7 }}
                                    />
                                </div>
                            </div>
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Short Bio</label>
                            <textarea
                                name="bio" value={formData.bio} onChange={handleChange} placeholder="I am an enthusiastic software engineer..."
                                rows={4}
                                style={{ width: '100%', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box', resize: 'vertical' }}
                            />
                        </div>

                        <div>
                            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>Top Skills (comma separated)</label>
                            <input
                                type="text" name="skills" value={formData.skills} onChange={handleChange} placeholder="Python, React, Docker..."
                                style={{ width: '100%', padding: '0.75rem 1rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                            />
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1rem' }}>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>GitHub URL</label>
                                <div style={{ position: 'relative' }}>
                                    <Code size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                    <input
                                        type="url" name="github" value={formData.github} onChange={handleChange} placeholder="https://github.com/..."
                                        style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                    />
                                </div>
                            </div>
                            <div>
                                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500, fontSize: '0.875rem', color: 'var(--text-muted)' }}>LinkedIn URL</label>
                                <div style={{ position: 'relative' }}>
                                    <Globe size={18} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                                    <input
                                        type="url" name="linkedin" value={formData.linkedin} onChange={handleChange} placeholder="https://linkedin.com/in/..."
                                        style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '8px', border: '1px solid var(--border-color)', background: 'var(--bg-dark)', color: 'var(--text-light)', boxSizing: 'border-box' }}
                                    />
                                </div>
                            </div>
                        </div>

                    </form>
                </div>
            </div>
        </div>
    );
};

export default Profile;
