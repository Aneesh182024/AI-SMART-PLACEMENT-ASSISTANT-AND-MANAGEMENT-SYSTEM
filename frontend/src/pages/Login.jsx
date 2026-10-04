import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, AlertCircle, Eye, EyeOff, LogIn, ArrowRight } from 'lucide-react';
import { API_BASE_URL } from '../config/api';

/**
 * Login Component - PSNA IT Smart Placement Assistant
 * Strictly validates credentials against backend database (PostgreSQL / FastAPI).
 * Stores returned role and token in localStorage and navigates to /dashboard on HTTP 200.
 * Displays backend HTTP 401 detail error dynamically in red below the form header.
 */
export default function Login({ onLoginSuccess, onNavigate }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Optional react-router-dom hook
  let navigate = null;
  try {
    navigate = useNavigate();
  } catch (err) {
    // Graceful fallback if component is rendered outside BrowserRouter
    navigate = null;
  }

  // Intercept standard submission and validate strictly against backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    const emailVal = email.trim();
    const passVal = password.trim();

    if (!emailVal || !passVal) {
      setError('Please provide both institutional email and password.');
      setIsLoading(false);
      return;
    }

    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || API_BASE_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: emailVal,
          password: passVal,
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok && response.status === 200) {
        // Save returned role and token in localStorage
        const token = data.token || data.access_token;
        const role = data.role || data.user?.role || 'student';

        localStorage.setItem('token', token);
        localStorage.setItem('role', role);
        localStorage.setItem('currentUser', JSON.stringify(data.user || data));

        // Invoke callbacks if provided
        if (onLoginSuccess) {
          onLoginSuccess(data.user || { role, token, email: emailVal });
        }

        // Navigate to /dashboard
        if (navigate) {
          navigate('/dashboard');
        } else if (onNavigate) {
          onNavigate('/dashboard');
        } else {
          window.location.href = '/dashboard';
        }
        return;
      }

      // On HTTP 401 or other errors: capture specific backend error details
      const errorDetail = data.detail || data.message || 'Invalid Email or Password! Account illai endral register seiyavum.';
      setError(errorDetail);
    } catch (networkErr) {
      console.error('Login network error:', networkErr);
      setError('Network connection error! Unable to reach backend server. Please verify backend is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-2xl shadow-xl border border-slate-200">
      {/* Form Header */}
      <div className="text-center mb-6">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-emerald-50 text-[#0D5C3A] mb-3">
          <LogIn className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-800">Sign In to Placement Portal</h2>
        <p className="text-xs text-slate-500 mt-1">
          PSNA College of Engineering and Technology &bull; Department of IT
        </p>
      </div>

      {/* Dynamic Red Error Banner Below Form Header */}
      {error && (
        <div 
          id="login-error-message"
          className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 text-xs font-semibold rounded-lg flex items-center gap-2 animate-shake"
        >
          <AlertCircle className="w-4 h-4 shrink-0 text-red-600" />
          <span>{error}</span>
        </div>
      )}

      {/* Login Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Email Field */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            Institutional Email Address
          </label>
          <div className="relative">
            <Mail className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type="email"
              id="login-email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. 713821104001@psnacet.edu.in or staff@psnacet.edu.in"
              className="w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#0D5C3A] focus:border-transparent outline-none transition-all"
            />
          </div>
        </div>

        {/* Password Field */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 mb-1">
            Password
          </label>
          <div className="relative">
            <Lock className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
            <input
              type={showPassword ? 'text' : 'password'}
              id="login-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your confidential password"
              className="w-full pl-9 pr-10 py-2 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-[#0D5C3A] focus:border-transparent outline-none transition-all"
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600 transition-colors"
            >
              {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          id="login-submit-btn"
          disabled={isLoading}
          className="w-full py-2.5 px-4 bg-[#0D5C3A] hover:bg-[#0A472D] text-white text-xs font-bold rounded-lg shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
        >
          {isLoading ? (
            <span>Verifying Credentials...</span>
          ) : (
            <>
              <span>Sign In</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
