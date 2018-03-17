# Парсер рассказов из https://ideer.ru/
# Made by makromant
# Working version at at 17 march 2018
import re
import requests
import time
import sys

URL = "https://ideer.ru/"
headers = {
	"User-Agent":
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.55"
}
TAGS = []
story = []
SITE_TAGS = re.findall("<li class=\"(.*?)> <a href=\"/secrets/(.*?)</a>",
					   requests.get(URL, headers=headers).text)
new_site_tags = []
for el in SITE_TAGS:
	new_site_tags.append(el[1].split(">")[1].strip())
SITE_TAGS = new_site_tags


def timer():
	time.sleep(300)


def find_story():
	"""Находит истории и записывает их в список"""
	story = re.findall("<div class=\"shortContent\">(.*?)</div>",
					   requests.get(URL, headers=headers).text)
	return story


def find_tag():
	"""Находит тег у последней истории"""
	tag = re.findall("</h2> <a class=\"fl-r tag\" href=\"/secrets/(.*?)/\"> (.*?) </a>",
					 requests.get(URL, headers=headers).text)
	return tag[0][1]


def check_tags(tag):
	"""Проверяет наличие тега на сайте(в популярных)"""
	if (tag in SITE_TAGS):
		return True
	else:
		return False


def add_tags():
	"""ДОбавление тега для фильтрации историй"""
	inner = ""
	while (1):
		inner = input(
			"\nВведите тег или \"q\" для завершения ввода или \"список\" (без добавления тегов будут выводиться все истории): ")
		inner = inner.lower().capitalize()
		# Проверка на существование тега
		if (inner == "Q"):
			break
		elif (inner.lower() == "список"):
			print("Доступные теги: ", SITE_TAGS)
			continue

		if (check_tags(inner)):
			TAGS.append(inner)
			print("\nДобавлен тег {0}.\n Ваш список: {1}".format(inner, TAGS))
		else:
			print("\nТакого тега не существует. Повторите ввод.")


def main():
	"""Сравнивает истории чтобы не печатать одно и то же. Печатает 1 историю в час если она появляется новая"""
	story.append(find_story()[0])
	tag = find_tag()
	if TAGS != []:
		if tag not in TAGS:
			return
	if len(story) > 1 and story[len(story) - 1] == story[len(story) - 2]:
		del story[len(story) - 1]
	else:
		print("\n" + "\t" * 4, tag)
		print(story[len(story) - 1])
	if len(story) > 2:
		del story[0]

# Starts
add_tags()

while 1:
	main()
