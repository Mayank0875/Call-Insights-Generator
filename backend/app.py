from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import aiohttp
import os
import tempfile
import shutil
from typing import Optional
import urllib.parse
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

async def download_audio_from_url(url: str, temp_dir: str) -> str:
    """
    Download audio from URL with special handling for GitHub and other platforms
    """

    if "github.com" in url and "/blob/" in url:
        url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    _, ext = os.path.splitext(filename)
    if not ext:
        ext = ".wav"
    
    temp_path = os.path.join(temp_dir, f"downloaded_audio{ext}")
    
    async with aiohttp.ClientSession() as session:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            
            async with session.get(url, headers=headers, timeout=30) as response:
                if not response.ok:
                    raise HTTPException(status_code=response.status, 
                                       detail=f"Failed to fetch audio from URL. Status: {response.status}")
                
                content_type = response.headers.get("Content-Type", "")
                valid_types = ["audio/", "video/", "application/octet-stream", "binary/"]
                
                if (content_type and 
                    not any(content_type.startswith(t) for t in valid_types) and
                    not ext.lower() in ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac']):
                    print(f"Warning: Content type '{content_type}' might not be audio")
                

                content = await response.read()
                
                with open(temp_path, "wb") as f:
                    f.write(content)
                
                if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
                    raise HTTPException(status_code=400, detail="Downloaded audio file is empty")
                
                return temp_path
                
        except aiohttp.ClientError as e:
            raise HTTPException(status_code=400, detail=f"Error downloading audio: {str(e)}")


@app.post("/process-audio-url/", response_model=AudioToTextResponse)
async def process_audio_url(request: URLRequest):
    url = request.url
    temp_dir = tempfile.mkdtemp()
    
    try:
        temp_path = await download_audio_from_url(url, temp_dir)
        result = convert_audio_to_text_and_analyze(temp_path)
        
        return result
    
    finally:
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Error cleaning up temporary directory: {e}")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)