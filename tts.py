import torch
import sounddevice as sd
import time
from pypdf import PdfReader

language = 'ru'
model_id = 'v4_ru'
speaker = 'xenia' # xenia, aidar, baya
sample_rate = 48000
device = torch.device('cpu')

reader = PdfReader("Кибердзюцу.pdf")

number_of_pages = len(reader.pages) # 223

list_texts = []
simple_text = ""
number_page = 19

correct_words_list = {
	"вопервых": "воп+ервых",
	"всё": "вс+ё",
	"вовторых": "вовтор+ых",
	"виновниками": "вин+овниками",
	"политики": "пол+итики",
	"безопасностью": "безоп+астностью",
	"те": "т+е",
	"или": "+или",
	"опасностей": "оп+асностей",
	"более": "б+олее",
	"ниндзя": "н+индзя",
	"хакерах": "х+акерах",
	"королевы": "корол+евы",
	"то": "т+о",
	"найдете": "найд+ете",
	"области": "+области",
	"идей": "ид+ей",
	"оригинальных": "оригин+альных",
	"уже": "уж+е",
	"другие": "друг+ие",
	"организации": "организ+ации",
	"организациях": "организ+ациях",
	"средневековыми": "средневек+овыми",
	"кибердзюцу": "кибердз+юцу",
	"некоторые": "н+екоторые",
	"использования": "исп+ользования",
	"устранения": "устран+ения",
	"уверен": "ув+ерен",
	"реализации": "реализ+ации",
	"работать": "раб+отать",
	"некоторое": "н+екоторое",
	"устоявшимся": "усто+явшимся",
	"наемными": "на+емными",
	"крестьян": "кресть+ян",
	"самураев": "самур+аев",
	"несколько": "н+есколько",
	"конфликтов": "конфл+иктов",
	"трактате": "тракт+ат+е",
	"внимателен": "вним+ателен",
	"информацию": "информ+ацию",
	"постепенно": "постеп+енно",
	"ученику": "ученик+у",
	"этой": "+этой",
	"некоторые": "н+екоторые",
	"действительно": "действ+ительно",
	"наверняка": "наверняк+а",
	"устоявшимся": "усто+явшимся",
	"поразному": "пор+азному",
	"нанимали": "наним+али",
	"методы": "м+етоды",
	"таким": "так+им",
	"противник": "прот+ивник",
	"внимателен": "вним+ателен",
	"наносить": "нанос+ить",
	"смотрит": "см+отрит",
	"агенты": "аг+енты",
	"бреши": "бр+еши",
	"совершения": "соверш+ения",
	"саботажа": "сабот+ажа",
	"поджога": "подж+ога",
	"мастерство": "мастерств+о",
	"методы": "м+етоды",
	"он": "+он",
	"да": "д+а",
	"она": "он+а",
	"те": "т+е",
	"или": "+или",
	"иные": "ин+ые",
	"во": "в+о",
	"время": "вр+емя",
	"говорится": "говор+ится",
	"продолжительной": "продолж+ительной",
	"проникали": "проник+али",
	"они": "",
}

for page in range(200):
	page = reader.pages[number_page]
	number_page += 1

	example_text = page.extract_text()
	# print(example_text)

	for i in range(301):
		simbol = f"[{i}]"
		example_text = example_text.replace(simbol, " ")

	example_text = example_text.replace("  ", "")

	example_text = example_text.lower()


	for uncorrect_word, correct_word in correct_words_list.items():
		example_text = example_text.replace(uncorrect_word, correct_word)

	count_point = 0
	for simbol in example_text:
		if simbol == ".":
			simbol = "..."
			count_point += 1
		
		if simbol == "(" or simbol == ")":
			simbol = "..."
		
		if simbol == "—":
			simbol = "..."
		
		if simbol == "-":
			simbol = ""
		
		if simbol == "..." and count_point == 3:
			# simple_text += ".."
			list_texts.append(simple_text)
			example_text = example_text.replace(simple_text, "")
			simple_text = ""
			count_point = 0
		
		simple_text += simbol



print(len(list_texts))

model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
										  model='silero_tts',
										  language=language,
										  speaker=model_id)


model.to(device)  # gpu or cpu


def speak(text: str):
	audio = model.apply_tts(text=text,
						speaker=speaker,
						sample_rate=sample_rate)
	

	sd.play(audio, sample_rate)
	time.sleep((len
	(audio) / sample_rate) + 0.5)
	sd.stop()


number_sentence = 63
slice_list = int(number_sentence / 3)

if number_sentence != 0:
	list_texts = list_texts[slice_list:]

for text in list_texts:
	print(f"Номер предложения: {number_sentence}")
	speak(text)
	number_sentence += 3