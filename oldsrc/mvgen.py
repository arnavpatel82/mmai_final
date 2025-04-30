from transformers import ClapModel, ClapProcessor
import torch
import torchaudio

# Load model
processor = ClapProcessor.from_pretrained("laion/clap-htsat-fused")
model = ClapModel.from_pretrained("laion/clap-htsat-fused")

# Load audio
waveform, sample_rate = torchaudio.load('media/musicgen_out.wav')

# Preprocess and encode
inputs = processor(audios=waveform, sampling_rate=sample_rate, return_tensors="pt")
embedding = model.get_audio_features(**inputs)

print(embedding)