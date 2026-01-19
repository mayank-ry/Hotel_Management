PROJECT
REPORT ON
Smart Resume Parser

Table Of Content
NOTE: Generate TOC in MS Word: References → Table of Contents → Automatic Table 1. After edits, right-click TOC → Update Field..
# Abstract

Virex AI is an enterprise-inspired recruitment intelligence platform that automates two high-cost stages of hiring:
(i) Resume Screening (ii) Preliminary Technical Interviews . Conventional recruitment workflows require recruiters to manually read and compare resumes against job descriptions (JDs), leading to fatigue-driven errors, delayed hiring, and inconsistent shortlisting. Existing Applicant Tracking Systems (ATS) typically depend on keyword matching, which fails under synonym variations.

To address this, Virex AI ingests PDF or plaintext resumes, extracts clean textual content using a robust parsing stack (PyPDF2 + PyMuPDF with OCR fallback), and converts unstructured documents into structured candidate profiles. The system then performs role-fit evaluation using a hybrid approach : (a) strict skill validation using word-boundary regex checks to avoid hallucinated matches, and (b) deterministic parameter scoring (Education, Experience, Skills, Projects, Certifications) on a 1–5 Likert scale. Role-specific weighting templates ensure evaluation fairness across Intern, Junior/Mid, and Senior positions. Based on normalized scores (0–100), candidates are Automatically classified into Shortlist/Waitlist/Reject buckets.
For borderline profiles, Virex AI issues an interview link for a context-aware AI interviewer that generates questions from the candidate resume and JD, enforces time limits (40 seconds/question), and grades answers on correctness, depth, and clarity (0–10). A final promotion algorithm combines Resume Score (40%) and Interview Score (60%) to upgrade deserving candidates. Additionally, a 3-ring anti-cheating suite—browser lockdown, strict timers, and backend flagging with 3-strike termination—improves assessment integrity. Overall, Virex AI reduces screening time significantly, improves standardization, and provides explainable, scalable hiring automation suitable for hackathon and industry demonstration.

# 1. Introduction
Recruitment teams often handle hundreds of applications per role. Manual screening of resumes is time-consuming and inconsistent, requiring recruiters to interpret diverse resume formats, normalize candidate information, and compare it against job requirements. As hiring volume increases, decision quality decreases due to fatigue, time pressure, and subjective bias.
## 1.1 Challenges in Modern Recruitment
High volume of resumes leads to superficial screening and missed talent.
Unstructured resume formats make extraction inconsistent across recruiters.
Bias and subjectivity create non-repeatable decisions.
Scheduling preliminary interviews delays time-to-hire.
Traditional ATS keyword matching fails with synonyms and creates false positives.
## 1.2 Why AI Resume Parsing Matters
AI-based parsing converts resumes into structured data, enabling measurable scoring and analytics. When combined with deterministic evaluation logic, AI reduces bias, increases auditability, and helps recruiters make faster decisions. Virex AI extends this pipeline by integrating a standardized AI interview module to validate skills claimed in resumes.
# 2. Problem Statement and Objectives
## 2.1 Problem Statement
Build a system that can parse PDF/plaintext resumes, convert them into structured candidate profiles, and generate a match score against a Job Description (JD), enabling recruiters to shortlist candidates quickly and accurately with minimal manual effort.
## 2.2 Assumptions
Resumes may be either selectable-text PDFs or scanned PDFs, plaintext (.txt) files are also supported.
Job description can be provided as text input or as a PDF file.
The evaluation must be explainable and consistent across candidates.
Candidates may attempt cheating during AI interviews; system must implement proctoring.
## 2.3 Objectives
Parse resumes (PDF / TXT) and extract clean textual content.
Convert unstructured text into a structured profile (name, contact, skills, education, experience).
Compute a deterministic role-fit score normalized to 0–100.
Support multiple formats and diverse resume structures.
Provide API-first design for integration with dashboards and external systems.
Trigger actions: shortlist, waitlist (invite interview), reject with notification workflows.
Conduct AI interviews for borderline candidates with automated scoring and anti-cheat enforcement.
# 3. Existing System vs Proposed System
Virex AI improves hiring decisions by combining deterministic scoring with context-aware LLM extraction and interview evaluation. The comparison below highlights key differences.

