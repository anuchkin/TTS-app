import threading

import torch
import sounddevice as sd
import soundfile as sf


e = threading.Event()

language = 'ru'
model_id = 'v4_ru'
speaker = 'xenia' # xenia, aidar, baya
sample_rate = 48000
device = torch.device('cpu')


model, _ = torch.hub.load(
	repo_or_dir='snakers4/silero-models',
	model='silero_tts',
	language=language,
	speaker=model_id
)

output_file = 'output.wav'
model.to(device)  # gpu or cpu


def voice(text: str):
	audio = model.apply_tts(
		text=text,
		speaker=speaker,
		sample_rate=sample_rate
	)
	
	sd.play(audio, sample_rate)
	e.wait(timeout=None)
	e.clear()
	sd.stop()

def save_voice(text: str):
	audio = model.apply_tts(
			text=text,
			speaker=speaker,
			sample_rate=sample_rate
	)

	sf.write(output_file, audio, sample_rate)

def voice_and_save(text: str):
	audio = model.apply_tts(
			text=text,
			speaker=speaker,
			sample_rate=sample_rate
	)

	sf.write(output_file, audio, sample_rate)

	sd.play(audio, sample_rate)
	e.wait(timeout=None)
	e.clear()
	sd.stop()