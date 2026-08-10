import { useQuery } from '@tanstack/react-query';
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
    BarChart, Bar
} from 'recharts';
import { Briefcase, Calendar, CheckCircle, TrendingUp } from 'lucide-react';
import AgentChat from '../components/AgentChat';

import api from '../api';

const fetchUserAnalytics = async () => {
    try {
        const { data } = await api.get('http://localhost:8000/dashboard/user-analytics');
        // Map the real backend response back into the frontend schema to avoid breaking UI layouts
        return {
            total_applications: data.analytics.applications_submitted || 0,
            interviews_scheduled: 0, // Implement dynamic interview counts later if needed
            offers_received: 0,
            rejection_rate: 0.0,
            resume_score: data.analytics.resume_score || 0,
            job_recommendations: data.recommendations || [],
            trends: [
                { month: 'Dynamic Data Live', applications: data.analytics.applications_submitted || 0, interviews: 0 },
            ]
        };
    } catch (e) {
        return {
            total_applications: 0,
            interviews_scheduled: 0,
            offers_received: 0,
            rejection_rate: 0,
            resume_score: 0,
            job_recommendations: [],
            trends: []
        };
    }
};

const StatCard = ({ title, value, icon, trend }: { title: string, value: string | number | undefined, icon: any, trend: string }) => (
    <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>{title}</p>
                <h3 style={{ fontSize: '1.75rem', margin: 0 }}>{value}</h3>
            </div>
            <div style={{ padding: '0.75rem', background: 'var(--glass-bg)', borderRadius: 'var(--radius-md)', color: 'var(--primary-light)' }}>
                {icon}
            </div>
        </div>
        <div style={{ marginTop: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.875rem' }}>
            <TrendingUp size={16} color="var(--success)" />
            <span style={{ color: 'var(--success)' }}>{trend}</span>
            <span style={{ color: 'var(--text-muted)' }}>vs last month</span>
        </div>
    </div>
);

const Dashboard = () => {
    const { data, isLoading } = useQuery({ queryKey: ['analytics'], queryFn: fetchUserAnalytics });

    if (isLoading) return <div style={{ padding: '2rem' }}>Loading dashboard data...</div>;

    return (
        <div style={{ paddingBottom: '2rem' }}>
            <div className="page-header">
                <h1 className="page-title">Career Overview</h1>
                <p>Welcome back! Here's how your job hunt is progressing.</p>
            </div>

            <div className="grid-4" style={{ marginBottom: '2rem' }}>
                <StatCard title="Total Applications" value={data?.total_applications} icon={<Briefcase />} trend="+12%" />
                <StatCard title="Interviews Scheduled" value={data?.interviews_scheduled} icon={<Calendar />} trend="+2" />
                <StatCard title="Offers Received" value={data?.offers_received} icon={<CheckCircle />} trend="+1" />
                <StatCard title="Response Rate" value={`${((1 - (data?.rejection_rate || 0)) * 100).toFixed(0)}%`} icon={<TrendingUp />} trend="+5%" />
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <AgentChat />
            </div>

            <div className="grid-2">
                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3>Application Activity</h3>
                    <p style={{ fontSize: '0.875rem', marginBottom: '1.5rem' }}>Your application volume over the last 4 months.</p>
                    <div style={{ height: '300px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data?.trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorApps" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--primary-color)" stopOpacity={0.8} />
                                        <stop offset="95%" stopColor="var(--primary-color)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                                <XAxis dataKey="month" stroke="var(--text-muted)" fontSize={12} tickLine={false} />
                                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                                <RechartsTooltip contentStyle={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
                                <Area type="monotone" dataKey="applications" stroke="var(--primary-light)" fillOpacity={1} fill="url(#colorApps)" strokeWidth={3} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="glass-panel" style={{ padding: '1.5rem' }}>
                    <h3>Interview Conversion</h3>
                    <p style={{ fontSize: '0.875rem', marginBottom: '1.5rem' }}>Applications leading to interviews.</p>
                    <div style={{ height: '300px' }}>
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data?.trends} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
                                <XAxis dataKey="month" stroke="var(--text-muted)" fontSize={12} tickLine={false} />
                                <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                                <RechartsTooltip cursor={{ fill: 'var(--bg-card-hover)' }} contentStyle={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-color)', borderRadius: '8px' }} />
                                <Bar dataKey="interviews" fill="var(--secondary-color)" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
