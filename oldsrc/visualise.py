import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter

# 1. Load Audio
filename = "media/classical.00000.au"  # Change this
y, sr = librosa.load(filename)

# 2. Generate Spectrogram
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
S_dB = librosa.power_to_db(S, ref=np.max)

# 3. Plot Spectrogram
plt.figure(figsize=(10, 8))
librosa.display.specshow(S_dB, sr=sr, cmap='magma')  # Try 'viridis', 'plasma', 'inferno' too
plt.axis('off')  # No axes
plt.tight_layout(pad=0)
plt.savefig('spectrogram_raw.png', bbox_inches='tight', pad_inches=0)
plt.close()

# 4. Artistic Post-Processing (Optional)
img = Image.open('spectrogram_raw.png')

# Apply artistic filters (choose what feels right)
img = img.filter(ImageFilter.GaussianBlur(radius=2))  # soft blur
img = img.filter(ImageFilter.CONTOUR)                 # edge contour
# img = img.transpose(Image.FLIP_LEFT_RIGHT)          # mirror effect (optional)

# 5. Save Final Art
img.save('spectrogram_art.png')
print("Art generated and saved as 'spectrogram_art.png'!")