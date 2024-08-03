from correct_accent_words import *
from numbers_into_words import *

class TextCorrection:
	""" A class for correcting the final text for voicing"""
	def improve_text(page_text: str) -> str:
		def __remove_extra_symbols(page_text: str) -> str:
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
			
			page_text = page_text.replace("\xa0", " ")
			page_text = page_text.replace("\n", " ")

			page_text = page_text.replace("  ", " ")

			return page_text

		def __fixing_words_accent(page_text: str) -> str:
			"""
			The placement of accents in words from the dictionary "correct_words_dict"

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Text with correct accents
			"""
			for uncorrect, correct in correct_accent_words_dict.items():
				page_text = page_text.replace(f" {uncorrect} ", f" {correct} ")
				page_text = page_text.replace(f" {uncorrect}, ", f" {correct} ")
				page_text = page_text.replace(f" {uncorrect}: ", f" {correct} ")

			page_text = page_text.replace("  ", " ")

			return page_text

		def __replacing_numbers_with_text(page_text: str) -> str:
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

		def __fixing_punctuation(page_text: str) -> str:
			"""
			A method for correcting punctuation marks

			Args:
				page_text (str): Text from page
			
			Returns:
				str: Text with corrected punctuation marks
			"""
			page_text = page_text.replace(" - ", "")
			page_text = page_text.replace("- ", "")
			page_text = page_text.replace(" -", "")

			page_text = page_text.replace("(", ",")
			page_text = page_text.replace(")", ",")

			page_text = page_text.replace(" , ", ", ")
			page_text = page_text.replace(" ,", ", ")

			page_text = page_text.replace("—", ",")

			page_text = page_text.replace(" , ", ", ")
			page_text = page_text.replace(" ,", ", ")

			page_text = page_text.replace(".", "..")
			page_text = page_text.replace(" ..", "..")
			page_text = page_text.replace(",..", "..")

			return page_text

		page_text = __remove_extra_symbols(page_text)
		page_text = __fixing_words_accent(page_text)
		page_text = __replacing_numbers_with_text(page_text)
		page_text = __fixing_punctuation(page_text)

		return page_text