# 4. Solution
## Proposed Solution Overview
Virex AI is a full-stack recruitment automation platform with two stages : Resume Evaluation (Virex Engine) and AI Interview (Virtual Interviewer). The system ingests resumes and JDs, extracts structured profiles using LLM + rules, computes deterministic scores using a weighted Likert model, and triggers workflow actions.
## 4.1 Key Functional Blocks
Resume Ingestion: batch upload of multiple resumes with a single JD.
Extraction Pipeline: PDF parsing + cleaning + section detection.
Structured Profile Generation: LangChain + Pydantic strict JSON output.
Weighted Scoring Engine: deterministic evaluation using role templates.
Decision Workflow: shortlist/waitlist/reject with email notifications.
AI Interview Module: adaptive Q&A, TTS/STT, automated grading.
Promotion Algorithm: final score = 0.4 resume + 0.6 interview.
Anti-cheating: 3-ring defense suite with violations logging and termination.
## 4.2 Decision Buckets
Shortlisted : high confidence profiles; direct next-round action.
Waitlisted : borderline profiles; interview invite link generated.
Rejected : does not meet thresholds; rejection email is queued.
# 5. System Design and Architecture
The implementation follows a modular monolith architecture (microservices-ready). The backend is built on FastAPI and exposes REST endpoints for authentication, resume processing, candidate workflows, and interview management.The system uses SQLAlchemy models with SQLite/PostgreSQL compatibility, and Redis cache for interview state.
## 5.1 Major Modules (Code Reference from Repository)
Resume Parser : app/resume_parser.py (PyPDF2 + OCR fallback).
Matcher & Scoring : app/matcher.py, app/role_templates.py.
Interview Engine : app/interview_manager.py, app/grading.py.
Anti-cheat Proctoring (Frontend) : static/candidate.js.
Database Layer : app/models/models.py, app/db.py.
Routers : app/routers/candidates.py, interview.py, auth.py.
## 5.2 Client–Server Architecture
Client : Recruiter dashboard (upload, leaderboard, actions).
Client : Candidate interview portal (TTS/STT + proctoring).
Server : FastAPI backend orchestrating parsing, scoring, interview sessions.
Persistence : relational database for candidates, sessions, transcripts, flags.
Cache : Redis used for active interview session state.
# 6. System Architecture, Workflow and Diagrams
This section explains the provided architecture and workflow diagrams. The diagrams are intentionally kept as placeholders so that the team can paste Mermaid/Markdown diagram blocks directly in the final report.
## Figure 1: System Architecture Diagram

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768829821158-5e6b8071-9341-4c08-ad61-4c7062a81e5d.png" alt="image" width="650">
</p>

### Purpose
To present the high-level modular decomposition of Virex AI and how data moves between recruiter UI, parsing engine, scoring engine, interview engine, and storage.
### Key Components
Frontend Dashboard (Recruiter UI): resume/JD upload, leaderboard, action buttons.
Resume Upload & Parsing Engine: extracts text from PDF/TXT (OCR fallback for scanned resumes).
LLM Structured Extractor (LangChain + Pydantic): produces strict JSON evidence and Likert scores.
Deterministic Weighted Scoring Engine: computes normalized score (0–100) using role templates.
Candidate Decision Workflow: shortlist/waitlist/reject + notifications.
AI Interview Engine: creates sessions, generates questions, grades answers, computes final score.
Anti-cheating Suite: browser lockdown, timers, backend flags + termination logic.
DB + Session + Transcript Logger: candidates, sessions, messages, flags, scores.
### Flow Explanation (Step-by-step)
Recruiter uploads JD and multiple resumes from the dashboard.
Backend parses each resume (PyPDF2 → PyMuPDF/OCR if needed).
LLM extracts structured evidence and Likert scores under strict output constraints.
Python layer re-computes scoring deterministically using role-specific weights.
Candidate is bucketed into Shortlisted / Waitlisted / Rejected.
Waitlisted candidates receive an AI interview link; session is created and cached.
Interview answers are graded; final score is calculated and written back to DB.
### Input / Output
Inputs :
JD text/PDF
Resume PDF/TXT files
Role template selection (auto/intern/junior/senior)
Outputs :
Leaderboard with scores and status
Candidate profile JSON
Interview transcript + report
Email notifications
### Engineering Significance
Clear separation of concerns enables microservices migration later.
Deterministic scoring makes decisions auditable and defensible.
Cache-backed interview sessions support reliability under concurrent users.
## Figure 2: System Workflow Diagram

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768829923683-91ad136f-5f3d-4890-9853-934438b33738.png" alt="image" width="650">
</p>

