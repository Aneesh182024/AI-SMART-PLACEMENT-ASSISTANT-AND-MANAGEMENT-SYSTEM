import React from 'react';
import { ExternalLink, Sparkles, ShieldCheck } from 'lucide-react';

export default function Footer({ onOpenPortfolio, onNavigate }) {
  return (
    <footer className="w-full bg-white border-t border-[#E2E8F0] shrink-0 py-2.5 px-4 text-xs text-[#64748B] z-30">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">

        {/* Left: Copyright & Developer Names */}
        <div className="flex items-center space-x-2 text-center sm:text-left">
          <span>© 2026 Developed by</span>
          <span className="font-bold text-[#1E293B] hover:text-[#0D5C3A] transition-colors">
            ANEESH KANNA N
          </span>
          <span>and</span>
          <span className="font-bold text-[#1E293B] hover:text-[#0D5C3A] transition-colors">
            ANNE BENILDA A
          </span>
          <span className="hidden md:inline text-[#94A3B8]">|</span>
          <span className="hidden md:inline text-[#64748B]">All Rights Reserved.</span>
        </div>

        {/* Right: Portfolio Link & Terms Link */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => onNavigate && onNavigate('terms')}
            className="text-[#64748B] hover:text-[#0EA5E9] hover:underline transition-colors flex items-center gap-1"
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Governance & Privacy</span>
          </button>

          <span className="text-[#CBD5E1]">|</span>

          {/* Dynamic Web Trigger: Click Me / Portfolio */}
          <button
            onClick={onOpenPortfolio}
            className="inline-flex items-center space-x-1.5 px-3 py-1 bg-[#FDF2F8] text-[#DB2777] border border-[#FCE7F3] rounded-full font-semibold hover:bg-[#FCE7F3] hover:shadow-xs transition-all cursor-pointer group"
          >
            <Sparkles className="w-3 h-3 text-[#DB2777] group-hover:rotate-12 transition-transform" />
            <span>Portfolio</span>
            <span className="text-[10px] bg-[#DB2777] text-white px-1.5 py-0.2 rounded-full">Click Me</span>
            <ExternalLink className="w-2.5 h-2.5" />
          </button>
        </div>
      </div>
    </footer>
  );
}
