import numpy as np
import sounddevice as sd
import json
import time

# Load the notes from the JSON file
with open('notes.json', 'r') as file:
    notes_mapping = json.load(file)

def play_tone(freqs, duration, waveform='square', sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if waveform == 'sine':
        notes = [np.sin(2 * np.pi * freq * t) for freq in freqs]
    elif waveform == 'square':
        notes = []
        for freq in freqs:
            period = int(sample_rate / freq)
            note = np.hstack((np.ones(period // 2), -1 * np.ones(period // 2)))
            note = np.tile(note, int(len(t) / period))
            note = np.resize(note, len(t))
            notes.append(note)
    else:
        raise ValueError("Invalid waveform. Choose 'sine' or 'square'.")
    
    chord = np.vstack(notes)
    chord = np.sum(chord, axis=0) / len(freqs)

    sd.play(chord, sample_rate)
    sd.wait()

def play_melody(melody, waveform='square', tempo=120, sample_rate=44100):
    duration_mapping = {'whole': 4, 'half': 2, 'quarter': 1, 'eighth': 0.5, 'sixteenth': 0.25}

    for note in melody:
        if note[0] == 'wait':
            duration = duration_mapping[note[1]] * 60 / tempo
            time.sleep(duration)  # Pause for the duration of the wait
        else:
            duration = duration_mapping[note[1]] * 60 / tempo
            frequencies = [notes_mapping[note_name] for note_name in note[0]]
            play_tone(frequencies, duration, waveform, sample_rate)