### Purpose
To explain the end-to-end operational workflow from ingestion to final decision.
### Key Components
Resume ingestion and parsing stage
Structured extraction and scoring stage
Decision stage (shortlist/waitlist/reject)
Interview stage for waitlist candidates
Promotion algorithm and final decision logging
### Flow Explanation (Step-by-step)
Recruiter logs in and uploads JD + resume batch.
Resumes are parsed and cleaned into text.
Evidence + Likert scores are generated; deterministic score is computed.
System assigns status and displays action buttons.
Waitlisted candidates are invited to interview; proctoring starts.
Interview scoring produces final score; threshold upgrades candidate.
### Input / Output
Inputs :
Recruiter credentials
JD
Resumes
Outputs :
Status bucket
Interview invite link
Final shortlist/reject
### Engineering Significance
Creates a measurable hiring funnel with standard checkpoints.
Reduces time-to-hire by automating screening + early interviews.
## Figure 3: DFD Level 0 (Context Diagram)

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768829979865-aea054c4-9c3c-4802-982e-2ae7ba192aa8.png" alt="image" width="650">
</p>

### Purpose
To show the system boundary and how external entities interact with Virex AI.
### Key Components
Recruiter (external entity)
Candidate (external entity)
Virex AI Platform (single process)
Database and Notification service (data stores / outputs)
### Flow Explanation (Step-by-step)
Recruiter provides JD and resumes to the platform.
Platform stores candidate records and evaluation results.
Candidate receives invite link and participates in interview.
Final decisions are communicated back to recruiter and candidate.
### Input / Output
Inputs :
Resumes, JD
Candidate responses
Recruiter actions
Outputs :
Scores, shortlist decisions
Interview report
Emails/notifications
### Engineering Significance
DFD-0 clarifies scope and system responsibilities.
Helps jury validate completeness of inputs/outputs and stakeholders.
## Figure 4: DFD Level 1 (Decomposition)

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768830053255-e87a574f-0e1e-4916-bc83-20cb250cf786.png" alt="image" width="650">
</p>

### Purpose
To decompose Virex AI into internal processes: parsing, extraction, scoring, interview and storage.
### Key Components
P1: Resume Parsing
P2: Structured Extraction
P3: Deterministic Scoring + Decision
P4: AI Interview + Proctoring
D1: Candidate Store
D2: Sessions/Transcripts Store
### Flow Explanation (Step-by-step)
P1 extracts clean text and stores raw resume text.
P2 converts text into evidence JSON and Likert scores.
P3 computes resume score and updates candidate status.
P4 creates interview session for waitlist and logs transcript.
### Input / Output
Inputs :
Resume files
JD
Candidate answers
Outputs :
Candidate profile
Scores
Transcript
Decision status
### Engineering Significance
Supports traceability of each stage (important for audits).
Allows scaling heavy steps (LLM calls) independently.
## Figure 5: UML Use Case Diagram

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768830111816-6fbc6493-a56d-4a28-8b0b-3f77ef915ea7.png" alt="image" width="650">
</p>

### Purpose
To capture functional requirements from user perspectives.
### Key Components
Actor : Recruiter – upload, view leaderboard, trigger actions.
Actor : Candidate – join interview, submit answers, view report.
Use Cases: login, upload resumes, evaluate, invite interview, shortlist/reject, generate report.
### Flow Explanation (Step-by-step)
Recruiter authenticates and performs bulk evaluation.
Recruiter triggers invite/shortlist/reject actions.
Candidate opens link, completes interview under proctoring.
System generates report and updates final status.
### Input / Output
Inputs :
Recruiter inputs
Candidate interview interaction
Outputs :
Use-case outcomes: score, decision, report
### Engineering Significance
Ensures requirements completeness for evaluation.
Maps directly to REST API endpoints in implementation.
## Figure 6: UML Class Diagram

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768830162649-22090fbc-1ef2-4381-906a-dad53e37e295.png" alt="image" width="650">
</p>

