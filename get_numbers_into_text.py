import requests

print("numbers_into_words_dict = {")

i = 3001
while i > 0:
	r = requests.get(f"https://num-words.com/ru/propysyu/0-9999/0-49/{i}/")
	text_from_site = r.text

	index1 = text_from_site.find("<h2>Число или сумма текстом:</h2></div><div><div><textarea readonly>")
	text_from_site = text_from_site[index1:]
	text_from_site = text_from_site[68:]

	index2 = text_from_site.find(",")
	number = text_from_site[:index2-6]

	print(f'    "{i}": "{number}",')
	i -= 1

print("}")


