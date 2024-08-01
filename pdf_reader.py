from tts import *

from correct_accent_words import *
from numbers_into_words import *

from pypdf import PdfReader



class OpenPdf:
	""" Class OpenPdf """

	def __init__(self, path_to_book: str, page_number: int = 0,) -> None:
		"""
		Standard definition

		Args:
			page_number (int): The page from which the text will start to be voiced
			path_to_book (str): Path to book
		
		Returns:
			None
		"""
		self.reader = PdfReader(path_to_book)
		self.number_of_pages = len(self.reader.pages)

		self.path_to_book = path_to_book
		self.page_number = page_number
		self.last_page_number = self.number_of_pages - self.page_number
		self.sentences_for_voice_acting = []

	
	def text_correction(self) -> None:
		"""
		A method for correcting text before voicing
		"""
		def remove_extra_symbols(page_text: str) -> str:
			"""
			A method for removing unnecessary characters

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Clean text
			"""
			for i in range(1001):
				simbol = f"[{i}]"
				page_text = page_text.replace(simbol, " ")
			
			page_text = page_text.replace("-", "")

			page_text = page_text.replace(".", "..")

			page_text = page_text.replace("\xa0", " ")
			
			page_text = page_text.replace("  ", " ")

			return page_text

		def fixing_words_accent(page_text: str) -> str:
			"""
			The placement of accents in words from the dictionary "correct_words_dict"

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Text with correct accents
			"""
			for uncorrect, correct in correct_accent_words_dict.items():
				page_text = page_text.replace(f" {uncorrect} ", f" {correct} ")
			
			page_text = page_text.replace("  ", " ")

			return page_text

		def replacing_numbers_with_text(page_text: str) -> str:
			"""
			A method for replacing different numbers with text

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Text with numbers
			"""
			for number, number_text in numbers_into_words_dict.items():
				page_text = page_text.replace(number, number_text)
			
			page_text = page_text.replace("  ", " ")

			return page_text

		def fixing_punctuation(page_text: str) -> str:
			"""
			A method for correcting punctuation marks

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Text with corrected punctuation marks
			"""
			page_text = page_text.replace("(", ",")
			page_text = page_text.replace(")", ",")
			page_text = page_text.replace("—", ",")
			page_text = page_text.replace("—", ",")
			page_text = page_text.replace("»", ",")

			return page_text

		def splitting_into_sentences(page_text: str) -> list:
			"""
			A method for splitting into three sentences

			Args:
				page_text (str): Text from page
			
			Returns:
				list: The text is divided into three sentences in the list
			"""
			amount_sentences = 0
			index_end_sentences = 0
			sentences = ""

			while True:
				index_end_sentences = page_text.find("..", index_end_sentences)

				if index_end_sentences != -1:
					index_end_sentences += 1
					amount_sentences += 1
				else:
					self.sentences_for_voice_acting.append(page_text)
					break
				
				if amount_sentences == 2:
					sentences = page_text[:index_end_sentences+1]
					page_text = page_text[index_end_sentences:]

					self.sentences_for_voice_acting.append(sentences)
					amount_sentences = 0
			
			return self.sentences_for_voice_acting


		pg_num = self.page_number
		lpg_num = self.last_page_number + 1

		print(pg_num)
		print(lpg_num)

		for current_page_number in range(pg_num, 21):
			current_page = self.reader.pages[current_page_number]

			page_text = current_page.extract_text()
			page_text = page_text.lower()

			page_text = remove_extra_symbols(page_text)
			page_text = fixing_words_accent(page_text)
			page_text = replacing_numbers_with_text(page_text)
			page_text = fixing_punctuation(page_text)

			sentences_for_voice_acting = splitting_into_sentences(page_text)

		return sentences_for_voice_acting


book = OpenPdf("books/Кибердзюцу.pdf", 19)

sentences_for_voice_acting = book.text_correction()


count = 0
for sentence in sentences_for_voice_acting[count:]:
	print(count)
	print(sentence)
	speak(sentence)
	count += 2



