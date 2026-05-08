const API_BASE_URL = 'http://localhost:8000/api/v1';

export const processClinicalDocument = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/clinical-documents/process`, {
        method: 'POST',
        body: formData,
        // The browser will automatically set 'multipart/form-data'
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
};