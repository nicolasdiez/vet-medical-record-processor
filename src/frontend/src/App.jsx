// src/frontend/src/App.jsx
import { useState } from 'react';
import UploadZone from './components/UploadZone';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (file) => {
    console.log("File selected:", file.name);
    setSelectedFile(file);
    // Future step: Send to backend here
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <header className="text-center">
          <h1 className="text-3xl font-bold text-gray-800">Veterinary Records Processor</h1>
          <p className="text-gray-600 mt-2">Upload a clinical history to extract structured medical data.</p>
        </header>

        <main className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
          <UploadZone onFileSelect={handleFileSelect} />
          
          {selectedFile && (
            <div className="mt-4 p-4 bg-green-50 text-green-700 rounded-md border border-green-200">
              <p className="font-medium">File ready for processing:</p>
              <p className="text-sm">{selectedFile.name}</p>
            </div>
          )}
        </main>

      </div>
    </div>
  );
}

export default App;