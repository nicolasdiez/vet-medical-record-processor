import { useState } from 'react';
import UploadZone from './components/UploadZone';
import DocumentViewer from './components/DocumentViewer';
import MedicalRecordEditor from './components/MedicalRecordEditor';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedData, setExtractedData] = useState(null);

  // Callback receiving the file and JSON from UploadZone
  const handleUploadSuccess = (file, data) => {
    setSelectedFile(file);
    setExtractedData(data);
  };

  // Reset to the initial screen
  const resetWorkspace = () => {
    setSelectedFile(null);
    setExtractedData(null);
  };

  // Dummy save function for Step 28 (Step 32 will make the API call)
  const handleSaveData = (validatedData) => {
    console.log("Data ready to be sent to DB:", validatedData);
    alert("Check the browser console to see the validated data!");
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col font-sans">
      
      {/* Fixed Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 flex justify-between items-center shadow-sm">
        <div>
          <h1 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <span className="text-2xl">🐾</span> VetRecords Smart Processor
          </h1>
        </div>
        {selectedFile && (
          <button 
            onClick={resetWorkspace}
            className="text-sm font-medium text-gray-500 hover:text-gray-800 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-md transition-colors"
          >
            Upload Another File
          </button>
        )}
      </header>

      <main className="flex-grow p-6">
        {!selectedFile ? (
          // STATE 1: Centered initial screen
          <div className="h-[calc(100vh-120px)] flex flex-col justify-center items-center">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Automate Clinical Data Entry</h2>
              <p className="text-gray-500 max-w-lg mx-auto">Upload a veterinary history in PDF or image format. The Smart Processor will extract the pet details and medical records automatically.</p>
            </div>
            <UploadZone onUploadSuccess={handleUploadSuccess} />
          </div>
        ) : (
          // STATE 2: Split Screen view
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full max-w-[1600px] mx-auto">
            
            {/* Left Column: PDF Viewer */}
            <section className="flex flex-col">
              <DocumentViewer file={selectedFile} />
            </section>

            {/* Right Column: Editor */}
            <section className="flex flex-col bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-[800px]">
              <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
                <h3 className="font-semibold text-gray-700">✍️ Medical Record Editor</h3>
              </div>
              
              {/* Insert the MedicalRecordEditor here */}
              <MedicalRecordEditor 
                initialData={extractedData} 
                onSave={handleSaveData} 
              />
              
            </section>

          </div>
        )}
      </main>
    </div>
  );
}

export default App;