### Purpose
To document core data models and relationships implemented using SQLAlchemy and Pydantic schemas.
### Key Components
Candidate: id, resume_text, job_description, match_score, interview_score, final_score, status, flags.
Recruiter: username, password_hash, session_token.
UploadJob: job_id, total_files, processed_count, status, results.
InterviewSession: session_id, candidate_id, role, current_question, scores, is_active.
InterviewMessage: role, content, timestamp.
### Flow Explanation (Step-by-step)
Recruiter owns multiple candidates and upload jobs.
Candidate owns a session; session owns multiple messages and scores.
Flags and feedback are stored as JSON for extensibility.
### Input / Output
Inputs :
User actions and derived entities
Outputs :
Persistent database records
### Engineering Significance
Enables normalized storage and future migration to PostgreSQL.
Supports analytics on hiring funnel and interview integrity.
## Figure 7: Sequence Diagram – Resume Evaluation

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768830208349-31379ee9-76b9-488a-80d4-ba4fb0bf8d69.png" alt="image" width="650">
</p>

### Purpose
To explain runtime call order for parsing, extraction, scoring and DB updates.
### Key Components
Frontend Dashboard
FastAPI Upload Router
Background Batch Processor
Resume Parser
LLM Evaluator
Database
### Flow Explanation (Step-by-step)
Frontend calls /upload with resumes + JD.
Backend creates UploadJob record and starts background task.
Each resume is parsed into cleaned text.
LLM generates evidence + Likert scores for each candidate (batching supported).
Deterministic score computed; candidate written to DB.
Frontend polls /jobs/{job_id} and then fetches leaderboard.
### Input / Output
Inputs :
Resumes
JD
Outputs :
Candidate IDs, scores, decisions
### Engineering Significance
Background processing increases throughput and prevents UI blocking.
Batch evaluation reduces LLM calls and cost.
## Figure 8: Sequence Diagram – Interview Flow

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768830258615-0e77fb35-025e-42c8-97a4-018e1e35c16b.png" alt="image" width="650">
</p>

### Purpose
To describe how sessions are created, questions generated, answers graded and final score computed.
### Key Components
Candidate Browser
FastAPI Interview Router
InterviewManager
LLM (Question + Grading)
Redis Cache
Database
### Flow Explanation (Step-by-step)
Candidate opens interview link with candidate_id.
Backend validates permanent lockout and cookie-based session lock.
InterviewManager creates or resumes session; question is generated.
Candidate responds (text/STT); backend grades with GRADING_PROMPT.
After N questions, final score is computed and candidate status updated.
Report is shown and downloadable transcript is generated.
### Input / Output
Inputs :
Candidate ID
Answers
Outputs :
Interview score, final score, transcript
### Engineering Significance
Session cookie lock prevents device switching and restart attacks.
Redis state cache supports resilience and quick resume.
## Figure 9: ER Diagram (Database Design)

<p align="center">
  <img src="https://image2url.com/r2/default/images/1768844027103-a60dd8e4-121a-4240-80a7-08c3ed38feb3.png" alt="image" width="650">
</p>

### Purpose
To document relational storage used for candidates, sessions, transcripts, and recruiter isolation.
### Key Components
candidates table
recruiters table
upload_jobs table
interview_sessions table
interview_messages table
### Flow Explanation (Step-by-step)
Recruiter uploads batch → UploadJob row created.
Candidates are inserted with scores and status.
Interview sessions reference candidates via foreign key.
Messages store transcript chronologically for reporting.
### Input / Output
Inputs :
Candidate data, scores, flags
Outputs :
Queryable hiring funnel database
### Engineering Significance
Row-level recruiter_username ensures data isolation between recruiter accounts.
Schema is migration-ready to PostgreSQL for scale.
# 7. Technical Approach
## 7.1 Resume Parsing Techniques
The resume ingestion layer supports both PDFs and plaintext. For PDFs, the system first attempts selectable-text extraction using PyPDF2. If extracted content is too short (<50 characters), the system falls back to PyMuPDF page rendering and EasyOCR recognition (scanned resume support). All extracted content is cleaned using normalization (whitespace, artifacts removal) before downstream processing.
Supported formats: .pdf, .txt
Primary extraction: PyPDF2 PdfReader
Fallback extraction: PyMuPDF + EasyOCR
Post-processing: text cleaning + segmentation
## 7.2 Deterministic Weighted Scoring Engine
Virex AI intentionally avoids “black-box” ranking based only on LLM judgment. LLMs are used for structured evidence extraction and Likert scoring, but the final math and decision thresholds are enforced deterministically in Python (see app/matcher.py). This ensures repeatability, fairness, and auditability.
### Skill Validation (False Positive Prevention)
A core innovation is precision skill validation using strict word-boundary checks. This prevents partial matches such as “Java” matching “JavaScript”, or “C” matching “C++”. For symbolic skills such as “C++”, “C#”, “.NET”, the system uses safe substring checks with heuristics.
Example:
JD Skill: Java → matches only “Java” token in resume.
JD Skill: C → does not match inside “C++”.
JD Skill: Node.js → substring check for exact token presence.
## 7.3 Likert Scale Evaluation (1–5)
1 (Poor): No evidence or irrelevant background.
2 (Fair): Minimal match; significant gaps.
3 (Good): Meets core requirements.
4 (Very Good): Exceeds requirements with strong evidence.
5 (Exceptional): Perfect match; leadership / elite achievements.
## 7.4 Role-Specific Weighting
Different seniority levels prioritize different signals. Virex AI applies role templates as per role_templates.py. This ensures fairness (e.g., projects matter more for interns; experience dominates for seniors).
## 7.5 Resume Score Calculation
Virex AI computes a normalized resume score (0–100) from Likert values and role weights. The formula required for the hackathon report is:
Resume Score = (Σ(Parameter Score × Weight)) × 20
Where Parameter Score ∈ {1..5} and weights sum to 1. Multiplying by 20 maps the weighted Likert average to a 0–100 scale.
Worked Example (Junior/Mid Role) :
Education = 4/5, Experience = 3/5, Skills = 4/5, Projects = 3/5, Certs = 2/5
Weights = Edu : 0.20, Exp : 0.25, Skills : 0.30, Projects : 0.15, Certs : 0.10
Weighted Sum = (4×0.20)+(3×0.25)+(4×0.30)+(3×0.15)+(2×0.10)=3.40
Resume Score = 3.40 × 20 = 68.0 / 100

