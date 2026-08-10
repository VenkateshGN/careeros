import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { LayoutDashboard, FileText, MonitorPlay, BookOpen, User, Bell, Briefcase } from 'lucide-react';
import { useUserStore } from '../store';
import ErrorBoundary from './ErrorBoundary';

const Sidebar = () => {
    const { user } = useUserStore();

    return (
        <aside className="sidebar fade-in">
            <div style={{ paddingBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{ width: '32px', height: '32px', background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))', borderRadius: '8px' }}></div>
                <h2 style={{ marginBottom: 0 }} className="text-gradient">CareerOS</h2>
            </div>

            <nav style={{ flex: 1 }}>
                <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1rem', marginLeft: '1rem' }}>Menu</p>
                <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <LayoutDashboard size={20} /> Dashboard
                </NavLink>
                <NavLink to="/jobs" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <Briefcase size={20} /> Job Portal
                </NavLink>
                <NavLink to="/profile" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <User size={20} /> My Profile
                </NavLink>
                <NavLink to="/resumes" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <FileText size={20} /> Resumes
                </NavLink>
                <NavLink to="/cover-letters" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <FileText size={20} /> Cover Letters
                </NavLink>
                <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', marginTop: '1.5rem', marginBottom: '1rem', marginLeft: '1rem' }}>AI Tooling</p>
                <NavLink to="/job-matching" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <FileText size={20} /> AI Job Matcher
                </NavLink>
                <NavLink to="/career-coach" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <User size={20} /> Career Coach
                </NavLink>
                <NavLink to="/interviews" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <MonitorPlay size={20} /> AI Interviews
                </NavLink>
                <NavLink to="/learning" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                    <BookOpen size={20} /> Learning Hub
                </NavLink>

                {user?.role === 'recruiter' && (
                    <>
                        <p style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.1em', marginTop: '1.5rem', marginBottom: '1rem', marginLeft: '1rem', color: 'var(--primary-color)' }}>Recruiter Portal</p>
                        <NavLink to="/recruiter" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                            <Briefcase size={20} /> Employer Dashboard
                        </NavLink>
                    </>
                )}
            </nav>
        </aside>
    );
};

const Topbar = () => {
    const { user, logout } = useUserStore();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <header className="topbar fade-in" style={{ animationDelay: '0.1s' }}>
            <div className="search-bar" style={{ flex: 1, maxWidth: '400px' }}>
                <input type="text" placeholder="Search jobs, skills, or courses..." />
            </div>
            <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                <button style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>
                    <Bell size={20} />
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{ textAlign: 'right' }}>
                        <p style={{ margin: 0, fontWeight: 600, color: 'var(--text-dark)', fontSize: '0.9rem' }}>{user?.name || "Guest"}</p>
                        <p style={{ margin: 0, fontSize: '0.8rem', textTransform: 'capitalize' }}>{user?.role || "Candidate"}</p>
                    </div>
                    <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--primary-dark)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <User size={20} color="var(--primary-light)" />
                    </div>
                    <button
                        onClick={handleLogout}
                        style={{ marginLeft: '1rem', padding: '0.4rem 0.8rem', fontSize: '0.8rem', borderRadius: '6px', background: 'var(--bg-lighter)', color: 'var(--text-muted)', border: '1px solid var(--border-color)', cursor: 'pointer' }}
                    >
                        Log Out
                    </button>
                </div>
            </div>
        </header>
    );
};

const Layout = () => {
    return (
        <div className="app-container">
            <Sidebar />
            <main className="main-content">
                <Topbar />
                <div className="view-content fade-in" style={{ animationDelay: '0.2s', flex: 1 }}>
                    <ErrorBoundary>
                        <Outlet />
                    </ErrorBoundary>
                </div>
            </main>
        </div>
    );
};

export default Layout;
