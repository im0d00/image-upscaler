from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uuid
from typing import Dict
import os
from pathlib import Path

app = FastAPI(title="Image Upscaler API")

# In-memory storage for demo purposes
# In production, use a database or cloud storage
tasks: Dict[str, dict] = {}
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload an image file for processing"""
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Generate unique upload ID
    upload_id = str(uuid.uuid4())

    # Save file
    file_path = UPLOAD_DIR / f"{upload_id}{file_ext}"
    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    # Store task info
    tasks[upload_id] = {
        "status": "uploaded",
        "filename": file.filename,
        "file_path": str(file_path)
    }

    return {"upload_id": upload_id, "filename": file.filename}


@app.post("/tasks/{upload_id}/start")
async def start_task(upload_id: str):
    """Start processing an uploaded image"""
    if upload_id not in tasks:
        raise HTTPException(status_code=404, detail="Upload not found")

    tasks[upload_id]["status"] = "processing"

    # In a real implementation, this would trigger async processing
    # For now, we'll simulate it

    return JSONResponse(
        status_code=202,
        content={"upload_id": upload_id, "status": "processing"}
    )


@app.get("/tasks/{upload_id}")
async def get_task_status(upload_id: str):
    """Get the status of a processing task"""
    if upload_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "upload_id": upload_id,
        "status": tasks[upload_id]["status"],
        "filename": tasks[upload_id].get("filename")
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
