import { useState, useEffect } from 'react';
import { Search, MapPin, IndianRupee, Briefcase, Filter, ChevronRight, Bookmark, X } from 'lucide-react';
import api from '../api';

interface Job {
    id: string;
    title: string;
    description: string;
    location: string;
    salary_min: number;
    salary_max: number;
    posted_at: string;
    match_score?: number;
    company_name?: string;
    company_logo?: string;
    company_website?: string;
}

const Jobs = () => {
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [locationTerm, setLocationTerm] = useState('');
    const [page, setPage] = useState(0);
    const [tab, setTab] = useState<'all' | 'recommended'>('all');
    const [brokenLogos, setBrokenLogos] = useState<Record<string, boolean>>({});
    const [showFilters, setShowFilters] = useState(false);
    const [selectedJob, setSelectedJob] = useState<Job | null>(null);
    const [fetchingDetails, setFetchingDetails] = useState(false);

    const fetchJobs = async () => {
        setLoading(true);
        try {
            const limit = 10;
            const skip = page * limit;
            const url = tab === 'recommended' ? '/jobs/suggestions' : `/jobs/?skip=${skip}&limit=${limit}`;
            const res = await api.get(url, {
                baseURL: 'http://localhost:8000'
            });
            setJobs(res.data);
        } catch (error) {
            console.error("Failed to fetch jobs natively, reverting to empty state", error);
        } finally {
            setLoading(false);
        }
    };

    const handleApply = (job: Job) => {
        if (job.company_website) {
            window.open(job.company_website, '_blank', 'noopener,noreferrer');
        } else {
            window.open('https://google.com/careers', '_blank', 'noopener,noreferrer');
        }
    };

    const handleViewMore = async (job: Job) => {
        setSelectedJob(job);
        setFetchingDetails(true);
        try {
            const res = await api.get(`/jobs/${job.id}`, {
                baseURL: 'http://localhost:8000'
            });
            setSelectedJob(res.data);
        } catch (error) {
            console.error("Failed to load job details", error);
        } finally {
            setFetchingDetails(false);
        }
    };

    useEffect(() => {
        fetchJobs();
    }, [page, tab]);

    // Format currency helper
    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount);
    };

    // Clean description helper to strip HTML tags and limit snippet length
    const cleanDescription = (htmlStr: string) => {
        if (!htmlStr) return "";
        // Strip HTML tags using regex
        const cleanText = htmlStr.replace(/<[^>]*>/g, '');
        if (cleanText.length > 160) {
            return cleanText.substring(0, 160) + "...";
        }
        return cleanText;
    };

    // Filter jobs by search term (title, description, company) and location term
    const filteredJobs = jobs.filter(job => {
        const matchesSearch = !searchTerm ||
            job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            (job.description && job.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
            (job.company_name && job.company_name.toLowerCase().includes(searchTerm.toLowerCase()));

        const matchesLocation = !locationTerm ||
            (job.location && job.location.toLowerCase().includes(locationTerm.toLowerCase()));

        return matchesSearch && matchesLocation;
    });

    return (
        <div style={{ color: 'var(--text-light)', paddingBottom: '3rem' }}>
            {/* Header Section */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem', flexWrap: 'wrap', gap: '1.5rem' }}>
                <div>
                    <h1 style={{ marginBottom: '0.5rem', fontSize: '2.25rem', fontWeight: 800, letterSpacing: '-0.025em' }} className="text-gradient">
                        Job Board
                    </h1>
                    <p style={{ color: 'var(--text-muted)', margin: 0, fontSize: '1rem' }}>
                        Discover remote, hybrid, and technical opportunities mapped directly to your profile.
                    </p>
                </div>

                {/* Modern Toggle Tabs */}
                <div style={{ display: 'flex', gap: '0.25rem', background: 'rgba(30, 41, 59, 0.45)', padding: '6px', borderRadius: '12px', border: '1px solid rgba(255, 255, 255, 0.08)', backdropFilter: 'blur(12px)' }}>
                    <button
                        onClick={() => { setTab('all'); setPage(0); }}
                        style={{
                            padding: '0.625rem 1.5rem',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontWeight: 600,
                            fontSize: '0.875rem',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            background: tab === 'all' ? 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))' : 'transparent',
                            color: tab === 'all' ? '#fff' : 'var(--text-muted)',
                            boxShadow: tab === 'all' ? '0 4px 12px rgba(99, 102, 241, 0.35)' : 'none'
                        }}
                    >
                        All Listings
                    </button>
                    <button
                        onClick={() => { setTab('recommended'); setPage(0); }}
                        style={{
                            padding: '0.625rem 1.5rem',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontWeight: 600,
                            fontSize: '0.875rem',
                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
                            background: tab === 'recommended' ? 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))' : 'transparent',
                            color: tab === 'recommended' ? '#fff' : 'var(--text-muted)',
                            boxShadow: tab === 'recommended' ? '0 4px 12px rgba(99, 102, 241, 0.35)' : 'none'
                        }}
                    >
                        Recommended Matches
                    </button>
                </div>
            </div>

            {/* Glassmorphic Search and Filters Bar */}
            <div
                style={{
                    padding: '1.25rem',
                    display: 'flex',
                    gap: '1rem',
                    marginBottom: '1.5rem',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    background: 'rgba(30, 41, 59, 0.35)',
                    backdropFilter: 'blur(16px)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '16px',
                    boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.2)'
                }}
            >
                <div style={{ flex: 1, minWidth: '260px', position: 'relative' }}>
                    <Search style={{ position: 'absolute', left: '1.25rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} size={20} />
                    <input
                        type="text"
                        placeholder="Search job title, keywords, or company..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        style={{
                            width: '100%',
                            padding: '0.875rem 1rem 0.875rem 3.25rem',
                            borderRadius: '12px',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            background: 'rgba(15, 23, 42, 0.5)',
                            color: '#fff',
                            fontSize: '0.95rem',
                            outline: 'none',
                            transition: 'all 0.3s ease',
                            boxSizing: 'border-box'
                        }}
                    />
                </div>

                <div style={{ position: 'relative', width: '220px', minWidth: '150px' }}>
                    <MapPin style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} size={18} />
                    <input
                        type="text"
                        placeholder="Filter by location..."
                        value={locationTerm}
                        onChange={(e) => setLocationTerm(e.target.value)}
                        style={{
                            width: '100%',
                            padding: '0.875rem 1rem 0.875rem 2.75rem',
                            borderRadius: '12px',
                            border: '1px solid rgba(255, 255, 255, 0.08)',
                            background: 'rgba(15, 23, 42, 0.5)',
                            color: '#fff',
                            fontSize: '0.95rem',
                            outline: 'none',
                            transition: 'all 0.3s ease',
                            boxSizing: 'border-box'
                        }}
                    />
                </div>

                <button
                    onClick={() => setShowFilters(!showFilters)}
                    className="btn"
                    style={{
                        background: showFilters ? 'var(--primary-color)' : 'rgba(15, 23, 42, 0.5)',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        color: '#fff',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        padding: '0.875rem 1.5rem',
                        borderRadius: '12px',
                        cursor: 'pointer',
                        fontWeight: 600,
                        boxShadow: showFilters ? '0 4px 12px rgba(99, 102, 241, 0.3)' : 'none',
                        transition: 'all 0.3s'
                    }}
                >
                    <Filter size={18} /> Filter Options
                </button>

                <button
                    onClick={fetchJobs}
                    className="btn btn-primary"
                    style={{
                        padding: '0.875rem 2rem',
                        background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))',
                        border: 'none',
                        borderRadius: '12px',
                        fontWeight: 600,
                        boxShadow: '0 4px 14px rgba(99, 102, 241, 0.35)',
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                    }}
                >
                    Find Careers
                </button>
            </div>

            {/* Collapsible Filter Panel */}
            {showFilters && (
                <div
                    className="fade-in"
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
                        gap: '1.5rem',
                        marginBottom: '2rem',
                        padding: '1.5rem',
                        background: 'rgba(30, 41, 59, 0.35)',
                        borderRadius: '16px',
                        border: '1px solid rgba(255, 255, 255, 0.08)',
                        backdropFilter: 'blur(12px)',
                        boxShadow: '0 10px 25px -5px rgba(0,0,0,0.3)'
                    }}
                >
                    {/* Job Type Filter */}
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <h4 style={{ marginBottom: '1rem', fontSize: '0.95rem', fontWeight: 700, color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '0.5rem' }}>
                            Job Type
                        </h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Full-time
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Contract
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Freelance
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Internship
                            </label>
                        </div>
                    </div>

                    {/* Salary Filter */}
                    <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <h4 style={{ marginBottom: '1rem', fontSize: '0.95rem', fontWeight: 700, color: '#fff', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '0.5rem' }}>
                            Salary Range
                        </h4>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Under ₹50k
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> ₹50k - ₹100k
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> ₹100k - ₹150k
                            </label>
                            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', color: 'var(--text-light)', fontSize: '0.9rem' }}>
                                <input type="checkbox" style={{ accentColor: 'var(--primary-color)', width: '16px', height: '16px' }} /> Over ₹150k
                            </label>
                        </div>
                    </div>
                </div>
            )}

            {/* Main Listings Feed - Now full width since filter board is collapsible */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', width: '100%' }}>
                {loading ? (
                    <div style={{ textAlign: 'center', padding: '5rem' }}>
                        <div style={{ width: '45px', height: '45px', border: '3px solid rgba(99,102,241,0.15)', borderTopColor: 'var(--primary-color)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1.5rem auto' }}></div>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>Analyzing and matching careers...</p>
                    </div>
                ) : (
                    <>
                        {filteredJobs.length === 0 ? (
                            <div className="card fade-in" style={{ padding: '4rem 2rem', textAlign: 'center', background: 'rgba(30, 41, 59, 0.25)', border: '1px solid rgba(255,255,255,0.06)' }}>
                                <h3 style={{ marginBottom: '0.5rem', fontSize: '1.25rem' }}>
                                    {tab === 'recommended' ? 'No Recommended Matches' : 'No listings available'}
                                </h3>
                                <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', maxWidth: '520px', margin: '0 auto', lineHeight: '1.6' }}>
                                    {tab === 'recommended'
                                        ? 'Please upload a resume in the Resume Builder or update the skills in your profile to receive personalized job matches. We filter recommendations to only show roles that closely fit your qualifications.'
                                        : 'There are no roles matching your criteria at this time. Try refining your keywords or location.'}
                                </p>
                            </div>
                        ) : (
                            filteredJobs.map((job) => {
                                const isHighMatch = job.match_score !== undefined && job.match_score !== null && job.match_score > 70;
                                const hasLogo = job.company_logo && !brokenLogos[job.id];
                                return (
                                    <div
                                        key={job.id}
                                        className="card fade-in"
                                        style={{
                                            padding: '1.75rem',
                                            background: isHighMatch
                                                ? 'linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.03) 100%)'
                                                : 'rgba(30, 41, 59, 0.3)',
                                            backdropFilter: 'blur(12px)',
                                            border: isHighMatch
                                                ? '1.5px solid rgba(99, 102, 241, 0.45)'
                                                : '1.5px solid rgba(255, 255, 255, 0.08)',
                                            borderRadius: '16px',
                                            boxShadow: isHighMatch
                                                ? '0 8px 32px 0 rgba(99, 102, 241, 0.12), inset 0 1px 1px rgba(255, 255, 255, 0.05)'
                                                : '0 8px 32px 0 rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.02)',
                                            transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s, box-shadow 0.3s',
                                            cursor: 'pointer'
                                        }}
                                    >
                                        {/* Card Top Block */}
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.25rem' }}>
                                            <div style={{ display: 'flex', gap: '1.25rem' }}>
                                                {/* Company Logo Badge */}
                                                <div style={{
                                                    width: '52px',
                                                    height: '52px',
                                                    borderRadius: '12px',
                                                    background: hasLogo ? '#ffffff' : 'rgba(15, 23, 42, 0.6)',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    justifyContent: 'center',
                                                    overflow: 'hidden',
                                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                                    padding: '4px'
                                                }}>
                                                    {hasLogo ? (
                                                        <img
                                                            src={job.company_logo}
                                                            alt={job.company_name}
                                                            onError={() => setBrokenLogos(prev => ({ ...prev, [job.id]: true }))}
                                                            style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                                                        />
                                                    ) : (
                                                        <Briefcase size={22} style={{ color: 'var(--primary-color)' }} />
                                                    )}
                                                </div>
                                                <div>
                                                    <h3 style={{ margin: '0 0 0.35rem 0', fontSize: '1.2rem', display: 'flex', alignItems: 'center', gap: '0.625rem', fontWeight: 700, letterSpacing: '-0.01em' }}>
                                                        {job.title}
                                                        {job.match_score !== undefined && job.match_score !== null && (
                                                            <span
                                                                className="badge"
                                                                style={{
                                                                    fontSize: '0.75rem',
                                                                    background: job.match_score > 70 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                                                                    color: job.match_score > 70 ? 'var(--success)' : '#f59e0b',
                                                                    border: '1px solid currentColor',
                                                                    borderRadius: '20px',
                                                                    padding: '2px 10px',
                                                                    fontWeight: 600
                                                                }}
                                                            >
                                                                {job.match_score}% Match
                                                            </span>
                                                        )}
                                                    </h3>
                                                    <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.925rem', fontWeight: 500 }}>
                                                        {job.company_name || 'CareerOS Partner'}
                                                    </p>
                                                </div>
                                            </div>
                                            <button style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: '4px', transition: 'color 0.2s' }}>
                                                <Bookmark size={20} />
                                            </button>
                                        </div>

                                        {/* Job Description Summary */}
                                        <p style={{ color: 'var(--text-light)', fontSize: '0.95rem', lineHeight: '1.6', marginBottom: '1.75rem' }}>
                                            {cleanDescription(job.description)}
                                        </p>

                                        {/* Card Footer Block */}
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid rgba(255, 255, 255, 0.08)', paddingTop: '1.25rem' }}>
                                            {/* Capsule Badges */}
                                            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                                                {job.location && (
                                                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: '#a5b4fc', fontSize: '0.8rem', background: 'rgba(99, 102, 241, 0.12)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(99, 102, 241, 0.2)', fontWeight: 600 }}>
                                                        <MapPin size={14} /> {job.location}
                                                    </span>
                                                )}
                                                {(job.salary_min || job.salary_max) && (
                                                    <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: '#34d399', fontSize: '0.8rem', background: 'rgba(52, 211, 153, 0.12)', padding: '6px 12px', borderRadius: '20px', border: '1px solid rgba(52, 211, 153, 0.2)', fontWeight: 600 }}>
                                                        <IndianRupee size={14} />
                                                        {job.salary_min ? formatCurrency(job.salary_min) : ''}
                                                        {job.salary_min && job.salary_max ? ' - ' : ''}
                                                        {job.salary_max ? formatCurrency(job.salary_max) : ''}
                                                    </span>
                                                )}
                                            </div>

                                            {/* Action Buttons */}
                                            <div style={{ display: 'flex', gap: '0.75rem' }}>
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleViewMore(job);
                                                    }}
                                                    className="btn"
                                                    style={{
                                                        padding: '0.625rem 1.25rem',
                                                        fontSize: '0.875rem',
                                                        background: 'rgba(255, 255, 255, 0.05)',
                                                        border: '1px solid rgba(255, 255, 255, 0.1)',
                                                        borderRadius: '8px',
                                                        color: '#fff',
                                                        cursor: 'pointer',
                                                        transition: 'all 0.2s',
                                                        fontWeight: 600
                                                    }}
                                                >
                                                    View Details
                                                </button>
                                                <button
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        handleApply(job);
                                                    }}
                                                    className="btn btn-primary"
                                                    style={{
                                                        padding: '0.625rem 1.25rem',
                                                        fontSize: '0.875rem',
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        gap: '0.35rem',
                                                        background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))',
                                                        border: 'none',
                                                        borderRadius: '8px',
                                                        fontWeight: 600,
                                                        boxShadow: '0 4px 10px rgba(99,102,241,0.25)',
                                                        cursor: 'pointer',
                                                        transition: 'all 0.2s'
                                                    }}
                                                >
                                                    Apply Now <ChevronRight size={16} />
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })
                        )}

                        {/* Pagination Block */}
                        <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem', marginTop: '2.5rem' }}>
                            <button
                                className="btn"
                                disabled={page === 0}
                                onClick={() => setPage(p => p - 1)}
                                style={{
                                    background: 'rgba(30, 41, 59, 0.35)',
                                    color: page === 0 ? 'var(--text-muted)' : 'var(--text-light)',
                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                    padding: '0.75rem 1.5rem',
                                    borderRadius: '10px',
                                    cursor: page === 0 ? 'not-allowed' : 'pointer',
                                    transition: 'all 0.2s',
                                    fontWeight: 600
                                }}
                            >
                                Previous
                            </button>
                            <button
                                className="btn"
                                onClick={() => setPage(p => p + 1)}
                                style={{
                                    background: 'rgba(30, 41, 59, 0.35)',
                                    color: 'var(--text-light)',
                                    border: '1px solid rgba(255, 255, 255, 0.08)',
                                    padding: '0.75rem 1.5rem',
                                    borderRadius: '10px',
                                    cursor: 'pointer',
                                    transition: 'all 0.2s',
                                    fontWeight: 600
                                }}
                            >
                                Next Page
                            </button>
                        </div>
                    </>
                )}
            </div>

            {/* View Full Job Details Modal */}
            {selectedJob && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100vw',
                        height: '100vh',
                        background: 'rgba(15, 23, 42, 0.75)',
                        backdropFilter: 'blur(8px)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        zIndex: 1000,
                        padding: '1rem',
                        boxSizing: 'border-box'
                    }}
                    onClick={() => setSelectedJob(null)}
                >
                    <div
                        style={{
                            background: '#1e293b',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: '24px',
                            width: '100%',
                            maxWidth: '750px',
                            maxHeight: '85vh',
                            display: 'flex',
                            flexDirection: 'column',
                            overflow: 'hidden',
                            boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'
                        }}
                        onClick={e => e.stopPropagation()}
                    >
                        {/* Modal Header */}
                        <div style={{ padding: '2rem', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                <div>
                                    <h2 style={{ margin: '0 0 0.5rem 0', fontSize: '1.5rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }} className="text-gradient">
                                        {selectedJob.title}
                                        {selectedJob.match_score !== undefined && selectedJob.match_score !== null && (
                                            <span
                                                className="badge"
                                                style={{
                                                    fontSize: '0.75rem',
                                                    background: selectedJob.match_score > 70 ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                                                    color: selectedJob.match_score > 70 ? 'var(--success)' : '#f59e0b',
                                                    border: '1px solid currentColor',
                                                    borderRadius: '20px',
                                                    padding: '2px 10px',
                                                    fontWeight: 600,
                                                    textShadow: 'none',
                                                    letterSpacing: 'normal'
                                                }}
                                            >
                                                {selectedJob.match_score}% Match
                                            </span>
                                        )}
                                    </h2>
                                    <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '1rem', fontWeight: 600 }}>
                                        {selectedJob.company_name || 'CareerOS Partner'}
                                    </p>
                                </div>
                                <button
                                    style={{
                                        background: 'rgba(255,255,255,0.05)',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        borderRadius: '50%',
                                        color: 'var(--text-muted)',
                                        display: 'flex',
                                        alignItems: 'center',
                                        justifyContent: 'center',
                                        width: '36px',
                                        height: '36px',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s',
                                        outline: 'none'
                                    }}
                                    onClick={() => setSelectedJob(null)}
                                >
                                    <X size={18} />
                                </button>
                            </div>
                        </div>

                        {/* Modal Body */}
                        <div className="custom-scrollbar" style={{ padding: '2rem', overflowY: 'auto', flex: 1, color: 'var(--text-light)', lineHeight: '1.6', fontSize: '0.95rem' }}>
                            {fetchingDetails ? (
                                <div style={{ textAlign: 'center', padding: '4rem' }}>
                                    <div style={{ width: '40px', height: '40px', border: '3px solid rgba(99,102,241,0.15)', borderTopColor: 'var(--primary-color)', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1.5rem auto' }}></div>
                                    <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>Retrieving full description...</p>
                                </div>
                            ) : (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                                    {/* Metadata Pills */}
                                    <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                                        {selectedJob.location && (
                                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: '#a5b4fc', fontSize: '0.85rem', background: 'rgba(99, 102, 241, 0.12)', padding: '6px 14px', borderRadius: '20px', border: '1px solid rgba(99, 102, 241, 0.2)', fontWeight: 600 }}>
                                                <MapPin size={14} /> {selectedJob.location}
                                            </span>
                                        )}
                                        {(selectedJob.salary_min || selectedJob.salary_max) && (
                                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '0.35rem', color: '#34d399', fontSize: '0.85rem', background: 'rgba(52, 211, 153, 0.12)', padding: '6px 14px', borderRadius: '20px', border: '1px solid rgba(52, 211, 153, 0.2)', fontWeight: 600 }}>
                                                <IndianRupee size={14} />
                                                {selectedJob.salary_min ? formatCurrency(selectedJob.salary_min) : ''}
                                                {selectedJob.salary_min && selectedJob.salary_max ? ' - ' : ''}
                                                {selectedJob.salary_max ? formatCurrency(selectedJob.salary_max) : ''}
                                            </span>
                                        )}
                                    </div>

                                    {/* Full Description parsed content */}
                                    <div
                                        className="job-description-content"
                                        dangerouslySetInnerHTML={{ __html: selectedJob.description }}
                                        style={{
                                            color: '#e2e8f0',
                                            lineHeight: '1.7',
                                            fontSize: '0.975rem'
                                        }}
                                    />
                                </div>
                            )}
                        </div>

                        {/* Modal Footer */}
                        <div style={{ padding: '1.5rem 2rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', justifyContent: 'flex-end', gap: '1rem', background: 'rgba(15, 23, 42, 0.3)' }}>
                            <button
                                className="btn"
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    background: 'rgba(255,255,255,0.05)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    color: 'var(--text-light)',
                                    borderRadius: '10px',
                                    cursor: 'pointer',
                                    fontWeight: 600,
                                    transition: 'all 0.2s'
                                }}
                                onClick={() => setSelectedJob(null)}
                            >
                                Close Window
                            </button>
                            <button
                                className="btn btn-primary"
                                style={{
                                    padding: '0.75rem 2rem',
                                    background: 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))',
                                    border: 'none',
                                    borderRadius: '10px',
                                    color: '#fff',
                                    cursor: 'pointer',
                                    fontWeight: 600,
                                    boxShadow: '0 4px 12px rgba(99,102,241,0.3)',
                                    transition: 'all 0.2s'
                                }}
                                onClick={() => handleApply(selectedJob)}
                            >
                                Apply Externally
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Jobs;
