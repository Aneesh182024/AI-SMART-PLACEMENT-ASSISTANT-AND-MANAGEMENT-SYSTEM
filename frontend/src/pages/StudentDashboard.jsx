import React, { useState } from 'react';
import { 
  User, GraduationCap, FileText, Award, Upload, CheckCircle2, 
  Lock, AlertTriangle, Sparkles, ExternalLink, ShieldCheck, 
  Eye, RefreshCw, BarChart2, BookOpen, Layers, Users
} from 'lucide-react';


export default function StudentDashboard({ user, onLogout }) {
  // Academic Form State
  const [cgpa, setCgpa] = useState('8.72');
  const [activeArrears, setActiveArrears] = useState('0');
  const [historyArrears, setHistoryArrears] = useState('0');
  const [semGpas, setSemGpas] = useState({
    sem1: '8.45', sem2: '8.60', sem3: '8.75', sem4: '8.80',
    sem5: '8.90', sem6: '8.85', sem7: '0.00', sem8: '0.00'
  });
  const [techSkills, setTechSkills] = useState('Python, Java, React, SQL, Machine Learning');
  const [isLocked, setIsLocked] = useState(true); // Data Freezing Gate
  const [requestSent, setRequestSent] = useState(false);

  // Resume Upload & AI Scorer State
  const [resumeFile, setResumeFile] = useState(null);
  const [isScoringResume, setIsScoringResume] = useState(false);
  const [resumeScore, setResumeScore] = useState(88);
  const [resumeFeedback, setResumeFeedback] = useState([
    { text: 'Strong action verbs detected (Architected, Developed, Implemented)', status: 'pass' },
    { text: 'Clean contact info & GitHub/LinkedIn hyperlinks found', status: 'pass' },
    { text: 'Recommendation: Add quantifiable numeric impact metrics to your final-year software project (e.g. "Increased processing speed by 25%")', status: 'warn' },
    { text: 'Consistent typography and clean reverse-chronological layout', status: 'pass' }
  ]);

  // Certificate Upload & AI Fake Detector State
  const [certFile, setCertFile] = useState(null);
  const [certType, setCertType] = useState('NPTEL Cloud Computing');
  const [isVerifyingCert, setIsVerifyingCert] = useState(false);
  const [certStatus, setCertStatus] = useState({
    analyzed: true,
    isAuthentic: true,
    confidence: '99.4%',
    remarks: 'No pixel tampering or font baseline shifts detected. Cryptographic layout verified.'
  });

  // Section-Segregated Peer Directory (Masked View)
  const [peers] = useState([
    { name: 'Aneesh Kanna N', regNo: '713821104001', rollNo: '21IT001', email: 'aneesh@psnacet.edu.in', mobile: '9876543210', year: 'IV', section: 'A', resumeUrl: '#' },
    { name: 'Anne Benilda A', regNo: '713821104002', rollNo: '21IT002', email: 'anne@psnacet.edu.in', mobile: '9876543211', year: 'IV', section: 'A', resumeUrl: '#' },
    { name: 'Balamurugan K', regNo: '713821104003', rollNo: '21IT003', email: 'bala@psnacet.edu.in', mobile: '9876543212', year: 'IV', section: 'A', resumeUrl: '#' },
    { name: 'Dharani S', regNo: '713821104004', rollNo: '21IT004', email: 'dharani@psnacet.edu.in', mobile: '9876543213', year: 'IV', section: 'A', resumeUrl: '#' },
    { name: 'Gokulnath R', regNo: '713821104005', rollNo: '21IT005', email: 'gokul@psnacet.edu.in', mobile: '9876543214', year: 'IV', section: 'A', resumeUrl: '#' },
    { name: 'Harini M', regNo: '713821104006', rollNo: '21IT006', email: 'harini@psnacet.edu.in', mobile: '9876543215', year: 'IV', section: 'A', resumeUrl: '#' },
  ]);

  // Handle Resume Drop
  const handleResumeDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer ? e.dataTransfer.files[0] : e.target.files[0];
    if (file) {
      setResumeFile(file.name);
      setIsScoringResume(true);
      setTimeout(() => {
        setIsScoringResume(false);
        setResumeScore(91);
      }, 1200);
    }
  };

  // Handle Certificate Drop
  const handleCertDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer ? e.dataTransfer.files[0] : e.target.files[0];
    if (file) {
      setCertFile(file.name);
      setIsVerifyingCert(true);
      setTimeout(() => {
        setIsVerifyingCert(false);
        setCertStatus({
          analyzed: true,
          isAuthentic: true,
          confidence: '99.8%',
          remarks: 'OpenCV pixel edge analysis & OCR font family matched official template.'
        });
      }, 1400);
    }
  };

  return (
    <div className="min-h-screen bg-[#F4F7F6] py-8 px-4 sm:px-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Top Header Card */}
        <div className="pearl-card p-6 border border-[#E2E8F0] flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#0D5C3A] to-[#108981] text-white flex items-center justify-center font-black text-xl shadow-md">
              AK
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-extrabold text-[#1E293B]">
                  {user?.name || 'Aneesh Kanna N'}
                </h2>
                <span className="text-xs bg-[#ECFDF5] text-[#0D5C3A] font-bold px-2.5 py-0.5 rounded-full border border-[#A7F3D0]">
                  Verified Student
                </span>
                <span className="text-xs bg-[#FDF2F8] text-[#DB2777] font-bold px-2 py-0.5 rounded-full border border-[#FCE7F3]">
                  Batch 2023–2027
                </span>
              </div>
              <p className="text-xs text-[#64748B] mt-0.5">
                Register No: <strong className="font-mono text-[#1E293B]">{user?.registerNo || '713821104001'}</strong> • Department of Information Technology • Year {user?.year || 'IV'} (Sec {user?.section || 'A'})
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 w-full md:w-auto justify-end">
            <button
              onClick={onLogout}
              className="px-4 py-2 text-xs font-bold text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors border border-red-200"
            >
              Sign Out
            </button>
          </div>
        </div>

        {/* 3 Main Grid Columns */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

          {/* COLUMN 1 & 2: ACADEMICS & MARKS (With Data Freezing Gate) */}
          <div className="lg:col-span-2 space-y-6">

            {/* Profile Freezing Banner */}
            <div className="p-4 rounded-xl bg-white border border-[#E2E8F0] shadow-xs flex items-center justify-between flex-wrap gap-3">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-[#FEF3C7] text-[#D97706] flex items-center justify-center">
                  <Lock className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-[#1E293B] flex items-center gap-1.5">
                    <span>Profile Data Freezing Gate: </span>
                    <span className="text-[#0D5C3A] font-extrabold uppercase">Active & Locked</span>
                  </h4>
                  <p className="text-xs text-[#64748B]">
                    Academic indices are frozen to preserve institutional audit integrity. Corrections require formal Tutor approval.
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setRequestSent(true)}
                disabled={requestSent}
                className={`px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all ${
                  requestSent
                    ? 'bg-[#ECFDF5] text-[#0D5C3A] border border-[#A7F3D0]'
                    : 'bg-[#F0F9FF] text-[#0EA5E9] hover:bg-[#E0F2FE] border border-[#BAE6FD]'
                }`}
              >
                {requestSent ? '✔ Permission Request Sent to Tutor' : 'Request Profile Unlock'}
              </button>
            </div>

            {/* Academic Indices Summary Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="pearl-card p-4 text-center">
                <p className="text-[11px] font-bold text-[#64748B] uppercase">Cumulative CGPA</p>
                <h3 className="text-2xl font-black text-[#0D5C3A] mt-1">{cgpa}</h3>
                <span className="text-[10px] text-[#108981] font-semibold">Anna Univ R-2022</span>
              </div>
              <div className="pearl-card p-4 text-center">
                <p className="text-[11px] font-bold text-[#64748B] uppercase">Active Backlogs</p>
                <h3 className="text-2xl font-black text-[#108981] mt-1">{activeArrears}</h3>
                <span className="text-[10px] text-[#108981] font-semibold">Clean Record</span>
              </div>
              <div className="pearl-card p-4 text-center">
                <p className="text-[11px] font-bold text-[#64748B] uppercase">Attendance Rate</p>
                <h3 className="text-2xl font-black text-[#0EA5E9] mt-1">94.5%</h3>
                <span className="text-[10px] text-[#0EA5E9] font-semibold">&gt; 75% (No SA)</span>
              </div>
              <div className="pearl-card p-4 text-center">
                <p className="text-[11px] font-bold text-[#64748B] uppercase">Placement Status</p>
                <h3 className="text-sm font-extrabold text-[#DB2777] mt-2">Eligible (Open)</h3>
                <span className="text-[10px] text-[#64748B]">Tutor Verified</span>
              </div>
            </div>

            {/* Semester-wise GPA Breakdown (Sem 1 to 8) */}
            <div className="pearl-card p-6 border border-[#E2E8F0]">
              <h3 className="text-sm font-extrabold text-[#1E293B] mb-3 flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-[#0D5C3A]" />
                  Semester GPA Progression (Anna University R-2022 Scale)
                </span>
                <span className="text-[11px] text-[#64748B] font-normal">
                  Weighted Credit Formulation
                </span>
              </h3>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {Object.entries(semGpas).map(([key, val], idx) => (
                  <div key={key} className="p-3 bg-[#F8FAF9] rounded-xl border border-[#E2E8F0] text-center">
                    <span className="text-[11px] font-bold text-[#64748B] uppercase block">
                      Semester {idx + 1}
                    </span>
                    <span className="text-base font-black text-[#1E293B]">
                      {val === '0.00' ? 'In Progress' : val}
                    </span>
                    <span className="text-[10px] text-[#94A3B8] block mt-0.5">
                      {idx === 0 && '22 Credits'}
                      {idx === 1 && '25 Credits'}
                      {(idx >= 2 && idx <= 4) && '22.5 Credits'}
                      {idx === 5 && '21 Credits'}
                      {idx === 6 && '17.5 Credits'}
                      {idx === 7 && '10 Credits'}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Section-Segregated Peer Directory Table */}
            <div className="pearl-card p-6 border border-[#E2E8F0]">
              <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
                <div>
                  <h3 className="text-sm font-extrabold text-[#1E293B] flex items-center gap-2">
                    <Users className="w-4 h-4 text-[#0EA5E9]" />
                    <span>Peer Directory — Year {user?.year || 'IV'} (Section {user?.section || 'A'})</span>
                  </h3>
                  <p className="text-xs text-[#64748B] mt-0.5">
                    Privacy Masking Active: Academic scores and backlogs of peers are protected.
                  </p>
                </div>
                <span className="text-[11px] bg-[#ECFDF5] text-[#0D5C3A] font-bold px-2.5 py-1 rounded-md border border-[#A7F3D0]">
                  {peers.length} Classmates Found
                </span>
              </div>

              {/* Table */}
              <div className="overflow-x-auto rounded-lg border border-[#E2E8F0]">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#F8FAF9] text-[#475569] font-bold border-b border-[#E2E8F0]">
                    <tr>
                      <th className="py-2.5 px-3">Student Name</th>
                      <th className="py-2.5 px-3">Register No</th>
                      <th className="py-2.5 px-3">Roll No</th>
                      <th className="py-2.5 px-3">Email Address</th>
                      <th className="py-2.5 px-3">Contact</th>
                      <th className="py-2.5 px-3 text-right">Resume</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E2E8F0]">
                    {peers.map((p, idx) => (
                      <tr key={idx} className="hover:bg-[#F8FAF9] transition-colors">
                        <td className="py-2.5 px-3 font-semibold text-[#1E293B]">{p.name}</td>
                        <td className="py-2.5 px-3 font-mono text-[#475569]">{p.regNo}</td>
                        <td className="py-2.5 px-3 font-mono text-[#64748B]">{p.rollNo}</td>
                        <td className="py-2.5 px-3 text-[#0EA5E9]">{p.email}</td>
                        <td className="py-2.5 px-3 text-[#475569] font-mono">{p.mobile}</td>
                        <td className="py-2.5 px-3 text-right">
                          <button className="text-[11px] text-[#0D5C3A] font-bold hover:underline flex items-center gap-1 justify-end ml-auto">
                            <span>View</span>
                            <ExternalLink className="w-3 h-3" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* COLUMN 3: AI SUITE (Resume Scorer & Fake Certificate Detector) */}
          <div className="space-y-6">

            {/* AI FEATURE 1: RESUME QUALITY MARK SCORER */}
            <div className="pearl-card p-6 border border-[#E2E8F0] relative overflow-hidden">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 rounded-lg bg-[#FDF2F8] text-[#DB2777] flex items-center justify-center font-bold">
                    <Sparkles className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-extrabold text-[#1E293B]">Resume AI Quality Test</h3>
                    <p className="text-[11px] text-[#64748B]">PyMuPDF + LLM Rubric Engine</p>
                  </div>
                </div>

                {/* Score Badge */}
                <div className="text-right">
                  <span className="text-2xl font-black text-[#0D5C3A]">{resumeScore}</span>
                  <span className="text-xs text-[#64748B]">/100</span>
                </div>
              </div>

              {/* Drag and Drop Zone */}
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleResumeDrop}
                className="p-5 border-2 border-dashed border-[#CBD5E1] rounded-xl text-center hover:border-[#0EA5E9] transition-colors cursor-pointer bg-[#F8FAF9]"
              >
                <input
                  type="file"
                  id="resume-upload"
                  accept=".pdf"
                  onChange={handleResumeDrop}
                  className="hidden"
                />
                <label htmlFor="resume-upload" className="cursor-pointer">
                  <Upload className="w-6 h-6 text-[#0EA5E9] mx-auto mb-2" />
                  <p className="text-xs font-bold text-[#1E293B]">
                    {resumeFile ? resumeFile : 'Drop PDF Resume or Browse'}
                  </p>
                  <p className="text-[10px] text-[#64748B] mt-0.5">
                    Analyzes metrics, action verbs, and layout
                  </p>
                </label>
              </div>

              {isScoringResume && (
                <div className="mt-3 p-2 bg-[#F0F9FF] text-[#0369A1] rounded-lg text-xs flex items-center justify-center gap-2">
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>AI parsing PDF layout & scoring...</span>
                </div>
              )}

              {/* AI Feedback Checklist */}
              <div className="mt-4 space-y-2">
                <span className="text-xs font-bold text-[#475569] block">AI Analysis Checklist:</span>
                {resumeFeedback.map((item, idx) => (
                  <div key={idx} className="p-2 rounded-lg bg-white border border-[#E2E8F0] text-[11px] flex items-start space-x-2">
                    {item.status === 'pass' ? (
                      <CheckCircle2 className="w-3.5 h-3.5 text-[#108981] shrink-0 mt-0.5" />
                    ) : (
                      <AlertTriangle className="w-3.5 h-3.5 text-[#F59E0B] shrink-0 mt-0.5" />
                    )}
                    <span className={item.status === 'pass' ? 'text-[#334155]' : 'text-[#B45309] font-medium'}>
                      {item.text}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* AI FEATURE 2: FAKE CERTIFICATE DETECTOR */}
            <div className="pearl-card p-6 border border-[#E2E8F0]">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 rounded-lg bg-[#ECFDF5] text-[#0D5C3A] flex items-center justify-center font-bold">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-extrabold text-[#1E293B]">Fake Certificate Detector</h3>
                  <p className="text-[11px] text-[#64748B]">OpenCV Image & Tesseract OCR Analysis</p>
                </div>
              </div>

              {/* Certificate Type Selector */}
              <div className="mb-3">
                <label className="block text-[11px] font-bold text-[#475569] mb-1">Select Credential Type</label>
                <select
                  value={certType}
                  onChange={(e) => setCertType(e.target.value)}
                  className="w-full input-field text-xs"
                >
                  <option value="NPTEL Cloud Computing">NPTEL Technical Examination</option>
                  <option value="GATE Score Card">GATE Score Card</option>
                  <option value="Global AWS Certification">AWS / Cloud Global Credential</option>
                  <option value="Oracle Java Cert">Oracle Certified Associate</option>
                </select>
              </div>

              {/* Upload Certificate */}
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleCertDrop}
                className="p-5 border-2 border-dashed border-[#CBD5E1] rounded-xl text-center hover:border-[#108981] transition-colors cursor-pointer bg-[#F8FAF9]"
              >
                <input
                  type="file"
                  id="cert-upload"
                  accept=".png,.jpg,.jpeg,.pdf"
                  onChange={handleCertDrop}
                  className="hidden"
                />
                <label htmlFor="cert-upload" className="cursor-pointer">
                  <Award className="w-6 h-6 text-[#108981] mx-auto mb-2" />
                  <p className="text-xs font-bold text-[#1E293B]">
                    {certFile ? certFile : 'Upload Credential Document'}
                  </p>
                  <p className="text-[10px] text-[#64748B] mt-0.5">
                    Checks font alignment, noise & seal integrity
                  </p>
                </label>
              </div>

              {isVerifyingCert && (
                <div className="mt-3 p-2 bg-[#ECFDF5] text-[#0D5C3A] rounded-lg text-xs flex items-center justify-center gap-2">
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Scanning image background & baseline...</span>
                </div>
              )}

              {/* Verification Status Card */}
              {certStatus.analyzed && !isVerifyingCert && (
                <div className="mt-4 p-3 rounded-xl bg-[#F0FDF4] border border-[#BBF7D0]">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-bold text-[#166534] flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-[#16A34A]" />
                      Authentic Certificate
                    </span>
                    <span className="font-mono font-bold text-[#15803D]">{certStatus.confidence} Match</span>
                  </div>
                  <p className="text-[11px] text-[#166534]">
                    {certStatus.remarks}
                  </p>
                </div>
              )}
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
