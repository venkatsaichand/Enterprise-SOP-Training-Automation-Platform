# AI SOP Training Engine

An AI-powered enterprise training platform that transforms Standard Operating Procedures (SOPs) into structured training guides, interactive assessments, and presentation-ready learning materials.

---

## Overview

Organizations rely on Standard Operating Procedures (SOPs) to ensure consistency, compliance, and operational excellence. However, converting lengthy SOP documents into effective training resources is often a manual and time-consuming process.

The AI SOP Training Engine automates this workflow by leveraging Google's Gemini API to generate structured training materials from SOP documents in seconds.

---

## Business Problem

Preparing onboarding and employee training material from SOP documents typically requires significant manual effort.

This project reduces that effort by automatically generating:

- Executive summaries
- Step-by-step training guides
- Scenario-based quizzes
- Common execution mistakes
- Process improvement recommendations
- Presentation-ready slide decks

---

## Features

- Upload SOP documents in PDF, DOCX, or TXT format
- Paste SOP text directly into the application
- Generate concise executive summaries
- Create structured role-based training guides
- Produce scenario-based quizzes with explanations
- Identify common execution mistakes
- Recommend practical process improvements
- Generate presentation-ready PowerPoint slides
- Export outputs as JSON, TXT, and PPTX

---

## Workflow

```
SOP Document
      │
      ▼
Document Parsing
      │
      ▼
Gemini AI Processing
      │
      ▼
Structured Training Package
      │
      ├── Executive Summary
      ├── Training Guide
      ├── Scenario Quiz
      ├── Common Mistakes
      ├── Process Improvements
      └── PowerPoint Slides
```

---

## Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Framework | Streamlit |
| AI Model | Google Gemini 2.5 Flash |
| File Processing | PyPDF, python-docx |
| Presentation Generation | python-pptx |
| Data Format | JSON |

---

## Skills Demonstrated

- Generative AI Application Development
- Prompt Engineering
- Enterprise Workflow Automation
- Knowledge Management
- Document Processing
- JSON Schema Design
- Streamlit Application Development
- Python Development
- API Integration
- UI/UX Design

---

## Business Impact

The application demonstrates how Generative AI can streamline internal knowledge management by converting operational documentation into standardized training resources.

Potential applications include:

- Employee onboarding
- SOP training
- Internal knowledge transfer
- Operations training
- Process documentation
- Learning and Development (L&D)

---

## Project Structure

```
main.py         → Streamlit application
prompts.py      → Prompt engineering templates
utils.py        → AI generation, parsing, exports
requirements.txt
```

---

## Future Improvements

- Multi-language support
- Role-specific training generation
- LMS integration
- Version comparison of SOPs
- AI-generated flowcharts
- Learning analytics dashboard

---

## Author

**Venkat Sai Chand Boda**

National Institute of Technology Kurukshetra
