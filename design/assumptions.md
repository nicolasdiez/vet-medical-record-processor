### Pet Identity Resolution Heuristic (MVP vs. Future Iterations)

**Assumption:** During Phase 1 (AI Processing & Extraction), the system attempts to automatically reconcile the extracted pet with existing records in the database to prevent duplicates. For this MVP, we assume that a pet can be identified by the combination of its `name` and `species` (e.g., "Bella" + "Dog").

**Known Limitation:** We acknowledge that this is an imperfect heuristic that could lead to collisions (false positives), as it is highly probable for a veterinary clinic to have multiple patients of the same species sharing common names.

**Justification:** Unstructured clinical documents (PDFs, images) often lack strict unique identifiers like microchip numbers in the immediate text snippet. This heuristic provides a functional, frictionless "happy path" to demonstrate the backend's automated reconciliation orchestration without over-engineering the MVP.

**Future Iteration (V2):** To achieve robust identity resolution, future versions will:
1. Implement compound matching by extracting and cross-referencing `Pet Name` + `Owner Contact Info` (Email/Phone).
2. Shift the final reconciliation responsibility entirely to the "Human-in-the-Loop" UI. The backend will return a list of "Potential Matches," allowing the veterinarian to manually link the extracted data to the correct existing patient profile before persisting.