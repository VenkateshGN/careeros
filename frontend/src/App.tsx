import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useUserStore } from './store';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import ResetPassword from './pages/ResetPassword';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import CoverLetters from './pages/CoverLetters';
import Resumes from './pages/Resumes';
import Interviews from './pages/Interviews';
import LearningHub from './pages/LearningHub';
import JobMatching from './pages/JobMatching';
import CareerCoach from './pages/CareerCoach';
import Jobs from './pages/Jobs';
import RecruiterDashboard from './pages/RecruiterDashboard';

const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { user } = useUserStore();
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />

        <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="jobs" element={<Jobs />} />
          <Route path="profile" element={<Profile />} />
          <Route path="resumes" element={<Resumes />} />
          <Route path="cover-letters" element={<CoverLetters />} />
          <Route path="interviews" element={<Interviews />} />
          <Route path="learning" element={<LearningHub />} />
          <Route path="job-matching" element={<JobMatching />} />
          <Route path="career-coach" element={<CareerCoach />} />
          <Route path="recruiter" element={<RecruiterDashboard />} />
        </Route>
      </Routes>
      <Toaster position="top-right" toastOptions={{ style: { background: 'var(--bg-lighter)', color: 'var(--text-light)', border: '1px solid var(--border-color)' } }} />
    </BrowserRouter>
  );
}

export default App;
