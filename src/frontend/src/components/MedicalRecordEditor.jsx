import { useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';

// ============================================================================
// Sub-component: Handles a single Medical Record and its nested Medications
// ============================================================================
const RecordItem = ({ control, register, index, removeRecord }) => {
  const { fields: medFields, append: appendMed, remove: removeMed } = useFieldArray({
    control,
    name: `medical_records.${index}.medications`
  });

  return (
    <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg relative">
      <button 
        type="button" 
        onClick={() => removeRecord(index)}
        className="absolute top-4 right-4 text-red-500 hover:text-red-700 text-sm font-medium"
      >
        Remove
      </button>

      <h5 className="font-medium text-gray-700 mb-3">Record #{index + 1}</h5>
      
      {/* Date Section */}
      <div className="mb-4 w-1/3">
        <label className="text-xs font-medium text-gray-600 mb-1">Date</label>
        <input 
          type="date" 
          {...register(`medical_records.${index}.date`)}
          className="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Vitals Section (4 Fields matching VitalsDTO) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 bg-white p-3 border border-gray-100 rounded-md shadow-sm">
        <div className="flex flex-col">
          <label className="text-xs font-medium text-gray-600 mb-1">Weight (kg)</label>
          <input 
            type="text" 
            placeholder="e.g. 4.1"
            {...register(`medical_records.${index}.vitals.weight_kg`)}
            className="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="flex flex-col">
          <label className="text-xs font-medium text-gray-600 mb-1">Temp (°C)</label>
          <input 
            type="text" 
            placeholder="e.g. 38.5"
            {...register(`medical_records.${index}.vitals.temperature_c`)}
            className="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="flex flex-col">
          <label className="text-xs font-medium text-gray-600 mb-1">Heart Rate (bpm)</label>
          <input 
            type="text" 
            placeholder="e.g. 120"
            {...register(`medical_records.${index}.vitals.heart_rate_bpm`)}
            className="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        <div className="flex flex-col">
          <label className="text-xs font-medium text-gray-600 mb-1">Resp. Rate (bpm)</label>
          <input 
            type="text" 
            placeholder="e.g. 24"
            {...register(`medical_records.${index}.vitals.respiratory_rate_bpm`)}
            className="px-3 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>

      {/* Diagnosis Section */}
      <div className="flex flex-col mb-4">
        <label className="text-xs font-medium text-gray-600 mb-1">Diagnosis</label>
        <textarea 
          rows={3}
          {...register(`medical_records.${index}.diagnosis`)}
          className="px-3 py-2 text-sm border border-gray-300 rounded-md shadow-sm resize-y focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      {/* Nested Medications Section */}
      <div className="mt-4 border-t border-gray-200 pt-4">
        <div className="flex justify-between items-center mb-3">
          <label className="text-sm font-medium text-gray-700 flex items-center gap-1">
            💊 Medications
          </label>
          <button 
            type="button"
            onClick={() => appendMed({ name: '', dosage: '', frequency: '', duration: '' })}
            className="text-xs text-blue-600 hover:text-blue-800 font-medium bg-blue-50 px-2 py-1 rounded"
          >
            + Add Med
          </button>
        </div>

        {medFields.length === 0 && (
          <p className="text-xs text-gray-400 italic mb-2">No medications extracted.</p>
        )}

        {/* Dynamic List with Labels */}
        <div className="space-y-2">
          {medFields.length > 0 && (
            <div className="flex gap-2 items-center px-1">
              <label className="text-[10px] font-semibold text-gray-500 uppercase w-1/3">Name</label>
              <label className="text-[10px] font-semibold text-gray-500 uppercase w-1/5">Dosage</label>
              <label className="text-[10px] font-semibold text-gray-500 uppercase w-1/5">Freq</label>
              <label className="text-[10px] font-semibold text-gray-500 uppercase w-1/5">Duration</label>
              <div className="w-6"></div> {/* Spacer for the delete button */}
            </div>
          )}

          {medFields.map((med, medIndex) => (
            <div key={med.id} className="flex gap-2 items-start">
              <input 
                placeholder="e.g. Amoxicillin"
                {...register(`medical_records.${index}.medications.${medIndex}.name`)}
                className="w-1/3 px-2 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500"
              />
              <input 
                placeholder="e.g. 10mg"
                {...register(`medical_records.${index}.medications.${medIndex}.dosage`)}
                className="w-1/5 px-2 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500"
              />
              <input 
                placeholder="e.g. 2x/day"
                {...register(`medical_records.${index}.medications.${medIndex}.frequency`)}
                className="w-1/5 px-2 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500"
              />
              <input 
                placeholder="e.g. 7 days"
                {...register(`medical_records.${index}.medications.${medIndex}.duration`)}
                className="w-1/5 px-2 py-1.5 text-sm border border-gray-300 rounded-md shadow-sm focus:ring-blue-500"
              />
              <button 
                type="button"
                onClick={() => removeMed(medIndex)}
                className="px-2 py-1 text-gray-400 hover:text-red-600 transition-colors"
                title="Remove Medication"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// Main Editor Component
// ============================================================================
export default function MedicalRecordEditor({ initialData, onSave }) {
  
  const { register, control, handleSubmit, reset } = useForm({
    defaultValues: {
      pet: { id: '', name: '', species: '', breed: '' },
      medical_records: []
    }
  });

  const { fields: recordFields, append: appendRecord, remove: removeRecord } = useFieldArray({
    control,
    name: "medical_records"
  });

useEffect(() => {
    if (initialData) {
      const payload = initialData.data || initialData;

      // 1. Map keys safely, and then SORT by date descending (newest first)
      const safeRecords = (payload.extracted_records || [])
        .map(rec => ({
          ...rec,
          vitals: {
            weight_kg: rec.vitals?.weight_kg ?? '',
            temperature_c: rec.vitals?.temperature_c ?? '',
            heart_rate_bpm: rec.vitals?.heart_rate_bpm ?? '',
            respiratory_rate_bpm: rec.vitals?.respiratory_rate_bpm ?? ''
          },
          medications: rec.medications || []
        }))
        .sort((a, b) => {
          // Convert date strings to timestamps for comparison. 
          // If a date is missing, treat it as 0 (oldest) so it goes to the bottom.
          const timeA = a.date ? new Date(a.date).getTime() : 0;
          const timeB = b.date ? new Date(b.date).getTime() : 0;
          return timeB - timeA; // Descending order
        });

      reset({
        pet: { 
          ...(payload.extracted_pet || { name: '', species: '', breed: '' }), 
          id: payload.pet_id || '' 
        },
        medical_records: safeRecords
      });
    }
  }, [initialData, reset]);

  if (!initialData) {
    return (
      <div className="flex h-full items-center justify-center text-gray-500 p-8 text-center bg-gray-50">
        Waiting for AI extraction data...
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSave)} className="flex flex-col h-full bg-white">
      
      <div className="flex-grow overflow-y-auto p-6 space-y-8">
        
        {/* --- Pet Information Section --- */}
        <section>
          <h4 className="text-lg font-semibold text-gray-800 border-b pb-2 mb-4 flex items-center gap-2">
            🐾 Pet Information
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <div className="flex flex-col md:col-span-2">
              <label className="text-xs font-medium text-gray-500 mb-1">System ID</label>
              <input 
                readOnly
                placeholder="New record (ID will be generated upon saving)"
                {...register("pet.id")}
                className="px-3 py-1.5 text-sm bg-gray-100 border border-gray-200 rounded-md text-gray-500 cursor-not-allowed"
              />
            </div>

            <div className="flex flex-col">
              <label className="text-sm font-medium text-gray-700 mb-1">Name</label>
              <input 
                {...register("pet.name")}
                className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex flex-col">
              <label className="text-sm font-medium text-gray-700 mb-1">Species</label>
              <input 
                {...register("pet.species")}
                className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            
            <div className="flex flex-col md:col-span-2">
              <label className="text-sm font-medium text-gray-700 mb-1">Breed</label>
              <input 
                {...register("pet.breed")}
                className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </section>

        {/* --- Medical Record List Section --- */}
        <section>
          <div className="flex justify-between items-center border-b pb-2 mb-4">
            <h4 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              🩺 Medical Record List
            </h4>
            <button 
              type="button"
              onClick={() => appendRecord({ 
                date: '', 
                diagnosis: '', 
                vitals: { weight_kg: '', temperature_c: '', heart_rate_bpm: '', respiratory_rate_bpm: '' },
                medications: [] 
              })}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              + Add Record
            </button>
          </div>

          <div className="space-y-6">
            {recordFields.length === 0 && (
              <p className="text-gray-500 text-sm italic">No medical records extracted.</p>
            )}

            {recordFields.map((field, index) => (
              <RecordItem 
                key={field.id}
                control={control}
                register={register}
                index={index}
                removeRecord={removeRecord}
              />
            ))}
          </div>
        </section>

      </div>

      {/* Sticky Action Footer */}
      <div className="p-4 border-t border-gray-200 bg-gray-50 flex justify-end gap-3 mt-auto">
        <button 
          type="button"
          className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 font-medium"
        >
          Discard
        </button>
        <button 
          type="submit"
          className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 font-medium shadow-sm"
        >
          Save & Persist
        </button>
      </div>

    </form>
  );
}