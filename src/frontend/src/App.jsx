// src/frontend/src/App.jsx
import { useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import UploadZone from './components/UploadZone';
import DocumentViewer from './components/DocumentViewer';
import MedicalRecordEditor from './components/MedicalRecordEditor';
import PetHistorySearch from './components/PetHistorySearch'; // NEW IMPORT
import { saveClinicalData } from './services/api';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedData, setExtractedData] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  // Handle successful document upload and AI extraction
  const handleUploadSuccess = (file, data) => {
    setSelectedFile(file);
    setExtractedData(data);
    toast.success("Document analyzed successfully!");
  };

  // Reset the workspace to upload a new document
  const resetWorkspace = () => {
    setSelectedFile(null);
    setExtractedData(null);
  };

  // Handle saving the validated data to the database
  const handleSaveData = async (validatedData) => {
    try {
      setIsSaving(true);
      
      // 1. Generate or retrieve unique IDs for the database
      const finalPetId = validatedData.pet.id || crypto.randomUUID();
      
      // 2. Prepare the payload matching the backend schema requirements
      const payload = {
        pet: {
          ...validatedData.pet,
          id: finalPetId
        },
        records: validatedData.medical_records.map(record => {
          
          // Sanitize Vitals: Convert empty strings to null, strings to numbers
          const sanitizedVitals = { ...record.vitals };
          Object.keys(sanitizedVitals).forEach(key => {
            if (sanitizedVitals[key] === "") {
              sanitizedVitals[key] = null;
            } else if (sanitizedVitals[key] !== null) {
              sanitizedVitals[key] = Number(sanitizedVitals[key]);
            }
          });

          // Sanitize Date: Fallback to today's date if missing to prevent DB errors
          const safeDate = record.date || new Date().toISOString().split('T')[0];

          return {
            ...record,
            date: safeDate,
            vitals: sanitizedVitals,
            pet_id: finalPetId, // Link the record to the correct pet
            id: record.id || crypto.randomUUID() // Generate a unique UUID for new records
          };
        })
      };

      // Call the API service
      await saveClinicalData(payload);

      // Show highly visible success pop-up toast
      toast.success("Data saved successfully to the database!", {
        duration: 6000, // Se mostrará durante 6 segundos (6000 ms)
        position: 'top-center', // Lo fuerza a salir en el centro de la pantalla
        style: {
          padding: '24px', // Más grande
          fontSize: '18px', // Letra más grande
          fontWeight: 'bold',
          backgroundColor: '#10B981', // Fondo verde esmeralda llamativo
          color: 'white',
          minWidth: '400px',
          textAlign: 'center',
        },
        icon: '🎉', // Cambiamos el icono por defecto
      });
      
      resetWorkspace();

    } catch (error) {
      console.error("Save error:", error);
      // Show error toast
      toast.error(`Error saving data:\n\n${error.message}`, { duration: 6000 });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col font-sans">
      
      {/* Toast notifications container */}
      <Toaster position="top-right" />
      
      {/* Header section */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center shadow-sm">
        <div>
          <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-2xl">🐾</span> VetRecords Smart Processor
          </h1>
        </div>
        {selectedFile && (
          <button 
            onClick={resetWorkspace}
            disabled={isSaving}
            className="text-sm font-medium text-gray-500 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-md transition-colors disabled:opacity-50"
          >
            Upload Another Clinical Document
          </button>
        )}
      </header>

      {/* Main content area */}
      <main className="flex-grow p-6">
        {!selectedFile ? (
          // Initial State: Upload screen + Search History
          <div className="min-h-[calc(100vh-120px)] flex flex-col justify-center items-center py-10">
            
            {/* Top section: Upload */}
            <div className="w-full flex flex-col items-center">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Smart Clinical Workspace</h2>
                <p className="text-gray-500 max-w-md mx-auto">
                  Upload a new document to extract medical records automatically, or look up an existing patient's clinical history.
                </p>
              </div>
              <UploadZone onUploadSuccess={handleUploadSuccess} />
            </div>

            {/* Divider */}
            <div className="w-full max-w-3xl my-12 flex items-center text-gray-300">
              <div className="flex-grow border-t border-gray-300"></div>
              <span className="px-4 text-sm font-medium text-gray-400">OR</span>
              <div className="flex-grow border-t border-gray-300"></div>
            </div>

            {/* Bottom section: Search History (Step 34) */}
            <div className="w-full flex flex-col items-center">
              <PetHistorySearch />
            </div>

          </div>
        ) : (
          // Active State: Split screen view (PDF + Editor)
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full max-w-[1600px] mx-auto">
            
            {/* Left side: PDF Viewer */}
            <section className="flex flex-col">
              <DocumentViewer file={selectedFile} />
            </section>

            {/* Right side: Editor */}
            <section className="flex flex-col bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-[800px]">
              <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <h3 className="font-semibold text-gray-700">
                  {isSaving ? "⏳ Saving to Database..." : "✍️ Medical Record Editor"}
                </h3>
              </div>
              
              <div className={`flex-grow overflow-hidden ${isSaving ? "opacity-50 pointer-events-none" : ""}`}>
                <MedicalRecordEditor 
                  initialData={extractedData} 
                  onSave={handleSaveData} 
                />
              </div>
              
            </section>

          </div>
        )}
      </main>
    </div>
  );
}

export default App;