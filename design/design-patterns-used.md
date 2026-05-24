# 🧠 Architecture & Design Patterns

This document outlines the core design patterns and architectural decisions implemented in the VetRecords Smart Processor. It is designed to provide clear insights into the technical reasoning behind the codebase.

---

## 🤖 1. Agentic AI & LLM Patterns

* **Human-in-the-Loop (HITL)**
  * **Concept:** An AI system design pattern where the machine learning model does the heavy lifting, but a human operator acts as the final decision-maker before data is persisted or actions are taken.
  * **Application in this App:** AI models (even advanced LLMs) can hallucinate or misinterpret complex clinical jargon. After processing the Clinical Document, the system does not save the data automatically. Instead, the veterinarian reviews the extracted `Pet` and `Medical Record` entities on the screen, applies corrections if needed, and explicitly approves the transaction.

* **LLM Schema Engineering & Constrained Decoding**
  * **Concept:** Techniques used to force a Large Language Model into producing deterministic, strictly typed, and machine-readable outputs (like JSON) instead of free-form conversational text. It combines prompt-level schemas with inference-level token restrictions.
  * **Application in this App:** Implemented using Pydantic models alongside the `instructor` library. By passing our domain structure directly to Gemini through its native schema capabilities, the system restricts the model's token generation at runtime. This guarantees 100% adherence to our data contracts, ensuring that fields like dates or names always arrive in the exact data type required by our backend.
  
---

## 🏗️ 2. Software Architecture Patterns

* **Hexagonal Architecture (Ports and Adapters)**
  * **Concept:** An architectural pattern that isolates the core business logic (Domain) from outside concerns (UI, Databases, External APIs). It uses "Ports" (interfaces) to define how the core communicates, and "Adapters" (concrete implementations) to connect to the outside world.
  * **Application in this App:** The backend is strictly divided. The core Use Cases and Domain models have zero knowledge of FastAPI, SQLite, or Gemini. If we want to swap Gemini for OpenAI, or SQLite for PostgreSQL, we only create a new Adapter. The core domain remains entirely untouched.

* **Domain-Driven Design (DDD)**
  * **Concept:** An approach focused on modeling the software to match the real-world business domain, using a "Ubiquitous Language" shared by developers and domain experts.
  * **Application in this App:** The code speaks the language of a veterinary clinic. We have distinct Domain Entities (`Pet`, `ClinicalRecord`) separated from Database ORM models. Business rules (like requiring an owner's name for a pet) are enforced at the Domain layer, not in the database or the UI.

** **Repository Pattern**
  * **Concept:** An abstraction layer between the application logic and the data mapping layer. It isolates the domain from the details of the database access technology.
  * **Application in this App:** Our Use Cases do not write SQL queries or interact directly with SQLAlchemy. Instead, they depend on abstract interfaces (Ports) namely `PetRepositoryPort` and `MedicalRecordRepositoryPort`. This makes the core application logic completely agnostic of the database engine and extremely easy to unit-test using mocks.

* **Dependency Injection (DI)**
  * **Concept:** A technique where an object receives its dependencies from outside rather than creating them itself.
  * **Application in this App:** Heavily leveraged via FastAPI's `Depends`. The router injects the specific Database Repository and the specific LLM Adapter into the Use Case at runtime. 

* **Strategy Pattern**
  * **Concept:** A behavioral design pattern that lets you define a family of algorithms, put each of them into a separate class, and make their objects interchangeable.
  * **Application in this App:** Used for document parsing. Depending on the type of clinical document uploaded (PDF, Word, Image), the router or service instantiates the specific `DocumentParser` strategy object (eg. `PDFFileTextExtractorAdapter`). This adheres to the Open/Closed Principle: if we want to support `.csv` files tomorrow, we just add a new strategy class without modifying the existing router logic.

* **Strategic Decision: JavaScript (JS) instead of TypeScript (TS)**
  * **Concept:** Choosing a dynamically typed language over a statically typed one for frontend development.
  * **Application in this App:** While TypeScript is the industry standard for large enterprise applications, standard JavaScript (ES6+) was intentionally chosen for this MVP/Proof of Concept. This maximizes development velocity, reduces build-step friction, and allows for rapid prototyping of the UI. For a V2 scaling phase, incrementally adopting TypeScript would be the logical next step.

---

## 🛠️ 3. Solution Architecture Patterns

* **Relational Database (SQLite to PostgreSQL path)**
  * **Concept:** Storing data in tables with strictly defined relationships and enforcing ACID (Atomicity, Consistency, Isolation, Durability) properties.
  * **Application in this App:** Veterinary medical data is highly structured and sensitive. A relational model perfectly maps the One-to-Many relationship between a `Pet` and its `MedicalRecords`. While SQLite is used for local development agility, the architecture via SQLAlchemy is designed to seamlessly migrate to **PostgreSQL** for production environments to ensure concurrent transaction safety.

* * **LLM as a Semantic Extraction Engine (Text-to-Structured-Data)**
  * **Concept:** Using a Large Language Model not as a conversational chatbot, but as a deterministic NLP processing engine designed to parse unstructured, messy text into highly structured database records.
  * **Application in this App:** Veterinary records often lack a standardized format. Instead of building brittle, custom Regular Expressions (Regex) to scrape names, dates, or diagnoses, the system first extracts the raw text from the document (using a Document Parser strategy) and feeds it to Gemini. Gemini is used strictly as a semantic parser: it understands the clinical context of the plain text and maps it accurately to our rigid Domain Entities, drastically reducing parsing errors across different clinic formats.

* **Multi-Stage Containerization (Docker)**
  * **Concept:** Using different Docker images for building the application versus running the application, keeping the final production image minimal and secure.
  * **Application in this App:** Used in the frontend deployment. Stage 1 uses a heavy `Node.js` image to install dependencies and compile the Vite/React code into static assets. Stage 2 uses an ultra-lightweight `Nginx` image merely to serve those static files. This drastically reduces the attack surface and image size.