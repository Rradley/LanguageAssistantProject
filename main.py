# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 17:03:40 2024

@author: Rob
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
import openai
import whisper
import tempfile
import os

input_type = "text"

# Initialize FastAPI app
app = FastAPI()

# Load Whisper model (you can use 'base', 'small', 'medium', or 'large')
whisperModel = whisper.load_model("small")

# OpenAI API Key
client = openai.OpenAI(
    api_key="sk-proj-",  # This is the default and can be omitted
)

@app.get("/")
def root():
    return {"message": "Welcome to the Grin&Go App Backend"}
 
"""   
@app.post("/chat/")
async def chat_with_gpt(input_type: str = Form(...), prompt: str = Form(None), file: UploadFile = None):
    try:
        if input_type == "text":
            # Handle text input
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return {"response": response.choices[0].message.content}

        elif input_type == "voice":
            # Handle voice input (convert audio to text)
            text = speech_to_text(file)  # Implement speech_to_text function
            response = openai.chat.completions.create(
                model="gpt-4o-realtime-preview-2024-12-17",
                messages=[{"role": "user", "content": text}],
            )
            return {"response": response.choices[0].message.content}

        else:
            raise HTTPException(status_code=400, detail="Invalid input type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""    
@app.post("/speak/")
async def speech_to_text(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(await file.read())
            temp_audio_path = temp_audio.name

        # Transcribe the audio using Whisper
        result = whisperModel.transcribe(temp_audio_path, language="es")  # Specify Spanish as the language
        transcription = result["text"]

        # Delete the temporary file
        os.remove(temp_audio_path)

        return {"transcription": transcription}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))