import { useState, useRef } from 'react';
import { processClinicalDocument } from '../services/api';

export default function UploadZone({ onUploadSuccess }) {
    const [isDragging, setIsDragging] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        setIsDragging(false);
        const files = Array.from(e.dataTransfer.files);
        if (files.length > 0) await uploadFile(files[0]);
    };

    const handleFileSelect = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            await uploadFile(e.target.files[0]);
        }
    };

    const uploadFile = async (file) => {
        setIsLoading(true);
        setError(null);

        try {
            // API call (we will update this to the real endpoint later)
            const data = await processClinicalDocument(file);
            // Pass the file and extracted data up to the parent (App.jsx)
            onUploadSuccess(file, data); 
        } catch (err) {
            setError(err.message || 'Failed to process document');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-2xl mx-auto w-full">
            <div
                className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-200
                    ${isDragging ? 'border-blue-500 bg-blue-50 scale-105' : 'border-gray-300 hover:border-gray-400 bg-white shadow-sm hover:shadow-md'}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current.click()}
            >
                <input
                    type="file"
                    ref={fileInputRef}
                    className="hidden"
                    accept=".pdf,.png,.jpg,.jpeg"
                    onChange={handleFileSelect}
                />
                
                {isLoading ? (
                    <div className="flex flex-col items-center space-y-4">
                        <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
                        <div className="text-blue-600 font-medium animate-pulse">
                            Processing clinical document...
                        </div>
                    </div>
                ) : (
                    <div className="text-gray-600 flex flex-col items-center">
                        <svg className="w-12 h-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                        </svg>
                        <span className="font-semibold text-blue-600 text-lg">Click to upload</span> 
                        <span>or drag and drop here</span>
                        <p className="text-sm mt-2 text-gray-400">Supported formats: PDF</p>
                    </div>
                )}
            </div>

            {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md flex items-center gap-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"></path></svg>
                    {error}
                </div>
            )}
        </div>
    );
}