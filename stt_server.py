from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import uvicorn
import tempfile
import os

app = FastAPI(title="VoiceOps - STT Engine")

# We use 'base.en' for ultra-low latency. 
# It runs blazingly fast on a dedicated GPU.
print("Loading Faster-Whisper onto GPU...")
model = WhisperModel("base.en", device="cuda", compute_type="float16")
print("Engine ready.")

@app.post("/v1/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Save the incoming audio payload temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Transcribe the audio
        segments, _ = model.transcribe(tmp_path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return {"transcript": text.strip()}
    finally:
        # Clean up the temp file to prevent memory leaks
        os.remove(tmp_path)

if __name__ == "__main__":
    # Host on 0.0.0.0 so your Mac can access it over the local network
    uvicorn.run(app, host="0.0.0.0", port=8000)