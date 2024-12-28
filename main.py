# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 17:03:40 2024

@author: Rob
"""

import os
from fastapi import FastAPI, HTTPException
import openai

input_type = "text"

# Initialize FastAPI app
app = FastAPI()

# OpenAI API Key
client = openai.OpenAI(
    api_key="sk",  # This is the default and can be omitted
)

@app.get("/")
def root():
    return {"message": "Welcome to the Grin&Go App Backend"}
    
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
    