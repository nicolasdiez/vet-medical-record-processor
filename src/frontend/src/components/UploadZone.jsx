import { useState, useRef } from 'react';
import { processClinicalDocument } from '../services/api';

export default function UploadZone() {
    // State management without TypeScript annotations
    const [isDragging, setIsDragging] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [extractionResult, setExtractionResult] = useState(null);
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
        if (files.length > 0) {
            await uploadFile(files[0]);
        }
    };

    const handleFileSelect = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            await uploadFile(e.target.files[0]);
        }
    };

    const uploadFile = async (file) => {
        setIsLoading(true);
        setError(null);
        setExtractionResult(null);

        try {
            const data = await processClinicalDocument(file);
            setExtractionResult(data);
        } catch (err) {
            setError(err.message || 'Failed to process document');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-8 max-w-4xl mx-auto">
            {/* Upload Area */}
            <div
                className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
                    ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
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
                    <div className="text-blue-600 font-semibold animate-pulse">
                        Processing document with AI...
                    </div>
                ) : (
                    <div className="text-gray-600">
                        <span className="font-semibold text-blue-600">Click to upload</span> or drag and drop
                        <p className="text-sm mt-2 text-gray-500">PDF, PNG, or JPG</p>
                    </div>
                )}
            </div>

            {/* Error Message */}
            {error && (
                <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md">
                    {error}
                </div>
            )}

            {/* Results Area (Phase 1 Mock visualization) */}
            {extractionResult && (
                <div className="mt-8">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4">AI Extraction Result (Mock)</h3>
                    <div className="bg-gray-900 rounded-lg p-4 overflow-auto max-h-96 text-left">
                        <pre className="text-green-400 text-sm font-mono">
                            {JSON.stringify(extractionResult, null, 2)}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    );
}