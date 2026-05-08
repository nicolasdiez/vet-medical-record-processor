# Ubiquitous Language

## Entities
*Concepts that have a unique identity and a lifecycle.*

* **Pet**: The animal patient receiving medical care. It is identified by a unique ID and contains static information such as name, species, and breed.
* **MedicalRecord**: An individual clinical encounter, visit, or diagnosis. It is uniquely identifiable and belongs to a specific `Pet`. It captures what happened during a specific point in time.

## Value Objects
*Immutable objects defined by their attributes rather than a unique identity.*

* **Vitals**: A collection of physiological measurements taken during a medical encounter (e.g., weight, temperature, heart rate, respiratory rate).
* **Medication**: Detailed information about a prescribed treatment, including the drug name, dosage, frequency, and duration.

## Supporting Concepts
*Transient or infrastructure-related concepts used for data processing.*

* **ClinicalDocument**: The raw, unstructured source file (PDF, Word or Image) provided by the veterinarian. It acts as a data container that is processed to extract domain entities.