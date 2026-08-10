import { BookOpen, Star, Clock, Trophy } from 'lucide-react';

const courses = [
    { title: "Advanced React Patterns", provider: "Internal", duration: "4 hours", progress: 65, popular: true },
    { title: "System Design Fundamentals", provider: "Internal", duration: "6 hours", progress: 0, popular: true },
    { title: "Mastering FastAPI", provider: "Internal", duration: "5 hours", progress: 100, popular: false },
];

const CourseCard = ({ course }: { course: { title: string, provider: string, duration: string, progress: number, popular: boolean } }) => (
    <div className="card" style={{ position: 'relative', display: 'flex', flexDirection: 'column' }}>
        {course.popular && (
            <span className="badge badge-warning" style={{ position: 'absolute', top: '1rem', right: '1rem', display: 'flex', gap: '0.25rem' }}>
                <Star size={12} /> Popular
            </span>
        )}
        <div style={{ marginBottom: '1rem', width: '48px', height: '48px', borderRadius: '12px', background: 'var(--glass-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <BookOpen size={24} className="text-gradient" />
        </div>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>{course.title}</h3>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}><Trophy size={14} /> {course.provider}</span>
            <span style={{ display: 'flex', alignItems: 'center', gap: '0.25rem' }}><Clock size={14} /> {course.duration}</span>
        </div>

        <div style={{ marginTop: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                <span>Progress</span>
                <span style={{ fontWeight: 600 }}>{course.progress}%</span>
            </div>
            <div style={{ width: '100%', height: '6px', background: 'var(--bg-card-hover)', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ width: `${course.progress}%`, height: '100%', background: course.progress === 100 ? 'var(--success)' : 'linear-gradient(90deg, var(--primary-color), var(--primary-light))', borderRadius: '4px' }}></div>
            </div>
        </div>
    </div>
);

const LearningHub = () => {
    return (
        <div style={{ paddingBottom: '2rem' }}>
            <div className="page-header">
                <h1 className="page-title">Learning Hub</h1>
                <p>Upskill smartly. Follow recommended pathways based on your interview feedback.</p>
            </div>

            <div style={{ marginBottom: '2rem', display: 'flex', gap: '1rem' }}>
                <button className="btn-primary">My Courses</button>
                <button className="btn-secondary">Browse Catalog</button>
                <button className="btn-secondary">Certifications</button>
            </div>

            <div className="grid-3">
                {courses.map((c, i) => (
                    <CourseCard key={i} course={c} />
                ))}
            </div>
        </div>
    );
};

export default LearningHub;
