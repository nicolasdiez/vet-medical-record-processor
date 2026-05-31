src/backend/
├── .dockerignore                                                     # Files/folders to exclude from the Docker build context
├── .env.dev                                                          # Environment variables for local development
├── .gitignore                                                        # Files/folders to exclude from Git version control
├── app/                                                              # Main application package
│   ├── application/                                                  # Application layer (Orchestration of domain logic)
│   │   └── use_cases/                                                # Business use cases implementation
│   │       ├── extract_clinical_data.py                              # Use case: Orchestrates PDF reading + LLM extraction
│   │       ├── get_pet_clinical_history.py                           # Use case: Retrieves pet data from the database
│   │       └── save_clinical_data.py                                 # Use case: Persists structured medical records
│   ├── config.py                                                     # Settings management (loads env variables)
│   ├── domain/                                                       # Core domain layer (No external dependencies allowed)
│   │   ├── entities.py                                               # Domain models with identity (e.g., Pet, MedicalRecord)
│   │   ├── ports/                                                    # Abstract interfaces (Contracts dictated by the domain)
│   │   │   ├── inbound/                                              # Inbound contracts (Interfaces for Use Cases)
│   │   │   │   └── interfaces.py                                     # Inbound interface definitions
│   │   │   └── outbound/                                             # Outbound contracts (Interfaces for DB, LLM, Extractors)
│   │   │       └── interfaces.py                                     # Outbound interface definitions
│   │   └── value_objects.py                                          # Immutable domain models (e.g., Weight, Vitals, Medication)
│   ├── infrastructure/                                               # Infrastructure layer (Concrete technical adapters)
│   │   ├── inbound/                                                  # Driving adapters (Trigger the application)
│   │   │   └── api/                                                  # Web layer implementation
│   │   │       ├── routers.py                                        # FastAPI HTTP endpoints (Controllers)
│   │   │       └── schemas.py                                        # Pydantic models for API Requests/Responses (DTOs)
│   │   └── outbound/                                                 # Driven adapters (Triggered by the application)
│   │       ├── gemini_medical_record_extractor.py                    # Adapter for LLM integration (Gemini + Instructor)
│   │       ├── pdf_text_extractor.py                                 # Adapter for processing PDFs (PyMuPDF)
│   │       └── persistence/                                          # Database implementation details
│   │           ├── database.py                                       # SQLAlchemy engine and session management
│   │           ├── models.py                                         # SQLAlchemy ORM schemas (Database tables)
│   │           ├── sql_medical_record_repository.py                  # Repository implementation for records
│   │           └── sql_pet_repository.py                             # Repository implementation for pets
│   └── main.py                                                       # FastAPI entry point, app initialization, and DI
├── backend_module_structure.txt                                      # Documentation artifact of the project's structure
├── Dockerfile                                                        # Instructions to build the backend Docker image
├── pytest.ini                                                        # Configuration settings for the Pytest testing framework
├── requirements.txt                                                  # Python dependencies file for pip
├── ruff.toml                                                         # Configuration file for Ruff (Python linter and formatter)
└── tests/                                                            # Testing suite
    ├── e2e/                                                          # End-to-End tests (testing the full stack, DB, and API)
    │   └── test_api.py                                               # E2E tests for the FastAPI endpoints
    ├── fixtures/                                                     # Test assets and dummy data
    │   ├── clinical_history_1.pdf                                    # Sample PDF used in tests
    │   └── clinical_history_2.pdf                                    # Additional sample PDF
    └── unit/                                                         # Unit tests (isolated testing of individual components)
        └── infrastructure/                                           # Unit tests for infrastructure components
            └── outbound/                                             # Unit tests for outbound adapters
                └── adapters/                                         # Adapter tests
                    ├── test_gemini_medical_record_extractor.py       # Unit tests for the LLM adapter
                    └── test_pdf_text_extractor.py                    # Unit tests for the PDF adapter