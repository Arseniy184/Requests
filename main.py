import requests # Модуль для обработки URL
from bs4 import BeautifulSoup # Модуль для работы с HTML
import time # Модуль для остановки программы
import smtplib # Модуль для работы с почтой

# Основной класс
class Currency:
	# Ссылка на нужную страницу
	DOLLAR_RUB = 'https://www.investing.com/'
	# Заголовки для передачи вместе с URL
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
	current_converted_price = 0
	difference = 0.3 # Разница после которой будет отправлено сообщение на почту

	def __init__(self):
		# Установка курса валюты при создании объекта
		self.current_converted_price = float(self.get_currency_price().replace(",", "."))

	# Метод для получения курса валюты
	def get_currency_price(self):
		# Парсим всю страницу
		full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)
		# Разбираем через BeautifulSoup
		soup = BeautifulSoup(full_page.content, 'html.parser')
		convert = soup.findAll("td", {"class": "lastNum", "class": "pid-8827-last"})
		return convert[0].text

	# Проверка изменения валюты
	def check_currency(self):
		currency = float(self.get_currency_price().replace(",", "."))
		if currency >= self.current_converted_price + self.difference:
			print("Курс сильно вырос, может пора что-то делать?")
			self.send_mail()
		elif currency <= self.current_converted_price - self.difference:
			print("Курс сильно упал, может пора что-то делать?")
			self.send_mail()

		print("Dollar Index = " + str(currency))
		time.sleep(3) # Засыпание программы на 3 секунды
		self.check_currency()

# Отправка почты через SMTP
	def send_mail(self):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login('ВАША ПОЧТА', 'ПАРОЛЬ')

		subject = 'Currency mail'
		body = 'Currency has been changed!'
		message = f'Subject: {subject}\n{body}'

		server.sendmail(
			'От кого',
			'Кому',
			message
		)
		server.quit()

# Создание объекта и вызов метода
currency = Currency()
currency.check_currency()
input()
# time.sleep(10)
# input('Press ENTER to exit')


