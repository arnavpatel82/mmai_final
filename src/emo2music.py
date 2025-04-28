from transformers import pipeline
import pretty_midi
import random

emotion_classifier = pipeline("text-classification", 
                              model="nateraw/bert-base-uncased-emotion", 
                              return_all_scores=True)

def get_top_emotions(text):
    results = emotion_classifier(text)[0]
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    return sorted_results[:2]  # top 2 emotions

# emotion to music mapping defaults based on emotions
emotion_music_map = {
    "joy":      {"tempo": 140, "key": "C", "scale": "major", "instruments": [25, 26, 27]},  # Guitars
    "sadness":  {"tempo": 60,  "key": "A", "scale": "minor", "instruments": [0, 6, 8]},     # Pianos
    "anger":    {"tempo": 150, "key": "D", "scale": "minor", "instruments": [30, 31]},      # Distorted guitars
    "fear":     {"tempo": 70,  "key": "E", "scale": "minor", "instruments": [48, 49]},      # Strings
    "surprise": {"tempo": 110, "key": "G", "scale": "major", "instruments": [19, 18]},      # Organs
    "love":     {"tempo": 90,  "key": "F", "scale": "major", "instruments": [14, 11, 13]},  # Bells
}

# used to determine pitch. I had chatgpt generate this since i don't have any experience with music (so it might be inaccurate)
scale_notes = {
    'C_major': [60, 62, 64, 65, 67, 69, 71, 72],  # C D E F G A B C
    'C_minor': [60, 62, 63, 65, 67, 68, 70, 72],  # C D Eb F G Ab Bb C

    'A_major': [57, 59, 61, 62, 64, 66, 68, 69],  # A B C# D E F# G# A
    'A_minor': [57, 59, 60, 62, 64, 65, 67, 69],  # A B C D E F G A

    'D_major': [62, 64, 66, 67, 69, 71, 73, 74],  # D E F# G A B C# D
    'D_minor': [62, 64, 65, 67, 69, 70, 72, 74],  # D E F G A Bb C D

    'E_major': [64, 66, 68, 69, 71, 73, 75, 76],  # E F# G# A B C# D# E
    'E_minor': [64, 66, 67, 69, 71, 72, 74, 76],  # E F# G A B C D E

    'F_major': [65, 67, 69, 70, 72, 74, 76, 77],  # F G A Bb C D E F
    'F_minor': [65, 67, 68, 70, 72, 73, 75, 77],  # F G Ab Bb C Db Eb F

    'G_major': [67, 69, 71, 72, 74, 76, 78, 79],  # G A B C D E F# G
    'G_minor': [67, 69, 70, 72, 74, 75, 77, 79],  # G A Bb C D Eb F G
}

def interpolate_params(em1, em2):
    label1, score1 = em1['label'], em1['score']
    label2, score2 = em2['label'], em2['score']
    total = score1 + score2
    w1, w2 = score1 / total, score2 / total
    params1 = emotion_music_map.get(label1)
    params2 = emotion_music_map.get(label2)
    tempo = int(params1['tempo'] * w1 + params2['tempo'] * w2)
    key = params1['key'] if w1 >= w2 else params2['key']
    scale = params1['scale'] if w1 >= w2 else params2['scale']
    instruments = params1['instruments'] + params2['instruments']
    instrument = random.choice(instruments)
    return tempo, key, scale, instrument


def generate_midi(tempo, key, scale, program, velocity=100, output_file=None):
    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    instrument = pretty_midi.Instrument(program=program)
    note_pool = scale_notes.get(f"{key}_{scale}", scale_notes['C_major'])
    time = 0.0
    for _ in range(16):  
        pitch = random.choice(note_pool)
        duration = random.uniform(0.3, 0.7)
        note = pretty_midi.Note(velocity=velocity, pitch=pitch, start=time, end=time + duration)
        instrument.notes.append(note)
        time += duration
    midi.instruments.append(instrument)
    if output_file:
        midi.write(output_file)

def text_to_music(text, output_file=None):
    top2 = get_top_emotions(text)
    print("\nEmotion blend:")
    for emo in top2:
        print(f"  {emo['label']}: {emo['score']:.3f}")
    tempo, key, scale, instrument = interpolate_params(top2[0], top2[1])
    intensity = top2[0]['score']
    velocity = int(80 + intensity * 40) # scaling velocity to the intensity makes the output more unique to the given phrase
    print(f"\n Music settings -> Tempo: {tempo} | Key: {key} {scale} | Instrument: {instrument} | Velocity: {velocity}")
    generate_midi(tempo, key, scale, instrument, velocity, output_file)

text_inputs = "I’m heartbroken, but also strangely hopeful that things will get better someday."
text_to_music(text_inputs, output_file='media/output.mid')