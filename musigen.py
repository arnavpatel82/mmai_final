import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy



processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")


inputs = processor(
    text=["catchy EDM beat that is danceable and has a high bpm"],
    padding=True,
    return_tensors="pt",
)
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=1, max_new_tokens=1024)

sampling_rate = model.config.audio_encoder.sampling_rate

# Prepare waveform: (channels, samples)
waveform = audio_values[0, 0].unsqueeze(0)

# Resample to 48000 Hz if necessary
if sampling_rate != 48000:
    resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=48000)
    waveform = resampler(waveform)
    sampling_rate = 48000  # Update the variable

# Save the resampled waveform
waveform = waveform.squeeze(0)  # back to (samples,)
scipy.io.wavfile.write("media/musicgen_out.wav", rate=sampling_rate, data=waveform.numpy())

