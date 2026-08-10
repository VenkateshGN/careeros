import { useState, useRef, useEffect } from 'react';
import { UploadCloud, FileText, Trash2, Download, Eye } from 'lucide-react';
import api from '../api';

const Resumes = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [activeResumeUrl, setActiveResumeUrl] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Initial check if user has a resume (mocked query for isolated demo)
    useEffect(() => {
        // Here we would sync with user DB state if available to check current_user.resume_url
    }, []);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUploadClick = () => {
        fileInputRef.current?.click();
    };

    const handleSubmitUpload = async () => {
        if (!file) return;
        setUploading(true);
        const formData = new FormData();
        formData.append('resume', file);

        try {
            const res = await api.post('/resume/upload', formData, {
                baseURL: 'http://localhost:8000',
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            });
            setActiveResumeUrl(res.data.resume_url);
            setFile(null); // clear staging
        } catch (error) {
            console.error("Upload failed", error);
        } finally {
            setUploading(false);
        }
    };

    const handleDelete = async () => {
        try {
            await api.delete('/resume/', { baseURL: 'http://localhost:8000' });
            setActiveResumeUrl(null);
        } catch (error) {
            console.error("Delete failed");
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1 style={{ marginBottom: 0 }}>Resume Manager</h1>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
                {/* Drag & Drop Upload Zone */}
                <div className="card fade-in" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', height: '100%' }}>
                    <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Upload New Resume</h3>

                    <div
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        onClick={handleUploadClick}
                        style={{
                            flex: 1,
                            border: `2px dashed ${dragActive ? 'var(--primary-light)' : 'var(--border-color)'}`,
                            borderRadius: '12px',
                            background: dragActive ? 'rgba(99, 102, 241, 0.05)' : 'var(--bg-dark)',
                            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                            cursor: 'pointer', transition: 'all 0.2s ease', gap: '1rem', padding: '3rem 1rem'
                        }}
                    >
                        <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'rgba(99, 102, 241, 0.1)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                            <UploadCloud size={32} color="var(--primary-light)" />
                        </div>
                        <div style={{ textAlign: 'center' }}>
                            <p style={{ margin: '0 0 0.5rem 0', fontWeight: 600, fontSize: '1.1rem' }}>
                                {file ? file.name : "Click or drag resume to upload"}
                            </p>
                            <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                                PDF documents up to 5MB
                            </p>
                        </div>
                        <input
                            ref={fileInputRef}
                            type="file"
                            accept="application/pdf"
                            style={{ display: 'none' }}
                            onChange={handleFileChange}
                        />
                    </div>

                    <div style={{ marginTop: '1.5rem', display: 'flex', justifyContent: 'flex-end' }}>
                        <button
                            className="btn btn-primary"
                            onClick={(e) => { e.stopPropagation(); handleSubmitUpload(); }}
                            disabled={!file || uploading}
                        >
                            {uploading ? 'Processing AI Data...' : 'Upload & Parse Resume'}
                        </button>
                    </div>
                </div>

                {/* Resume History / Active File */}
                <div className="card fade-in" style={{ padding: '2rem', animationDelay: '0.1s' }}>
                    <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Active Document</h3>

                    {activeResumeUrl ? (
                        <div style={{ border: '1px solid var(--border-color)', borderRadius: '8px', background: 'var(--bg-dark)' }}>
                            <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.75rem', borderRadius: '8px' }}>
                                    <FileText size={24} color="var(--primary-color)" />
                                </div>
                                <div style={{ flex: 1 }}>
                                    <p style={{ margin: '0 0 0.25rem 0', fontWeight: 600 }}>resume_main.pdf</p>
                                    <p style={{ margin: 0, color: 'var(--success)', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                                        <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--success)', display: 'inline-block' }}></span>
                                        Parsed Successfully
                                    </p>
                                </div>
                            </div>
                            <div style={{ display: 'flex', padding: '0.5rem' }}>
                                <button style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--text-light)', padding: '0.75rem', cursor: 'pointer', display: 'flex', justifyContent: 'center', gap: '0.5rem', alignItems: 'center' }}>
                                    <Eye size={16} /> Preview
                                </button>
                                <a href={`http://localhost:8000/resume/download`} target="_blank" rel="noreferrer" style={{ flex: 1, textDecoration: 'none', background: 'transparent', border: 'none', color: 'var(--text-light)', padding: '0.75rem', cursor: 'pointer', display: 'flex', justifyContent: 'center', gap: '0.5rem', alignItems: 'center', borderLeft: '1px solid var(--border-color)' }}>
                                    <Download size={16} /> Download
                                </a>
                                <button onClick={handleDelete} style={{ flex: 1, background: 'transparent', border: 'none', color: 'var(--danger)', padding: '0.75rem', cursor: 'pointer', display: 'flex', justifyContent: 'center', gap: '0.5rem', alignItems: 'center', borderLeft: '1px solid var(--border-color)' }}>
                                    <Trash2 size={16} /> Delete
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
                            <FileText size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                            <p>No active resume on file.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Resumes;
