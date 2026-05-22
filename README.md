# 🐾 VetRecords Smart Processor

[![Backend Tests CI](https://github.com/nicolasdiez/vet-medical-record-processor/actions/workflows/tests.yml/badge.svg)](https://github.com/nicolasdiez/vet-medical-record-processor/actions/workflows/tests.yml)

An AI-powered, full-stack application designed to automate the extraction, structuring, and persistence of clinical veterinary records from unstructured PDF documents. 

Built with a strong emphasis on clean code, validation, and user experience.

---

## 🏗️ Architecture & Tech Stack

This project strictly follows **Hexagonal Architecture (Ports and Adapters)** on the backend to isolate the domain logic from external concerns (like the database or the AI provider).

### Backend
* **Framework:** FastAPI (Python 3.11)
* **AI Integration:** Google Gemini Pro + `instructor` (for deterministic Pydantic schema extraction)
* **Database:** SQLite with SQLAlchemy ORM
* **Testing:** Pytest (Unit and End-to-End)

### Frontend
* **Framework:** React 18 + Vite
* **Styling:** Tailwind CSS
* **Form Management:** React Hook Form
* **Notifications:** React Hot Toast

---

## 🚀 Getting Started (Local Development)

### Prerequisites
* Python 3.11+
* Node.js 20+
* A Google Gemini API Key

### 1. Backend Setup
Navigate to the backend directory, create a virtual environment, and install dependencies:

    cd src/backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

Create a `.env.dev` file in the `src/backend` directory:

    GEMINI_API_KEY=your_api_key_here
    ENVIRONMENT=development

Run the FastAPI server:

    fastapi dev app/main.py

### 2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install dependencies:

    cd src/frontend
    npm install

Start the Vite development server:

    npm run dev

The application will be available at `http://localhost:5173`.

---

## 🐳 Docker Deployment (Coming Soon)
*The containerization of this application is currently in progress. A `docker-compose.yml` will be provided shortly to spin up the entire stack with a single command.*

---
*Developed as a proof-of-concept for AI-driven clinical workflow automation.*