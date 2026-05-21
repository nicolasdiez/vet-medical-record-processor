// src/frontend/src/services/api.js
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Upload clinical document containing Pet's personal data and Pet´s medical records
export const processClinicalDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/clinical-documents/process`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
};

// Save the reviewed Pet's personal data and Pet's medical records 
export const saveClinicalData = async (payload) => {
    const response = await fetch(`${API_BASE_URL}/clinical-data`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    });

    if (!response.ok) {
        const errorData = await response.json();
        let errorMessage = errorData.detail || 'Failed to save clinical data';
        
        // If FastAPI returns an array of validation errors (Pydantic 422)
        if (Array.isArray(errorData.detail)) {
            // Map the array into a readable string: "body.records.0.vitals.weight_kg -> input should be a valid number"
            errorMessage = errorData.detail
                .map(err => `${err.loc.join('.')} -> ${err.msg}`)
                .join('\n');
        }
        
        throw new Error(errorMessage);
    }

    return await response.json();
};

// Fetch medical history for a specific pet
export const getPetMedicalRecords = async (petId) => {
    const response = await fetch(`${API_BASE_URL}/pets/${petId}/medical-records`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch medical history');
    }

    return await response.json();
};