// src/frontend/src/components/PetHistorySearch.jsx

import { useState } from 'react';
import { getPetMedicalRecords } from '../services/api';
import toast from 'react-hot-toast';

export default function PetHistorySearch() {
  const [petId, setPetId] = useState('');
  const [records, setRecords] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!petId.trim()) return;

    try {
      setIsLoading(true);
      setRecords(null); // Clear previous results
      
      const data = await getPetMedicalRecords(petId.trim());
      
      // Sort records by date descending (newest first)
      const sortedRecords = (data || []).sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      });
      
      setRecords(sortedRecords);
      
      if (sortedRecords.length === 0) {
        toast.error("No records found for this Pet ID.");
      } else {
        toast.success(`Found ${sortedRecords.length} records!`);
      }

    } catch (error) {
      console.error("Search error:", error);
      toast.error(error.message || "Could not retrieve history.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto mt-12 bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
        🔍 Lookup Clinical History
      </h3>
      
      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-3 mb-8">
        <input 
          type="text" 
          placeholder="Enter Pet ID (e.g., 123e4567-...)" 
          value={petId}
          onChange={(e) => setPetId(e.target.value)}
          className="flex-grow px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
        <button 
          type="submit"
          disabled={isLoading || !petId.trim()}
          className="px-6 py-2 bg-gray-800 text-white font-medium rounded-md hover:bg-gray-700 transition-colors disabled:opacity-50"
        >
          {isLoading ? "Searching..." : "Search"}
        </button>
      </form>

      {/* Timeline Results */}
      {records && records.length > 0 && (
        <div className="relative border-l-2 border-blue-200 ml-4 pl-6 space-y-8">
          {records.map((record, index) => (
            <div key={record.id || index} className="relative">
              
              {/* Timeline Dot */}
              <div className="absolute -left-[31px] top-1 h-4 w-4 rounded-full bg-blue-500 border-4 border-white shadow-sm"></div>
              
              {/* Record Card */}
              <div className="bg-gray-50 border border-gray-100 rounded-lg p-4 shadow-sm">
                <span className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-1 block">
                  {new Date(record.date).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}
                </span>
                
                <p className="text-gray-800 font-medium mb-3">{record.diagnosis}</p>
                
                {/* Vitals Summary */}
                {record.vitals && (
                  <div className="flex gap-4 mb-3 text-sm text-gray-600 bg-white p-2 rounded border border-gray-100">
                    {record.vitals.weight_kg && <span>⚖️ {record.vitals.weight_kg} kg</span>}
                    {record.vitals.temperature_c && <span>🌡️ {record.vitals.temperature_c} °C</span>}
                  </div>
                )}

                {/* Medications List */}
                {record.medications && record.medications.length > 0 && (
                  <div className="mt-2">
                    <span className="text-xs font-semibold text-gray-500 uppercase">Medications:</span>
                    <ul className="mt-1 space-y-1">
                      {record.medications.map((med, idx) => (
                        <li key={idx} className="text-sm text-gray-700 flex items-center gap-2">
                          💊 <b>{med.name}</b> - {med.dosage} ({med.frequency}) {med.duration && `for ${med.duration}`}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}