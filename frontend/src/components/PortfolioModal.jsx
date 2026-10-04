import React from 'react';
import { X, Hammer, Sparkles, UserCheck, Mail, Globe, Code } from 'lucide-react';


export default function PortfolioModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div className="pearl-card max-w-lg w-full p-6 relative overflow-hidden animate-scaleUp">
        {/* Close Button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-[#64748B] hover:text-[#1E293B] bg-slate-100 p-1.5 rounded-full hover:bg-slate-200 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-[#FDF2F8] text-[#DB2777] border border-[#FCE7F3] mb-3 shadow-xs">
            <Hammer className="w-7 h-7 animate-bounce" />
          </div>
          <span className="inline-block text-[11px] font-bold text-[#DB2777] bg-[#FCE7F3] px-3 py-1 rounded-full uppercase tracking-wider mb-1">
            Developer Portfolio
          </span>
          <h3 className="text-xl font-bold text-[#1E293B]">
            Portfolio Under Construction
          </h3>
          <p className="text-xs text-[#64748B] mt-1">
            This module is currently being finalized. Full showcases, interactive case studies, and engineering repositories will be live soon!
          </p>
        </div>

        {/* Developer Profiles Card */}
        <div className="space-y-3 mb-6">
          {/* Developer 1: Aneesh Kanna N */}
          <div className="p-3.5 rounded-xl bg-[#F8FAF9] border border-[#E2E8F0] flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-[#0D5C3A] text-white flex items-center justify-center font-bold text-sm">
                AK
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#1E293B]">ANEESH KANNA N</h4>
                <p className="text-xs text-[#0D5C3A] font-medium">Lead Developer & Full-Stack Architect</p>
                <p className="text-[11px] text-[#64748B]">B.Tech Information Technology, PSNA CET</p>
              </div>
            </div>
            <div className="flex items-center space-x-1.5 text-[#64748B]">
              <span className="text-[10px] bg-[#ECFDF5] text-[#0D5C3A] font-semibold px-2 py-0.5 rounded border border-[#A7F3D0]">
                Active
              </span>
            </div>
          </div>

          {/* Developer 2: Anne Benilda A */}
          <div className="p-3.5 rounded-xl bg-[#FDF2F8] border border-[#FCE7F3] flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-[#DB2777] text-white flex items-center justify-center font-bold text-sm">
                AB
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#1E293B]">ANNE BENILDA A</h4>
                <p className="text-xs text-[#DB2777] font-medium">Co-Developer & Systems Engineering</p>
                <p className="text-[11px] text-[#64748B]">B.Tech Information Technology, PSNA CET</p>
              </div>
            </div>
            <div className="flex items-center space-x-1.5 text-[#64748B]">
              <span className="text-[10px] bg-[#FDF2F8] text-[#DB2777] font-semibold px-2 py-0.5 rounded border border-[#FCE7F3]">
                Active
              </span>
            </div>
          </div>
        </div>

        {/* System Declaration Note */}
        <div className="bg-[#F0F9FF] border border-[#BAE6FD] p-3 rounded-lg text-xs text-[#0369A1] mb-5">
          <p className="font-semibold flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-[#0EA5E9]" />
            Official Platform Ownership
          </p>
          <p className="text-[11px] mt-0.5 text-[#0284C7]">
            Designed and engineered for the Department of Information Technology at PSNA College of Engineering and Technology, Dindigul.
          </p>
        </div>

        {/* Action Button */}
        <button
          onClick={onClose}
          className="w-full py-2.5 px-4 btn-emerald rounded-lg text-sm font-semibold flex items-center justify-center space-x-2"
        >
          <span>Understood & Close</span>
        </button>
      </div>
    </div>
  );
}
