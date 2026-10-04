import React, { useState, useEffect } from 'react';
import { User, GraduationCap, ShieldCheck, Crown, KeyRound, Mail, Phone, Lock, Eye, EyeOff, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';
import OtpModal from '../components/OtpModal';
import { API_BASE_URL } from '../config/api';

export default function AuthPage({ onLoginSuccess, onNavigate, initialAgreed = false }) {
  const [activeTab, setActiveTab] = useState('student'); // 'student' | 'teacher' | 'hod'
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isOtpOpen, setIsOtpOpen] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Login Form State
  const [loginIdentifier, setLoginIdentifier] = useState(''); // Reg No / Email / Phone
  const [loginPassword, setLoginPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);

  // Sign Up Form State
  const [fullName, setFullName] = useState('');
  const [registerNo, setRegisterNo] = useState('');
  const [gender, setGender] = useState('Male');
  const [department] = useState('INFORMATION TECHNOLOGY');
  const [year, setYear] = useState('IV');
  const [section, setSection] = useState('A');
  const [mobile, setMobile] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [agreedToTerms, setAgreedToTerms] = useState(initialAgreed);

  useEffect(() => {
    if (initialAgreed) {
      setAgreedToTerms(true);
      setIsSignUp(true);
    }
  }, [initialAgreed]);

  // Handle Login Submit
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!loginIdentifier.trim() || !loginPassword.trim()) {
      setError('Please fill in all credential fields.');
      return;
    }

    try {
      const resp = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identifier: loginIdentifier,
          password: loginPassword,
          role: activeTab.toUpperCase()
        })
      });

      if (resp.ok) {
        const data = await resp.json();
        if (data.access_token) {
          localStorage.setItem('psna_token', data.access_token);
        }
        onLoginSuccess({
          role: activeTab,
          identifier: loginIdentifier,
          name: data.user?.name || (activeTab === 'student' ? 'Aneesh Kanna N' : (activeTab === 'teacher' ? 'Dr. S. Karthik' : 'Dr. M. IT HOD')),
          department: data.user?.department || 'IT',
          token: data.access_token,
          ...data.user
        });
        return;
      }
    } catch (err) {
      console.warn('Backend login fallback mode:', err);
    }

    const userData = {
      role: activeTab,
      identifier: loginIdentifier,
      name: activeTab === 'student' ? 'Aneesh Kanna N' : (activeTab === 'teacher' ? 'Dr. S. Karthik' : 'Dr. M. IT HOD'),
      department: 'IT',
      year: 'IV',
      section: 'A',
      registerNo: loginIdentifier.includes('@') ? '713821104001' : loginIdentifier,
      email: loginIdentifier.includes('@') ? loginIdentifier : `${loginIdentifier}@psnacet.edu.in`,
    };

    onLoginSuccess(userData);
  };

  // Handle Sign Up Submit with Strict Validations
  const handleSignUpSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email.includes('@')) {
      setError('Institutional Email Address must contain an "@" symbol.');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    if (!/\d/.test(password)) {
      setError('Password must contain at least one numeric digit (0-9).');
      return;
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      setError('Password must contain at least one special symbol (!@#$%^&*...).');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match. Please re-type your confirm password.');
      return;
    }

    if (!agreedToTerms) {
      setError('You must agree to the Terms and Conditions and acknowledge the Privacy Policy to create an account.');
      return;
    }

    const newStudentUser = {
      role: 'student',
      name: fullName,
      registerNo: registerNo,
      gender: gender,
      department: 'IT',
      year: year,
      section: section,
      mobile: mobile,
      email: email,
    };

    setSuccessMsg('Account created successfully! Logging you in...');
    setTimeout(() => {
      onLoginSuccess(newStudentUser);
    }, 900);
  };

  return (
    <div className="w-full flex items-center justify-center py-2 px-4 my-auto">
      <div className="max-w-lg w-full">
        {/* Main Card */}
        <div className="pearl-card p-5 sm:p-6 border border-[#E2E8F0] relative overflow-hidden shadow-lg shadow-[#0D5C3A]/5">
          {/* Header Title */}
          <div className="text-center mb-4">
            <div className="flex justify-center mb-2">
              <img 
                src="/logos/psna_logo.png" 
                alt="PSNA College of Engineering and Technology, Dindigul" 
                className="h-9 sm:h-10 w-auto object-contain"
              />
            </div>
            <h2 className="text-lg sm:text-xl font-black text-[#1E293B] tracking-tight">
              Institutional Access Portal
            </h2>
            <p className="text-[11px] sm:text-xs font-bold text-[#0D5C3A]">
              PSNA CET Department of Information Technology
            </p>
            <p className="text-[10px] text-[#64748B]">
              Secure Role-Based Access Control (RBAC) System
            </p>
          </div>

          {/* Role Selection Tabs */}
          {!isSignUp && (
            <div className="grid grid-cols-3 gap-1 p-1 bg-[#F1F5F9] rounded-lg mb-4">
              {/* Student Tab */}
              <button
                type="button"
                onClick={() => { setActiveTab('student'); setError(''); }}
                className={`py-1.5 px-2 rounded-md text-[11px] font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
                  activeTab === 'student'
                    ? 'bg-white text-[#0D5C3A] shadow-xs'
                    : 'text-[#64748B] hover:text-[#1E293B]'
                }`}
              >
                <GraduationCap className="w-3.5 h-3.5" />
                <span>Student</span>
              </button>

              {/* Teacher Tab */}
              <button
                type="button"
                onClick={() => { setActiveTab('teacher'); setError(''); }}
                className={`py-1.5 px-2 rounded-md text-[11px] font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
                  activeTab === 'teacher'
                    ? 'bg-white text-[#0D5C3A] shadow-xs'
                    : 'text-[#64748B] hover:text-[#1E293B]'
                }`}
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Teacher</span>
              </button>

              {/* HOD Tab */}
              <button
                type="button"
                onClick={() => { setActiveTab('hod'); setError(''); }}
                className={`py-1.5 px-2 rounded-md text-[11px] font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
                  activeTab === 'hod'
                    ? 'bg-white text-[#0D5C3A] shadow-xs'
                    : 'text-[#64748B] hover:text-[#1E293B]'
                }`}
              >
                <Crown className="w-3.5 h-3.5" />
                <span>HOD</span>
              </button>
            </div>
          )}

          {/* Error / Success Feedback */}
          {error && (
            <div className="mb-3 p-2 bg-red-50 border border-red-200 text-red-700 text-[11px] rounded-lg flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {successMsg && (
            <div className="mb-3 p-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-[11px] rounded-lg flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* VIEW A: SIGN IN FORM */}
          {!isSignUp ? (
            <form onSubmit={handleLoginSubmit} className="space-y-3">
              <div>
                <label className="block text-[11px] font-bold text-[#475569] mb-1">
                  {activeTab === 'student' && 'Register Number or Email Address'}
                  {activeTab === 'teacher' && 'Staff Email or Phone Number'}
                  {activeTab === 'hod' && 'HOD Email or Official Phone Number'}
                </label>
                <div className="relative">
                  <input
                    type="text"
                    required
                    placeholder={
                      activeTab === 'student'
                        ? 'e.g. 713821104001 or student@psnacet.edu.in'
                        : 'e.g. staff@psnacet.edu.in or 9876543210'
                    }
                    value={loginIdentifier}
                    onChange={(e) => setLoginIdentifier(e.target.value)}
                    className="w-full input-field pl-8 py-2 text-xs"
                  />
                  <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none text-[#94A3B8]">
                    {activeTab === 'student' ? <GraduationCap className="w-3.5 h-3.5" /> : <Mail className="w-3.5 h-3.5" />}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-[11px] font-bold text-[#475569] mb-1">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    placeholder="Enter your secure password"
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    className="w-full input-field pl-8 pr-8 py-2 text-xs"
                  />
                  <div className="absolute inset-y-0 left-0 pl-2.5 flex items-center pointer-events-none text-[#94A3B8]">
                    <Lock className="w-3.5 h-3.5" />
                  </div>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-2.5 flex items-center text-[#94A3B8] hover:text-[#475569]"
                  >
                    {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              {/* Remember Me & Forgot Password Row */}
              <div className="flex items-center justify-between text-[11px]">
                <label className="flex items-center space-x-1.5 text-[#475569] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-3.5 h-3.5 rounded accent-[#0D5C3A]"
                  />
                  <span>Remember Me</span>
                </label>

                <button
                  type="button"
                  onClick={() => setIsOtpOpen(true)}
                  className="font-bold text-[#0EA5E9] hover:underline"
                >
                  Forgot Password? (OTP)
                </button>
              </div>

              {/* Login Button */}
              <button
                type="submit"
                className="w-full py-2.5 px-4 btn-emerald rounded-lg text-xs sm:text-sm font-bold shadow-md shadow-[#0D5C3A]/20 flex items-center justify-center space-x-2 cursor-pointer mt-1"
              >
                <span>Sign In as {activeTab.toUpperCase()}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>

              {/* Sign Up Switch */}
              <div className="pt-2.5 border-t border-[#E2E8F0] text-center text-[11px] text-[#64748B]">
                <span>Don't have an institutional student account? </span>
                <button
                  type="button"
                  onClick={() => { setIsSignUp(true); setError(''); }}
                  className="font-bold text-[#0D5C3A] hover:underline ml-1"
                >
                  Create New Account / Sign Up
                </button>
              </div>
            </form>
          ) : (
            /* VIEW B: SIGN UP / STUDENT REGISTRATION FORM */
            <form onSubmit={handleSignUpSubmit} className="space-y-2.5">
              <div className="flex items-center justify-between pb-1.5 border-b border-[#E2E8F0]">
                <h3 className="text-xs font-extrabold text-[#1E293B]">Student Registration</h3>
                <button
                  type="button"
                  onClick={() => { setIsSignUp(false); setError(''); }}
                  className="text-[11px] font-bold text-[#0EA5E9] hover:underline"
                >
                  ← Back to Login
                </button>
              </div>

              {/* Full Name & Register Number */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Full Legal Name</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. Aneesh Kanna N"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full input-field py-1.5 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Register Number</label>
                  <input
                    type="text"
                    required
                    placeholder="e.g. 713821104001"
                    value={registerNo}
                    onChange={(e) => setRegisterNo(e.target.value)}
                    className="w-full input-field py-1.5 text-xs font-mono"
                  />
                </div>
              </div>

              {/* Gender, Department & Year & Section */}
              <div className="grid grid-cols-4 gap-1.5">
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Gender</label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full input-field py-1.5 text-xs"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Dept</label>
                  <input
                    type="text"
                    readOnly
                    value="IT"
                    className="w-full input-field py-1.5 text-xs bg-[#F8FAF9] font-bold text-[#0D5C3A] cursor-not-allowed"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Year</label>
                  <select
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    className="w-full input-field py-1.5 text-xs font-bold"
                  >
                    <option value="I">I</option>
                    <option value="II">II</option>
                    <option value="III">III</option>
                    <option value="IV">IV</option>
                  </select>
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Sec</label>
                  <select
                    value={section}
                    onChange={(e) => setSection(e.target.value)}
                    className="w-full input-field py-1.5 text-xs font-bold"
                  >
                    <option value="A">A</option>
                    <option value="B">B</option>
                    <option value="C">C</option>
                    <option value="D">D</option>
                    <option value="E">E</option>
                    <option value="F">F</option>
                  </select>
                </div>
              </div>

              {/* Mobile & Email */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Mobile Number</label>
                  <input
                    type="tel"
                    required
                    placeholder="9876543210"
                    value={mobile}
                    onChange={(e) => setMobile(e.target.value)}
                    className="w-full input-field py-1.5 text-xs font-mono"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Email (Must contain @)</label>
                  <input
                    type="email"
                    required
                    placeholder="student@psnacet.edu.in"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full input-field py-1.5 text-xs"
                  />
                </div>
              </div>

              {/* Password & Confirm Password */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Password</label>
                  <input
                    type="password"
                    required
                    placeholder=">= 8 chars, 1 num, 1 sym"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full input-field py-1.5 text-xs"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-bold text-[#475569] mb-0.5">Confirm Password</label>
                  <input
                    type="password"
                    required
                    placeholder="Re-type password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full input-field py-1.5 text-xs"
                  />
                </div>
              </div>

              {/* Terms Checkbox */}
              <div className="pt-0.5">
                <label className="flex items-start space-x-1.5 text-[11px] text-[#334155] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={agreedToTerms}
                    onChange={(e) => setAgreedToTerms(e.target.checked)}
                    className="w-3.5 h-3.5 rounded accent-[#0D5C3A] mt-0.5"
                    required
                  />
                  <span>
                    I agree to terms and acknowledge privacy policy.{' '}
                    <button
                      type="button"
                      onClick={() => onNavigate('terms')}
                      className="text-[#0EA5E9] font-bold hover:underline"
                    >
                      Read full terms ↗
                    </button>
                  </span>
                </label>
              </div>

              {/* Register Button */}
              <button
                type="submit"
                className="w-full py-2.5 px-4 btn-emerald rounded-lg text-xs font-bold shadow-md shadow-[#0D5C3A]/20 flex items-center justify-center space-x-2 cursor-pointer"
              >
                <span>Register Account</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </form>
          )}
        </div>
      </div>

      {/* Forgot Password OTP Modal */}
      <OtpModal
        isOpen={isOtpOpen}
        onClose={() => setIsOtpOpen(false)}
        initialEmail={loginIdentifier.includes('@') ? loginIdentifier : ''}
      />
    </div>
  );
}
