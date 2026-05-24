# 🚀 Future Improvements & Next Steps

While this MVP is fully functional and demonstrates the core architecture, the following enhancements are planned to elevate the system to an enterprise-grade production standard.


### 1. Enforce Controlled Vocabularies via Constrained Decoding
To prevent the LLM from generating variations of the same concept (e.g., "perro", "canino", "dog"), we will use Pydantic `Enum` classes. This tightly couples the LLM's constrained decoding to our domain rules, ensuring absolute data consistency in the database.

```python
class Species(str, Enum):
    DOG = "dog"
    CAT = "cat"
class Pet(BaseModel):
    # The LLM is now mathematically forced to output exactly one of the Enum values
    species: Species = Field(..., description="Species of the animal")
```


### 2. LLM Call Resilience (Retry Mechanisms)
AI provider APIs can suffer from transient errors, timeouts, or rate limits. Implement exponential backoff and retry logic (e.g., using the Python `Tenacity` library) wrapping the Gemini API calls. This ensures the application gracefully recovers from temporary network failures without breaking the user experience.

```python
from tenacity import retry, stop_after_attempt, wait_exponential
# Retries up to 3 times, waiting 2s, then 4s, then 8s between attempts
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def process_document_with_llm(text_content: str):
    return client.chat.completions.create(...) # Gemini API call via instructor
```


### 3. AI Observability & Prompt Tracing
Integrate a tracing tool (such as Langfuse, Arize, or OpenTelemetry) to monitor LLM interactions in production. This provides visibility into token usage, latency, and exact prompt/response pairs, which is critical for debugging edge cases where the LLM might hallucinate or fail to parse a specific clinic's format.

```python
from langfuse.decorators import observe
@observe() # Automatically traces the execution, inputs, and outputs of this specific LLM call
def extract_entities_from_clinical_text(text: str) -> Pet:
    # LLM logic here
    pass
```


### 4. Cloud Object Storage & Audit Trails
Currently, the system processes documents on the fly. For a production clinical environment, the original uploaded files (PDFs, images) should be persisted in an object storage service (e.g., AWS S3, Google Cloud Storage). The generated URL should be linked to the `MedicalRecord` entity to maintain a legal audit trail and allow veterinarians to compare the AI extraction against the original source document at any time.

```python
from pydantic import HttpUrl
class MedicalRecord(BaseModel):
    id: str = Field(...)
    # ... existing fields ...
    source_document_url: Optional[HttpUrl] = Field(
        None, 
        description="Immutable AWS S3 / GCS URL linking to the original uploaded document for legal auditing."
    )
```


### 5. Authentication & Role-Based Access Control (RBAC)
Given the sensitive nature of medical data, implement JWT-based authentication (using FastAPI's security utilities) to ensure only authorized veterinary staff can process documents or review records.

```python
# FastAPI dependency injection for strict role validation
@router.post("/process")
async def process_document(file: UploadFile, current_user = Depends(require_role("veterinarian"))):
    pass
```


### 6. Automated Database Migrations
As the Domain Models evolve (adding new fields or entities), the database schema needs to adapt without losing data. Introduce `Alembic` (which integrates natively with SQLAlchemy) to manage schema changes programmatically. This is also the necessary stepping stone for the planned migration from SQLite to PostgreSQL.

```python
# Generate and apply schema changes safely via CLI
alembic revision --autogenerate -m "Add species enum" && alembic upgrade head
```


### 7. E2E Testing with Testcontainers
While the Use Cases are easily unit-tested via mocked repositories, adding Integration/E2E tests using `Testcontainers` would allow spinning up temporary, isolated Docker containers (e.g., a real PostgreSQL instance) to test the database adapters and API endpoints automatically in a CI/CD pipeline.

```python
from testcontainers.postgres import PostgresContainer
# Spin up an ephemeral Postgres container for isolated integration tests
with PostgresContainer("postgres:15-alpine") as postgres:
    engine = create_engine(postgres.get_connection_url())
```