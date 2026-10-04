import React, { useState } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import TermsPage from './pages/TermsPage';
import StudentDashboard from './pages/StudentDashboard';
import AdminDashboard from './pages/AdminDashboard';
import PortfolioModal from './components/PortfolioModal';

export default function App() {
  const [currentPage, setCurrentPage] = useState('landing'); // 'landing' | 'login' | 'terms' | 'student' | 'admin'
  const [currentUser, setCurrentUser] = useState(null);
  const [isPortfolioOpen, setIsPortfolioOpen] = useState(false);
  const [initialAgreedTerms, setInitialAgreedTerms] = useState(false);

  // Restore session from localStorage on initial load
  React.useEffect(() => {
    try {
      const savedUser = localStorage.getItem('currentUser');
      const token = localStorage.getItem('token');
      const role = localStorage.getItem('role');
      if (token && savedUser) {
        const parsed = JSON.parse(savedUser);
        setCurrentUser(parsed);
      }
    } catch (e) {
      console.error('Session restore error:', e);
    }
  }, []);

  // Navigation handler with support for /dashboard routing
  const handleNavigate = (page, options = {}) => {
    if (options.agreed) {
      setInitialAgreedTerms(true);
    }
    if (page === '/dashboard' || page === 'dashboard') {
      const currentRole = localStorage.getItem('role') || currentUser?.role || 'student';
      if (currentRole.toLowerCase() === 'student') {
        setCurrentPage('student');
      } else {
        setCurrentPage('admin');
      }
    } else {
      setCurrentPage(page);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Login handler
  const handleLoginSuccess = (userData) => {
    setCurrentUser(userData);
    const userRole = (userData.role || localStorage.getItem('role') || 'student').toLowerCase();
    if (userRole === 'student') {
      setCurrentPage('student');
    } else {
      // 'teacher' or 'hod'
      setCurrentPage('admin');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Logout handler
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    localStorage.removeItem('currentUser');
    setCurrentUser(null);
    setCurrentPage('login');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="h-screen flex flex-col justify-between bg-[#F4F7F6] text-[#1E293B] overflow-x-hidden">
      {/* Global Institutional Header with 5 Logos */}
      <Header onNavigate={handleNavigate} currentPage={currentPage} />

      {/* Main Page Content Body (Centered vertically & scrollable if overflowing) */}
      <main className="flex-1 flex flex-col justify-center overflow-y-auto py-2">
        {currentPage === 'landing' && (
          <LandingPage onNavigate={handleNavigate} />
        )}

        {currentPage === 'login' && (
          <AuthPage
            onLoginSuccess={handleLoginSuccess}
            onNavigate={handleNavigate}
            initialAgreed={initialAgreedTerms}
          />
        )}

        {currentPage === 'terms' && (
          <TermsPage
            onNavigate={handleNavigate}
            onAccept={() => setInitialAgreedTerms(true)}
          />
        )}

        {currentPage === 'student' && (
          <StudentDashboard
            user={currentUser}
            onLogout={handleLogout}
          />
        )}

        {currentPage === 'admin' && (
          <AdminDashboard
            user={currentUser}
            onLogout={handleLogout}
          />
        )}
      </main>

      {/* Global Footer with Aneesh & Anne Developer Credits & Portfolio Trigger (Always Visible) */}
      <Footer
        onOpenPortfolio={() => setIsPortfolioOpen(true)}
        onNavigate={handleNavigate}
      />

      {/* Developer Portfolio Modal */}
      <PortfolioModal
        isOpen={isPortfolioOpen}
        onClose={() => setIsPortfolioOpen(false)}
      />
    </div>
  );

}
