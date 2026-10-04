import React, { useState, useEffect } from 'react';
import { X, Mail, KeyRound, CheckCircle2, ArrowRight, RefreshCw, AlertCircle } from 'lucide-react';

export default function OtpModal({ isOpen, onClose, initialEmail = '' }) {
  const [step, setStep] = useState(1); // 1: Enter Email, 2: Enter OTP, 3: Success
  const [email, setEmail] = useState(initialEmail);
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [timer, setTimer] = useState(300); // 5 mins in seconds
  const [generatedOtp, setGeneratedOtp] = useState('');
  const [error, setError] = useState('');
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (initialEmail) setEmail(initialEmail);
  }, [initialEmail]);

  useEffect(() => {
    let interval = null;
    if (step === 2 && timer > 0) {
      interval = setInterval(() => setTimer(t => t - 1), 1000);
    }
    return () => clearInterval(interval);
  }, [step, timer]);

  if (!isOpen) return null;

  const handleSendOtp = (e) => {
    e.preventDefault();
    if (!email || !email.includes('@')) {
      setError('Please provide a valid institutional email address.');
      return;
    }
    setError('');
    setIsSending(true);

    // Simulate OTP generation & SMTP dispatch
    setTimeout(() => {
      const mockOtp = Math.floor(100000 + Math.random() * 900000).toString();
      setGeneratedOtp(mockOtp);
      setIsSending(false);
      setStep(2);
      setTimer(300);
    }, 900);
  };

  const handleOtpChange = (val, idx) => {
    if (val.length > 1) val = val[0];
    const newOtp = [...otp];
    newOtp[idx] = val;
    setOtp(newOtp);

    // Focus next input automatically
    if (val && idx < 5) {
      const nextInput = document.getElementById(`otp-box-${idx + 1}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handleVerifyAndReset = (e) => {
    e.preventDefault();
    const entered = otp.join('');
    if (entered !== generatedOtp && entered !== '123456') {
      setError(`Invalid OTP code entered. (For testing preview: use ${generatedOtp || '123456'})`);
      return;
    }
    if (newPassword.length < 8) {
      setError('New password must be at least 8 characters long.');
      return;
    }
    if (!/\d/.test(newPassword) || !/[!@#$%^&*]/.test(newPassword)) {
      setError('Password must contain at least 1 number and 1 special symbol (!@#$%^&*).');
      return;
    }
    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setError('');
    setStep(3);
  };

  const formatTimer = () => {
    const mins = Math.floor(timer / 60);
    const secs = timer % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div className="pearl-card max-w-md w-full p-6 relative overflow-hidden animate-scaleUp">
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-[#64748B] hover:text-[#1E293B] bg-slate-100 p-1.5 rounded-full hover:bg-slate-200 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Step 1: Request OTP */}
        {step === 1 && (
          <div>
            <div className="text-center mb-5">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-[#F0F9FF] text-[#0EA5E9] mb-3 shadow-xs">
                <Mail className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[#1E293B]">Reset Account Password</h3>
              <p className="text-xs text-[#64748B] mt-1">
                Enter your registered college email. We will send a secure 6-digit OTP verification code.
              </p>
            </div>

            {error && (
              <div className="mb-4 p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSendOtp} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-[#475569] mb-1">
                  Registered Email Address
                </label>
                <input
                  type="email"
                  required
                  placeholder="e.g. 713821104001@psnacet.edu.in"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full input-field"
                />
              </div>

              <button
                type="submit"
                disabled={isSending}
                className="w-full py-2.5 px-4 btn-emerald rounded-lg text-sm font-semibold flex items-center justify-center gap-2"
              >
                {isSending ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    <span>Sending Code...</span>
                  </>
                ) : (
                  <>
                    <span>Send Verification Code</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          </div>
        )}

        {/* Step 2: Enter OTP & New Password */}
        {step === 2 && (
          <div>
            <div className="text-center mb-5">
              <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-[#ECFDF5] text-[#0D5C3A] mb-3 shadow-xs">
                <KeyRound className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-[#1E293B]">Enter 6-Digit OTP</h3>
              <p className="text-xs text-[#64748B] mt-1">
                A verification code was sent to <strong className="text-[#1E293B]">{email}</strong>.
              </p>
              {generatedOtp && (
                <div className="mt-2 py-1 px-3 bg-[#FDF2F8] border border-[#FCE7F3] rounded-md inline-block text-[11px] text-[#DB2777] font-semibold">
                  Preview OTP: <span className="font-mono text-xs font-black">{generatedOtp}</span>
                </div>
              )}
            </div>

            {error && (
              <div className="mb-4 p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg flex items-center gap-1.5">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleVerifyAndReset} className="space-y-4">
              {/* OTP Digits */}
              <div>
                <label className="block text-xs font-semibold text-[#475569] mb-2 text-center">
                  Verification Code (Expires in {formatTimer()})
                </label>
                <div className="flex justify-center space-x-2">
                  {otp.map((digit, idx) => (
                    <input
                      key={idx}
                      id={`otp-box-${idx}`}
                      type="text"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleOtpChange(e.target.value, idx)}
                      className="w-10 h-12 text-center text-lg font-mono font-bold border border-[#CBD5E1] rounded-lg focus:border-[#0EA5E9] focus:ring-2 focus:ring-[#0EA5E9]/20 outline-none bg-white text-[#1E293B]"
                    />
                  ))}
                </div>
              </div>

              {/* New Password */}
              <div>
                <label className="block text-xs font-semibold text-[#475569] mb-1">
                  New Password (min. 8 chars, 1 num, 1 symbol)
                </label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="w-full input-field"
                />
              </div>

              {/* Confirm New Password */}
              <div>
                <label className="block text-xs font-semibold text-[#475569] mb-1">
                  Confirm New Password
                </label>
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full input-field"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2.5 px-4 btn-emerald rounded-lg text-sm font-semibold flex items-center justify-center gap-2"
              >
                <span>Verify & Reset Password</span>
              </button>

              <div className="text-center pt-1">
                <button
                  type="button"
                  onClick={handleSendOtp}
                  className="text-xs text-[#0EA5E9] hover:underline font-medium"
                >
                  Didn't receive the email? Resend code
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Step 3: Success Screen */}
        {step === 3 && (
          <div className="text-center py-4">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-[#ECFDF5] text-[#0D5C3A] mb-3">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="text-lg font-bold text-[#1E293B]">Password Reset Successfully!</h3>
            <p className="text-xs text-[#64748B] mt-1 mb-5">
              Your institutional account credentials have been updated securely. You can now log in.
            </p>
            <button
              onClick={() => {
                onClose();
                setStep(1);
              }}
              className="w-full py-2.5 px-4 btn-emerald rounded-lg text-sm font-semibold"
            >
              Back to Login
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
