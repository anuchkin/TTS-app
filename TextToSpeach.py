import threading

import torch
import sounddevice as sd
import soundfile as sf


class TextToSpeach:
	""" A class for voicing text """
	def __init__(self) -> None:
		""" Basic __init__ """
		self.sd = sd
		
		self.language = 'ru'
		self.model_id = 'v4_ru'
		self.speaker = 'xenia' # xenia, aidar, baya
		self.sample_rate = 48000
		self.device = torch.device('cpu')

		self.e = threading.Event()

		self.model, _ = torch.hub.load(
			repo_or_dir='snakers4/silero-models',
			model='silero_tts',
			language=self.language,
			speaker=self.model_id
		)

		self.output_file = 'output.wav'
		self.model.to(self.device)  # gpu or cpu

	def voice(self, text: str) -> None:
		"""
		A method for voicing text

		Args:
			text (str): Text for voice-over
		
		Returns:
			None
		"""
		audio = self.model.apply_tts(
			text=text,
			speaker=self.speaker,
			sample_rate=self.sample_rate
		)
		
		self.sd.play(audio, self.sample_rate)
		self.e.wait(timeout=None)
		self.e.clear()
		self.sd.stop()

	def save_voice(self, text: str) -> None:
		"""
		A method for saving the spoken text to an audio file

		Args:
			text (str): Text for voice-over
		
		Returns:
			None
		"""
		audio = self.model.apply_tts(
				text=text,
				speaker=self.speaker,
				sample_rate=self.sample_rate
		)

		sf.write(self.output_file, audio, self.sample_rate)

	def voice_and_save(self, text: str):
		"""
		A method for voicing text and saving the voiced text to an audio file
		
		Args:
			text (str): Text for voice-over
		
		Returns:
			None
		"""
		audio = self.model.apply_tts(
				text=text,
				speaker=self.speaker,
				sample_rate=self.sample_rate
		)

		sf.write(self.output_file, audio, self.sample_rate)

		self.sd.play(audio, self.sample_rate)
		self.e.wait(timeout=None)
		self.e.clear()
		self.self.sd.stop()