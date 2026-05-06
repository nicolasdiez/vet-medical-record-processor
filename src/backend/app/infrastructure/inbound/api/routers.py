from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/records", tags=["Medical Records"])

class UploadResponse(BaseModel):
    filename: str
    status: str
    message: str

@router.post("/upload", response_model=UploadResponse)
async def upload_record(file: UploadFile = File(...)):
    """
    Mock endpoint to receive a medical record file from the frontend.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    # TODO: Pass the file to the Application Layer (Use Case) here
    
    return UploadResponse(
        filename=file.filename,
        status="success",
        message="File received successfully and is pending processing."
    )