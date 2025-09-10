# Resume Analyzer

A Django-based Resume Analyzer that extracts text from PDF/DOCX resumes, highlights skills, education, and experience, and provides structured data. Users can view all uploaded resumes in a history page and download JSON/CSV files.

---

## Features

- Upload PDF or DOCX resumes
- Extract text and structured information:
  - Email
  - Phone number
  - Skills
  - Education
  - Experience
- Highlight skills, education, and experience in the resume text
- Download extracted data as JSON or CSV
- History page for all past uploads
- Pure Django + Python project (no external CSS frameworks)

---

## Tech Stack

- Python 3.11  
- Django 5.2.6  
- SQLite (default database)  
- HTML + CSS (static files)  
- Libraries: `python-docx`, `PyPDF2` (for PDF/DOCX text extraction)

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd resume_analyzer
