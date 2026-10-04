import React, { useState } from 'react';
import { ShieldCheck, ArrowLeft, Check, FileText, Lock, Users, Cpu, Database, UserCheck, AlertTriangle } from 'lucide-react';

export default function TermsPage({ onNavigate, onAccept }) {
  const [accepted, setAccepted] = useState(false);

  const handleAcceptTerms = () => {
    setAccepted(true);
    if (onAccept) onAccept();
    if (onNavigate) onNavigate('login', { agreed: true });
  };

  return (
    <div className="min-h-screen bg-[#F4F7F6] py-8 px-4 sm:px-6">
      <div className="max-w-4xl mx-auto">
        {/* Top Navigation Bar */}
        <div className="flex items-center justify-between mb-6">
          <button
            onClick={() => onNavigate('login')}
            className="inline-flex items-center space-x-2 text-xs font-bold text-[#0D5C3A] bg-white px-3.5 py-2 rounded-lg border border-[#E2E8F0] shadow-2xs hover:bg-[#ECFDF5] transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>← Return to Institutional Login</span>
          </button>

          <span className="text-xs text-[#64748B] font-medium bg-[#FDF2F8] text-[#DB2777] border border-[#FCE7F3] px-3 py-1 rounded-full">
            Official Governance Document
          </span>
        </div>

        {/* Main Document Container */}
        <div className="pearl-card p-6 sm:p-10 border border-[#E2E8F0]">
          {/* Header */}
          <div className="border-b border-[#E2E8F0] pb-6 mb-8 text-center sm:text-left">
            <div className="flex flex-wrap items-center justify-between gap-4 mb-4 pb-4 border-b border-[#E2E8F0]/70">
              <img src="/logos/psna_logo.png" alt="PSNA Logo" className="h-10 w-auto object-contain" />
              <div className="flex items-center gap-3">
                <img src="/logos/naac_logo.png" alt="NAAC A++" className="h-8 w-auto object-contain" />
                <img src="/logos/nba_logo.png" alt="NBA" className="h-6 w-auto object-contain" />
                <img src="/logos/nirf_logo.png" alt="NIRF" className="h-6 w-auto object-contain" />
                <img src="/logos/ariia_logo.png" alt="ARIIA" className="h-6 w-auto object-contain" />
              </div>
            </div>

            <div className="inline-flex items-center space-x-2 text-xs font-bold text-[#0D5C3A] bg-[#ECFDF5] px-3 py-1 rounded-full border border-[#A7F3D0] mb-3">
              <ShieldCheck className="w-4 h-4 text-[#0D5C3A]" />
              <span>PSNA CET • Department of Information Technology</span>
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-[#1E293B] tracking-tight">
              Terms and Conditions & Privacy Policy
            </h1>
            <p className="text-sm font-semibold text-[#0EA5E9] mt-1">
              Smart Academic Assistant & IT Placement Portal Governance Protocol
            </p>
            <div className="mt-4 p-3.5 rounded-xl bg-[#F8FAF9] border border-[#E2E8F0] text-xs text-[#475569] leading-relaxed">
              <span className="font-bold text-[#1E293B]">Ownership Declaration: </span>
              The Service is owned, engineered, and maintained by{' '}
              <strong className="text-[#0D5C3A]">ANEESH KANNA N</strong> and{' '}
              <strong className="text-[#0D5C3A]">ANNE BENILDA A</strong>. All Rights Reserved.
            </div>
          </div>

          {/* Table of Quick Links */}
          <div className="mb-8 p-4 rounded-xl bg-[#F0F9FF] border border-[#BAE6FD]/80 text-xs">
            <p className="font-bold text-[#0369A1] mb-2 flex items-center gap-1.5">
              <FileText className="w-4 h-4" /> Quick Sections Index (15 Sections):
            </p>
            <div className="flex flex-wrap gap-2 text-[11px]">
              {['1. About', '2. RBAC Roles', '3. Data Freezing', '4. Data Collected', '5. AI Suite', '6. Privacy Masking', '7. Retention', '8. Security', '9. Rights', '10. Storage', '11. Auth', '12. Updates', '13. Termination', '14. Liability', '15. Developers'].map((s, idx) => (
                <a key={idx} href={`#section-${idx + 1}`} className="px-2 py-0.5 bg-white text-[#0284C7] rounded border border-[#BAE6FD] hover:bg-[#E0F2FE]">
                  {s}
                </a>
              ))}
            </div>
          </div>

          {/* All 15 Formal Governance Sections */}
          <div className="space-y-8 text-xs sm:text-sm text-[#334155] leading-relaxed">

            {/* Section 1 */}
            <section id="section-1" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">1</span>
                About the Service
              </h2>
              <p>
                The Service is an advanced student academic manager and placement automation platform designed specifically for the Information Technology (IT) department of PSNA College of Engineering and Technology to handle student tracking from 1st to 4th year across multiple batches and sections (A to F).
              </p>
              <p className="mt-2 text-[#64748B]">
                The purpose of the Service is to simplify repetitive data collection, map real-time academic trends through automated color coding, manage administrative access for faculty and the Head of Department (HOD), and deploy AI automation tools to streamline placement drives, resume auditing, and certificate verification.
              </p>
            </section>

            {/* Section 2 */}
            <section id="section-2" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">2</span>
                Eligibility and Account Responsibilities (RBAC)
              </h2>
              <p>
                Access is governed by a strict Role-Based Access Control (RBAC) hierarchy. Users must supply accurate institutional credentials:
              </p>
              <ul className="list-disc pl-5 mt-2 space-y-1 text-[#475569]">
                <li><strong className="text-[#1E293B]">Students:</strong> Responsible for inputting initial setup parameters, checking company profiles, and using the AI suite honestly. Strictly prohibited from attempting to view peer records or bypass security layers.</li>
                <li><strong className="text-[#1E293B]">Tutors & Class Incharges:</strong> Responsible for auditing student files, executing manual score overrides, and managing individual placement eligibilities.</li>
                <li><strong className="text-[#1E293B]">Head of Department (HOD):</strong> Granted master oversight to track overall departmental trends and staff assignments concurrently.</li>
              </ul>
            </section>

            {/* Section 3 */}
            <section id="section-3" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">3</span>
                Academic Calculations & Automated Systems
              </h2>
              <div className="space-y-2">
                <div className="p-3 bg-[#F8FAF9] rounded-lg border border-[#E2E8F0]">
                  <strong className="text-[#0D5C3A] block mb-1">🔒 The Data Freezing Rule:</strong>
                  To maintain absolute data integrity, student profiles are instantly locked upon initial submission. Students cannot directly modify their profile info. Corrections require a formal digital permission request that must be approved and executed manually by an authorized Class Incharge or Tutor.
                </div>
                <div className="p-3 bg-[#F8FAF9] rounded-lg border border-[#E2E8F0]">
                  <strong className="text-[#0EA5E9] block mb-1">📊 Visual Performance Dashboards:</strong>
                  The system renders real-time academic trends, class performances, and project distributions through dynamic Bar Graphs and Linear Performance Charts for faculty review.
                </div>
                <div className="p-3 bg-[#F8FAF9] rounded-lg border border-[#E2E8F0]">
                  <strong className="text-[#DB2777] block mb-1">⚡ One-Click Eligibility:</strong>
                  Placement eligibility flags (&quot;Eligible&quot; or &quot;Not Eligible&quot;) and company status counters (&quot;Placed&quot; alongside salary package details) are deployed at the absolute discretion of authorized faculty handlers.
                </div>
              </div>
            </section>

            {/* Section 4 */}
            <section id="section-4" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">4</span>
                Privacy Policy: Information We Collect
              </h2>
              <p>We process and retain structural student and staff metrics including:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1 text-[#475569]">
                <li>Account and Profile Information: Full legal name, register number, roll number, email address, phone number, admission year, batch, and section (A to F).</li>
                <li>Academic and Placement Data: CGPA records, specific subject grades, active backlogs, internal assessment marks, and placement eligibility statuses.</li>
                <li>Uploaded Media: PDF resumes, NPTEL, GATE, and global technical course certificates.</li>
                <li>System Metadata: Natural language AI queries and extracted search JSON arrays.</li>
              </ul>
            </section>

            {/* Section 5 */}
            <section id="section-5" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">5</span>
                How We Use Your Information (The AI Suite)
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-[#475569]">
                <li><strong className="text-[#1E293B]">Placement AI Chatbot:</strong> Translates natural language questions into structured database filters.</li>
                <li><strong className="text-[#1E293B]">Resume Quality Mark Test:</strong> Scores resume text patterns out of 100 and outputs targeted impact feedback.</li>
                <li><strong className="text-[#1E293B]">Fake Certificate Detector:</strong> Inspects file layout alignments, image tampering parameters, and font anomalies.</li>
              </ul>
            </section>

            {/* Section 6 */}
            <section id="section-6" className="scroll-mt-20">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">6</span>
                Data Storage & Privacy Masking Rule
              </h2>
              <div className="p-3 bg-[#ECFDF5] border border-[#A7F3D0] rounded-lg">
                <strong className="text-[#0D5C3A] block mb-1">🛡️ Privacy Masking Rule:</strong>
                To prevent student spying, the student directory hides sensitive metrics (such as CGPA, parent info, and failure logs) from peer views. It limits visible peer rows strictly to safe fields: Name, Register Number, Roll Number, Resume link, Email, and Phone.
              </div>
            </section>

            {/* Sections 7 to 15 condensed with full legal precision */}
            <section id="section-7">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">7</span>
                Data Retention and Deletion
              </h2>
              <p>
                Student profiles are retained for the active 4-year lifecycle. Students do not possess individual deletion rights. All deletion or graduation archiving must be processed through the department HOD or platform developers (<strong className="text-[#0D5C3A]">ANEESH KANNA N and ANNE BENILDA A</strong>).
              </p>
            </section>

            <section id="section-8">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">8</span>
                Security
              </h2>
              <p>
                We employ technical controls including Role-Based Access Control (RBAC), authenticated entry constraints, and secure cloud storage. Users are responsible for keeping passwords confidential.
              </p>
            </section>

            <section id="section-9">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">9</span>
                Your Choices and Rights
              </h2>
              <p>
                Students can view personal performance, check corporate profiles on the Company Bulletin Board, upload updated resumes for quality scoring, and track digital correction requests.
              </p>
            </section>

            <section id="section-10">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">10</span>
                Cookies and Local Storage
              </h2>
              <p>
                The platform utilizes browser session storage and local cache keys to keep you securely signed in across active sessions and to maintain draft states.
              </p>
            </section>

            <section id="section-11">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">11</span>
                Unified Authentication Mechanisms
              </h2>
              <p>
                Authentication tokens strictly confirm operational identity and align UI state with assigned role permissions (Student, Teacher, or HOD view).
              </p>
            </section>

            <section id="section-12">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">12</span>
                Changes to the Service or These Terms
              </h2>
              <p>
                The developers (<strong className="text-[#0D5C3A]">ANEESH KANNA N and ANNE BENILDA A</strong>) reserve the right to modify these Terms and Privacy Policy as the trial expands. Continuing to use the platform denotes full compliance.
              </p>
            </section>

            <section id="section-13">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">13</span>
                Suspension and Termination
              </h2>
              <p>
                Administrators reserve the right to suspend access if a user attempts to bypass permissions or access unauthorized peer data. If the Fake Certificate Detector flags an uploaded certificate for tampering, an automated compliance alert is sent directly to the class tutor.
              </p>
            </section>

            <section id="section-14">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">14</span>
                Disclaimer and Limitation of Liability
              </h2>
              <p>
                The Service is provided on an &quot;as available&quot; basis for departmental management. The developers shall not be held liable for algorithmic false flags or data parsing format mismatches from custom Excel sheets.
              </p>
            </section>

            <section id="section-15">
              <h2 className="text-base font-bold text-[#1E293B] flex items-center gap-2 border-b border-[#E2E8F0] pb-1.5 mb-2">
                <span className="w-6 h-6 rounded-md bg-[#0D5C3A] text-white flex items-center justify-center text-xs font-black">15</span>
                Contact & Governance Attribution
              </h2>
              <div className="p-4 bg-[#F8FAF9] rounded-xl border border-[#E2E8F0] space-y-1">
                <p><strong className="text-[#1E293B]">Lead Developers & Platform Owners: </strong> ANEESH KANNA N & ANNE BENILDA A</p>
                <p><strong className="text-[#1E293B]">Department: </strong> Information Technology, PSNA College of Engineering and Technology</p>
                <p className="text-[#0D5C3A] font-bold pt-2">© 2026 Developed by ANEESH KANNA N and ANNE BENILDA A. All Rights Reserved.</p>
              </div>
            </section>
          </div>

          {/* Bottom Confirmation Bar */}
          <div className="mt-10 pt-6 border-t border-[#E2E8F0] flex flex-col sm:flex-row items-center justify-between gap-4">
            <button
              onClick={() => onNavigate('login')}
              className="text-xs font-semibold text-[#64748B] hover:text-[#1E293B]"
            >
              ← Cancel & Return to Login
            </button>

            <button
              onClick={handleAcceptTerms}
              className="py-3 px-8 btn-emerald rounded-xl text-sm font-bold shadow-md shadow-[#0D5C3A]/20 flex items-center gap-2 cursor-pointer"
            >
              <Check className="w-4 h-4" />
              <span>I Agree & Acknowledge Terms</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