# 8. AI Interview Module
Borderline candidates are routed to an adaptive AI interview portal instead of being rejected. The interview is context-aware: it uses the candidate resume and JD to ask relevant questions and validate claimed skills. The implementation is managed by InterviewManager (app/interview_manager.py) with a structured grading rubric (app/grading.py).
## 8.1 Question Generation
Input context : resume_text + job_description + match_score + chat history.
Prompt : INTERVIEW_SYSTEM_PROMPT generates short conversational questions.
Progression : strong skills → gaps relative to JD → deeper probing.
## 8.2 Interview Flow
Candidate opens interview link (candidate_id).
System enforces fullscreen + webcam initialization.
Interview session is created/resumed with cookie lock.
AI asks question; TTS reads it (ElevenLabs / browser TTS fallback).
Candidate responds via typing or browser Speech-to-Text.
Answer graded (0–10) with feedback; next question generated.
After 5 questions, interview ends and report is generated.
## 8.3 Scoring Rubric (0–10)
Technical correctness: factual validity of solution.
Depth: explanation quality (how/why, trade-offs).
Clarity: communication structure and examples.
Time limit per question: 40 seconds (Ring 2 anti-cheat constraint).
# 9. Final Score and Promotion Algorithm
Virex AI applies a promotion algorithm that gives higher importance to verifiable interview performance. This design supports candidates from non-traditional backgrounds who may have weaker resumes but strong real skills.
Final Score = (Resume Score × 0.4) + (Interview Score × 0.6)
Resume Score is normalized to 0–100.
Interview Score is 0–10 and is scaled to 0–100 before combining.
Threshold: If Final Score ≥ 70 → candidate promoted to Shortlisted.
Example:
Resume Score = 60
Interview Score = 8.5/10 → 85
Final Score = (60×0.4) + (85×0.6) = 24 + 51 = 75 → Promoted
# 10. Anti-Cheating and Security Suite
Assessment integrity is critical for automated interviews. Virex AI implements a 3-ring defense strategy at the client and server level (see static/candidate.js and app/routers/interview.py).
## 10.1 Ring 1: Browser Lockdown
Fullscreen enforcement: exiting fullscreen triggers a violation.
Focus tracking: tab-switch/minimize detected via visibilitychange.
Right-click and copy/cut/paste disabled to prevent copying questions.
## 10.2 Ring 2: Secondary Device Countermeasures
Strict timer: 40 seconds per question reduces lookup time.
Unselectable question text limits OCR or quick copy workflows.
## 10.3 Ring 3: Monitoring & Backend Flagging
Webcam presence: self-audit webcam feed displayed to candidate.
Typing heuristics: blocks rapid injected text (superhuman input spikes).
Persistent violations logged in database (flags JSON).
3-strike termination: interview is terminated on 3rd violation.
## 10.4 Permanent Lockout Rules
Statuses Shortlisted / Rejected / Terminated / Completed are forbidden from restarting interviews.
Cookie-based session lock prevents running interview on another device concurrently.

