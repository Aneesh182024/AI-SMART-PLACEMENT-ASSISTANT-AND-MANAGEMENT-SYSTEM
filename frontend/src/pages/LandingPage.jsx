import React, { useState } from 'react';
import { ArrowRight, Lock, Sparkles, Database, FileSpreadsheet, Bot, ShieldCheck, CheckCircle } from 'lucide-react';

export default function LandingPage({ onNavigate }) {
  const [department] = useState('INFORMATION TECHNOLOGY');

  return (
    <div className="w-full flex items-center justify-center py-2 px-4 my-auto">
      <div className="max-w-lg w-full">
        {/* Main Floating Glass Card */}
        <div className="pearl-card p-5 sm:p-7 border border-[#E2E8F0] relative overflow-hidden shadow-lg shadow-[#0D5C3A]/5">
          {/* Top Decorative Pearl Pink Accent */}
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#0D5C3A] via-[#0EA5E9] to-[#DB2777]"></div>

          {/* Institutional Badge */}
          <div className="text-center mb-4">
            <div className="flex justify-center mb-2">
              <img 
                src="/logos/psna_logo.png" 
                alt="PSNA College of Engineering and Technology, Dindigul" 
                className="h-10 sm:h-12 w-auto object-contain drop-shadow-2xs"
              />
            </div>

            <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full bg-[#ECFDF5] border border-[#A7F3D0] text-[#0D5C3A] text-[11px] font-bold mb-1.5 shadow-2xs">
              <Sparkles className="w-3 h-3 text-[#0D5C3A]" />
              <span>PSNA CET • Autonomous Academic Portal</span>
            </div>
            
            <h2 className="text-lg sm:text-xl font-black text-[#1E293B] tracking-tight">
              AI SMART PLACEMENT ASSISTANT
            </h2>
            <p className="text-[11px] sm:text-xs font-bold text-[#0EA5E9] uppercase tracking-wider">
              & Management System (2026 Edition)
            </p>
            <p className="text-[11px] text-[#64748B] mt-1 max-w-sm mx-auto leading-relaxed">
              Automating academic data ingestion, Anna University R-2022 CGPA calculations, AI resume & certificate fraud auditing, and corporate placement eligibility.
            </p>
          </div>

          {/* Department Selection Box (Locked to IT) */}
          <div className="space-y-3 mb-4">
            <div>
              <label className="block text-[11px] font-bold text-[#334155] uppercase tracking-wider mb-1 flex items-center justify-between">
                <span>Academic Department</span>
                <span className="text-[10px] text-[#0D5C3A] font-semibold flex items-center gap-1">
                  <Lock className="w-3 h-3" /> Pre-Configured
                </span>
              </label>

              <div className="relative">
                <input
                  type="text"
                  readOnly
                  value="INFORMATION TECHNOLOGY (IT)"
                  className="w-full bg-[#F8FAF9] border border-[#CBD5E1] text-[#1E293B] font-bold text-xs sm:text-sm rounded-lg py-2.5 px-3 cursor-not-allowed select-none shadow-inner"
                />
                <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <span className="text-[10px] bg-[#0D5C3A] text-white font-bold px-1.5 py-0.5 rounded">
                    LOCKED
                  </span>
                </div>
              </div>
            </div>

            {/* Quick Feature Grid */}
            <div className="grid grid-cols-2 gap-2">
              <div className="p-2 rounded-lg bg-[#F8FAF9] border border-[#E2E8F0] flex items-center space-x-1.5 text-[11px] text-[#475569]">
                <Bot className="w-3.5 h-3.5 text-[#0EA5E9]" />
                <span className="font-semibold">Placement AI Chatbot</span>
              </div>
              <div className="p-2 rounded-lg bg-[#F8FAF9] border border-[#E2E8F0] flex items-center space-x-1.5 text-[11px] text-[#475569]">
                <FileSpreadsheet className="w-3.5 h-3.5 text-[#108981]" />
                <span className="font-semibold">5-Tier Color Excel</span>
              </div>
              <div className="p-2 rounded-lg bg-[#F8FAF9] border border-[#E2E8F0] flex items-center space-x-1.5 text-[11px] text-[#475569]">
                <ShieldCheck className="w-3.5 h-3.5 text-[#DB2777]" />
                <span className="font-semibold">Fake Cert Detector</span>
              </div>
              <div className="p-2 rounded-lg bg-[#F8FAF9] border border-[#E2E8F0] flex items-center space-x-1.5 text-[11px] text-[#475569]">
                <Database className="w-3.5 h-3.5 text-[#0D5C3A]" />
                <span className="font-semibold">R-2022 CGPA Engine</span>
              </div>
            </div>
          </div>

          {/* Continue Action Button */}
          <button
            onClick={() => onNavigate('login')}
            className="w-full py-2.5 px-4 btn-emerald rounded-lg text-xs sm:text-sm font-bold shadow-md shadow-[#0D5C3A]/20 flex items-center justify-center space-x-2 group cursor-pointer"
          >
            <span>Continue to Institutional Access Portal</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
}
