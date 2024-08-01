from TextCorrection import TextCorrection

class OpenBook():
	""" Class OpenPdf """
	def __init__(self, path_to_book: str, home_page_number: int = 0) -> None:
		"""
		Standard definition

		Args:
			path_to_book (str): Path to book
			page_number (int): The page from which the text will start to be voiced
		
		Returns:
			None
		"""
		self.path_to_book = path_to_book
		self.home_page_number = home_page_number

		self.books_formats = [
			".pdf", ".fb2", ".mobi",
			".kf8", ".azw", ".lrf",
			".txt", ".doc", ".docs",
			".rtf", ".pdf", ".djvu",
		]

		self.book_format = ""

		for book_format in self.books_formats:
			if self.path_to_book.find(book_format) != -1:
				self.book_format = book_format
				break

	def __make_sentence(self, page_text: str) -> None:
		sentence = ""
		count_sentence = 0
		index_end_sentence = 0
		
		while True:
			index_end_sentence = page_text.find("..", index_end_sentence)
			if index_end_sentence != -1: # or page_text.find("?", index_end_sentence) != 1:
				sentence = page_text[:index_end_sentence+3]
				page_text = page_text[index_end_sentence+3:]
				count_sentence += 1
			else:
				sentence = page_text[:index_end_sentence]
				self.sentences_voice_acting.append(sentence)
				break
			
			if count_sentence:
				self.sentences_voice_acting.append(sentence)
				count_sentence = 0

	def open_book(self) -> None:
		if self.book_format == ".pdf":
			from pypdf import PdfReader

			self.pdf_reader = PdfReader(self.path_to_book)
			self.number_pages = len(self.pdf_reader.pages)
			self.last_page_number = self.number_pages - self.home_page_number
	
	def get_sentences(self) -> list:
		self.sentences_voice_acting = []

		if self.book_format == ".pdf":
			for page_number in range(self.home_page_number, self.last_page_number):
				print(f"Page number is: {page_number}")
				page = self.pdf_reader.pages[page_number]

				page_text = page.extract_text().lower()
				page_text = TextCorrection.improve_text(page_text)

				self.__make_sentence(page_text)

			return self.sentences_voice_acting


