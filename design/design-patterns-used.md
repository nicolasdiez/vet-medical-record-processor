# Agentic AI Patterns

* **Human-in-the-Loop (HITL)**: After processing the Clinical Document and extracting the Medical Records, the human user (veterinarian), who is infront of the screen, has the chance to review the extracted Pet and Medical Record entities, and execute corrections if needed.

* **LLM Schema Engineering** (or "Prompting via Schema"): technique that uses structured data formats—such as JSON, XML, or database schemas—to guide large language models (LLMs) to produce precise, consistent, and machine-readable outputs. 
In this Vet-App, I have implemented the LLM schema engineering pattern by using Pydantic models (to build domain entities), and the Instructor library (for structured LLM outputs). 


# Software Architecture Patterns

* **Hexagonal Architecture**:
* **Domain Driven Design**:
* **Use of JS instead of TS**


# Solution Architecture Patterns

* **Postgre DB**: The structured and sensible nature of the data involved (medical), requires solid ACID properties.
* **Gemini LLM**: 
