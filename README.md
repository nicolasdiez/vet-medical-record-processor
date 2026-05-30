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

    ```bash
    cd src/backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

Create a `.env.dev` file in the `src/backend` directory:

    GEMINI_API_KEY=your_api_key_here
    ENVIRONMENT=development

Run the FastAPI server:

    ```bash
    uvicorn app.main:app --reload
    ```

### 2. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install dependencies:

    ```bash
    cd src/frontend
    npm install
    ```

Start the Vite development server:

    ```bash
    npm run dev
    ```

The application will be available at `http://localhost:5173`.

---

## 🐳 Getting Started (Docker Deployment)

You can run the entire application stack (Frontend, Backend, Database, and Network) in isolated containers using Docker Compose.

### Prerequisites
* Docker and Docker Compose installed.
* **For Windows users:** WSL 2 (Windows Subsystem for Linux) is required.
  * To install WSL, open PowerShell as Administrator and run: `wsl --install`
  * Restart your computer and set up your Linux username/password.
  * If using **Git Bash**, simply type `wsl` to enter the Linux environment. Then, to install the lightweight **Docker Engine** without the heavy Docker Desktop app, run:
    `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`
  * Finally, start the Docker service with: `sudo service docker start`

### 1. Environment Setup
Create a `.env` file in the **root** directory of the project and add your Gemini API Key:

    GEMINI_API_KEY=your_api_key_here

### 2. Run the Stack
Execute the following command from the root directory to build and start the containers in detached mode. 

*(⚠️ **Important for Windows users:** Since we installed Docker inside WSL in the prerequisites, ensure you are executing this command **inside your WSL terminal**, not in standard PowerShell or Git Bash).*

    ```bash
    sudo docker compose up -d --build
    ```
*("sudo docker compose down" to stop all the containers running)*

### 3. Access the Application
Once the containers are up and running, the Nginx web server will serve the frontend at:

    http://localhost:8080

*(The backend API will be running internally on port 8000 and exposed if needed for direct queries).*

---

## ⚖️ License & Copyright

**© 2026 Nicolás Diez Risueño. All rights reserved.**

This repository and its entire contents, including but not limited to the source code, system architecture, database schema, design patterns, UX/UI layouts, and underlying structural concepts, are strictly proprietary and confidential. 

Any unauthorized use, reproduction, modification, distribution, or structural imitation (including conceptual cloning, architectural adaptation, or using the core design logic as a blueprint for internal or commercial workflows) without explicit written permission from the author is strictly prohibited. This project is protected under international copyright and intellectual property laws.

---