# 11. Technology Stack

# 12. Implementation and Working (Step-by-step)
Recruiter logs in via /login; authentication cookie (session_token) is issued.
Recruiter uploads resume batch + JD via /upload endpoint (multipart form).
Backend creates UploadJob row and launches background processing.
Each resume is parsed (parse_resume) and cleaned into text.
System detects role automatically from JD (ROLE_DEDUCTION_PROMPT) or uses selected template.
LLM performs evidence extraction + Likert scoring; Python enforces weighted math and thresholds.
Candidate bucket assigned; leaderboard is updated in real-time.
Recruiter triggers action: shortlist/reject/invite interview; email is queued.
Candidate opens interview link; system enforces anti-cheat + session lock.
Interview is conducted (5 questions) and graded; final score computed.
Database updated with transcript, flags, and final decision.
## 12.1 Pseudocode (Key Pipeline)
for resume in uploaded_files:
    text = parse_resume(resume.bytes)
    evidence, likert = LLM_extract_and_score(text, jd)
    resume_score = deterministic_weighted_score(likert, role_template)
    decision = threshold_bucket(resume_score)
    save_candidate(text, resume_score, decision)

if decision == WAITLIST:
    session = create_interview_session(candidate_id)
    interview_score = run_ai_interview(session)
    final_score = 0.4*resume_score + 0.6*interview_score
    promote_if(final_score >= 70)
# 13. Results and Output Screens
This section documents expected outputs. Add screenshots in the placeholders below.
[Screenshot Placeholder] Recruiter Dashboard – Upload Screen
[Screenshot Placeholder] Leaderboard – Candidate Buckets & Action Buttons
[Screenshot Placeholder] Candidate Profile JSON Output
[Screenshot Placeholder] AI Interview Portal – Proctoring + Timer
[Screenshot Placeholder] Final Report – Transcript + Scores
# 14. Testing and Validation
Testing focused on correctness of parsing, deterministic scoring stability, API reliability, and security enforcement.
## 14.1 Unit and Integration Tests
Parser tests: verify PDF/TXT extraction across formats (tests/test_parser.py).
Auth tests: recruiter login and session protection (tests/test_auth.py).
API tests: upload job status endpoints and candidate retrieval.
## 14.2 Edge Cases Tested
Empty or very short extracted text triggers OCR fallback.
Scanned PDF resumes with non-selectable text.
Skills ambiguity: Java vs JavaScript; C vs C++ boundary checks.
Multiple candidates batch upload (chunk size=10, concurrency=5).
Interview restart attempts blocked using status + cookie lock.
## 14.3 Performance Considerations
Batch evaluation reduces number of LLM calls.
Background task processing avoids blocking UI.
Redis cache accelerates interview state operations.
# 15. Conclusion
Virex AI delivers a complete, explainable recruitment automation pipeline. By converting unstructured resumes into structured evidence and enforcing deterministic scoring with role templates, the system reduces manual screening time, improves fairness, and provides auditable decision reasoning. The integrated AI interview module further validates skills and offers a second chance mechanism for borderline candidates. The platform is scalable, secure, and suitable for real-world recruiting workflows and hackathon evaluation.
# 16. Future Scope
Multilingual resume parsing (Hindi and regional languages).
OCR optimization and layout-aware parsing for complex templates.
Vector embeddings hybrid search for semantic retrieval + ranking.
Model fine-tuning on recruitment datasets for role-specific grading.
Cloud deployment with microservices, queue workers, autoscaling.
Integration with HRMS/ATS systems via webhooks and APIs.
Recruiter analytics dashboard: funnel metrics, bias checks, time-to-hire.
# References (APA)
FastAPI Documentation. (n.d.). Retrieved from https://fastapi.tiangolo.com/
LangChain Documentation. (n.d.). Retrieved from https://python.langchain.com/
Pydantic Documentation. (n.d.). Retrieved from https://docs.pydantic.dev/
SQLite Documentation. (n.d.). Retrieved from https://www.sqlite.org/docs.html
ElevenLabs Documentation. (n.d.). Retrieved from https://elevenlabs.io/docs
OpenAI API Documentation. (n.d.). Retrieved from https://platform.openai.com/docs

