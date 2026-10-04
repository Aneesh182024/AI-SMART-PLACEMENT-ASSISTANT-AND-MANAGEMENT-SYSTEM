import React from 'react';
import { GraduationCap } from 'lucide-react';

export default function Header({ onNavigate, currentPage }) {
  return (
    <header className="w-full bg-white border-b border-[#E2E8F0] shadow-xs shrink-0 z-40">
      {/* 5 Institutional Official Logos Top Bar */}
      <div className="bg-[#FFFFFF] border-b border-[#E2E8F0]/80 py-1 sm:py-1.5 px-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between flex-wrap gap-2">
          
          {/* Logo 1: Official PSNA Crest & Name */}
          <div 
            onClick={() => onNavigate && onNavigate('landing')}
            className="flex items-center cursor-pointer hover:opacity-90 transition-opacity"
          >
            <img 
              src="/logos/psna_logo.png" 
              alt="PSNA College of Engineering and Technology, Dindigul" 
              className="h-8 sm:h-9 w-auto object-contain"
            />
          </div>

          {/* Logos 2, 3, 4, 5 Accreditation & Ranking Seals */}
          <div className="flex items-center space-x-2 sm:space-x-4 overflow-x-auto py-0.5">
            {/* NBA Logo */}
            <div className="flex items-center bg-white p-0.5 rounded border border-[#E2E8F0]/70">
              <img 
                src="/logos/nba_logo.png" 
                alt="NBA - National Board of Accreditation" 
                className="h-6 sm:h-7 w-auto object-contain"
              />
            </div>

            {/* NIRF Logo */}
            <div className="flex items-center bg-white p-0.5 rounded border border-[#E2E8F0]/70">
              <img 
                src="/logos/nirf_logo.png" 
                alt="NIRF - National Institutional Ranking Framework" 
                className="h-6 sm:h-7 w-auto object-contain"
              />
            </div>

            {/* NAAC A++ Seal */}
            <div className="flex items-center bg-white rounded-full">
              <img 
                src="/logos/naac_logo.png" 
                alt="NAAC Accredited with Grade A++" 
                className="h-7 sm:h-8 w-auto object-contain drop-shadow-2xs"
              />
            </div>

            {/* ARIIA Logo */}
            <div className="flex items-center bg-white p-0.5 rounded border border-[#E2E8F0]/70">
              <img 
                src="/logos/ariia_logo.png" 
                alt="ARIIA 2021" 
                className="h-6 sm:h-7 w-auto object-contain"
              />
            </div>
          </div>

        </div>
      </div>

      {/* Main Subtitle & Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 py-1.5 flex items-center justify-between">
        <div 
          onClick={() => onNavigate && onNavigate('landing')}
          className="flex items-center space-x-2.5 cursor-pointer group"
        >
          <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-gradient-to-br from-[#0D5C3A] to-[#108981] text-white flex items-center justify-center shadow-2xs group-hover:scale-105 transition-transform">
            <GraduationCap className="w-4 h-4 sm:w-4.5 sm:h-4.5" />
          </div>
          <div>
            <h2 className="text-xs sm:text-sm font-extrabold text-[#1E293B] tracking-tight group-hover:text-[#0D5C3A] transition-colors leading-tight">
              AI SMART PLACEMENT ASSISTANT AND MANAGEMENT SYSTEM
            </h2>
            <p className="text-[10px] sm:text-[11px] font-semibold text-[#0EA5E9] flex items-center gap-1.5">
              <span>Department of Information Technology</span>
              <span className="text-[9px] bg-[#FDF2F8] text-[#DB2777] font-bold px-1.5 py-0.2 rounded-full border border-[#FCE7F3]">
                Autonomous
              </span>
            </p>
          </div>
        </div>

        {/* Quick Nav Controls */}
        <div className="flex items-center space-x-1.5">
          {currentPage !== 'landing' && (
            <button
              onClick={() => onNavigate('landing')}
              className="px-2.5 py-1 text-xs font-semibold text-[#475569] hover:text-[#0D5C3A] hover:bg-[#F4F7F6] rounded-md transition-colors"
            >
              Home
            </button>
          )}
          {currentPage !== 'terms' && (
            <button
              onClick={() => onNavigate('terms')}
              className="px-2.5 py-1 text-xs font-semibold text-[#0EA5E9] hover:bg-[#F0F9FF] rounded-md transition-colors"
            >
              Policies & T&C
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
