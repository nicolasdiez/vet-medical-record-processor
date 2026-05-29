import { useState, useEffect } from 'react';

export default function DocumentViewer({ file }) {
  const [pdfUrl, setPdfUrl] = useState(null);

  useEffect(() => {
    // When a valid PDF is received, create a temporary local URL to display it
    if (file && file.type === "application/pdf") {
      const url = URL.createObjectURL(file);

      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPdfUrl(url);
      
      // Clean up memory when the component unmounts
      return () => URL.revokeObjectURL(url);
    }
  }, [file]);

  if (!file) return null;

  return (
    <div className="flex flex-col h-[800px] bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
        <h3 className="font-semibold text-gray-700 truncate" title={file.name}>
          📄 {file.name}
        </h3>
        <span className="text-xs text-gray-500 bg-gray-200 px-2 py-1 rounded-full">
          Original Document
        </span>
      </div>
      
      <div className="flex-grow bg-gray-100">
        {pdfUrl ? (
          <iframe
            src={`${pdfUrl}#toolbar=0&navpanes=0`} 
            className="w-full h-full border-none"
            title="PDF Viewer"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-gray-500 p-8 text-center">
            Preview is only available for PDF files.
          </div>
        )}
      </div>
    </div>
  );
}