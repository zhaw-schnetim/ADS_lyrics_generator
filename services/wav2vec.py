import json
import os.path

import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from datetime import datetime
import torch


def transcribe(audio_file_name: str):
    path = "results/output/" + audio_file_name + "/" + "vocals.wav"

    audio, rate = librosa.load(path, sr=16000)
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
    input_values = tokenizer(audio, return_tensors="pt").input_values
    logits = model(input_values).logits
    prediction = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(prediction)[0]

    path = os.path.join('results/transcripts/', audio_file_name)
    os.mkdir(path)
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    with open(path + "/transcript_" + str(ts).replace(".", "_") + ".txt", 'w') as fp:
        fp.write(transcription)

    path = os.path.join('results/information/', audio_file_name)
    os.mkdir(path)
    with open(path + "/result.json", 'w') as fp:
        result_json = {"transcribed_lyrics": transcription}
        json.dump(result_json, fp)
