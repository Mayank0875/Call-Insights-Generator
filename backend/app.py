from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import aiohttp
import os
import tempfile
import shutil
from typing import Optional

from src.Model import CallAssistant
from src.Audio_Ingestion import transcribe_audio

app = FastAPI()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AudioToTextResponse(BaseModel):
    separate_format: str
    summary: str
    performance: str

class URLRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "Processing API"}

@app.post("/process-audio/", response_model=AudioToTextResponse)
async def process_audio(file: Optional[UploadFile] = File(None), url: Optional[str] = Form(None)):
    if not file and not url:
        raise HTTPException(status_code=400, detail="Either file or URL must be provided")
    

    temp_dir = tempfile.mkdtemp()
    temp_path = None
    
    try:
        if file:
            content_type = file.content_type
            if not content_type or not content_type.startswith("audio/"):
                raise HTTPException(status_code=400, detail="Uploaded file is not an audio file")
            
            temp_path = os.path.join(temp_dir, file.filename)
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        

        elif url:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as response:
                        if not response.ok:
                            raise HTTPException(status_code=400, detail="Failed to fetch audio from URL")
                        
                        content_type = response.headers.get("Content-Type", "")
                        if not content_type.startswith("audio/"):
                            raise HTTPException(status_code=400, detail="URL does not point to an audio file")
                        
                        temp_path = os.path.join(temp_dir, "downloaded_audio")
                        with open(temp_path, "wb") as f:
                            f.write(await response.read())
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")
        

        result = convert_audio_to_text_and_analyze(temp_path)
        
        return result
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def convert_audio_to_text_and_analyze(audio_path):
    
    transcript = transcribe_audio(audio_path)
    
    call_assistant = CallAssistant()
    structured_dialogue = call_assistant.generate_structured_dialogue(transcript)
    summary_prompt_template = call_assistant.generate_summary(structured_dialogue)
    performance_report_template = call_assistant.generate_performance_report(structured_dialogue)
    
    return AudioToTextResponse(
        separate_format=str(structured_dialogue),
        summary = str(summary_prompt_template),
        performance = str(performance_report_template)
    )

@app.post("/process-audio-url/", response_model=AudioToTextResponse)
async def process_audio_url(request: URLRequest):
    
    url = request.url
    temp_dir = tempfile.mkdtemp()
    temp_path = None
    
    try:

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if not response.ok:
                        raise HTTPException(status_code=400, detail="Failed to fetch audio from URL")
                    
        
                    content_type = response.headers.get("Content-Type", "")
                    if not content_type.startswith("audio/"):
                        raise HTTPException(status_code=400, detail="URL does not point to an audio file")
                    

                    temp_path = os.path.join(temp_dir, "downloaded_audio")
                    with open(temp_path, "wb") as f:
                        f.write(await response.read())
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")
        
        result = convert_audio_to_text_and_analyze(temp_path)
        
        return result
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)