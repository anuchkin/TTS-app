import threading

from TextToSpeach import TextToSpeach

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window

# Глобальные настройки
Window.size = (500, 500)
Window.clearcolor = (255/255, 186/255, 3/255, 1)
Window.title = "Конвертер"


class MyApp(App):

	def __init__(self):
		super().__init__()
		self.label = Label(text='Озвучивание текста')
		self.input_data = TextInput(hint_text='Введите озвучиваемый текст:', multiline=False)
		
		self.button_voice_over = Button(text="Озвучить!")
		self.button_voice_stop = Button(text="Остановить!")

		self.button_voice_over.bind(on_press=self.on_button_voice_over)
		self.button_voice_stop.bind(on_press=self.on_button_voice_stop)

	def on_button_voice_over(self, *args):
		text = self.input_data.text
		if text:
			self.thread_speak = threading.Thread(target=tts.voice_and_save, args=(text,))
			self.thread_speak.start()
	
	def on_button_voice_stop(self, *args):
		tts.e.clear()
		tts.sd.stop()


	def build(self):
		box = BoxLayout(orientation='vertical')
		box.add_widget(self.label)
		box.add_widget(self.input_data)
		box.add_widget(self.button_voice_over)
		box.add_widget(self.button_voice_stop)

		return box


# Запуск проекта
if __name__ == "__main__":
	tts = TextToSpeach()
	MyApp().run()