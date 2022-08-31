import reqkMathLexer

if __name__ == "__main__":

	running = True
	show_tokens = False
	show_parse  = False
	dev_mode    = False
	show_stages = False
	print("Type ':h' for a list of commands!")
	while running:
		fn, expected_fe = '<stdin>', '.reqk'  # file extension
		text = input(">> ")

		if len(text) == 0 or text.count(' ') == len(text):
			continue

		elif text[0:2] == ':f':  # file open
			text, fail = reqkMathLexer.file_opener(text)
			if fail == 1:
				print(text)
				continue

			print('>> '+text)

		elif text[0:2] == ':h':
			reqkMathLexer.help()
			continue

		elif text in ['q', ':q']:
			break

		elif text in ['tk', ':tk']:
			if show_tokens == True: show_tokens = False
			elif show_tokens == False: show_tokens = True
			
			print(" - Tokens Visible - " if show_tokens == True else " - Tokens Hidden - ")
			continue

		elif text in ['pt', ':pt']:
			if show_parse == True: show_parse = False
			elif show_parse == False: show_parse = True
			
			print(" - Parsing Visible - " if show_parse == True else " - Parsing Hidden - ")
			continue

		elif text in ['d', ':d']:
			if dev_mode == True: dev_mode = False
			elif dev_mode == False: dev_mode = True
			
			print(" - Developer Mode ON - " if dev_mode == True else " - Developer Mode OFF - ")
			continue

		elif text in ['st', ':st']:
			if show_stages == True: show_stages = False
			elif show_stages == False: show_stages = True
			
			print(" - Calculations Visible - " if show_stages == True else " - Calculations Hidden - ")
			continue

		print(reqkMathLexer.main(fn, text, show_tokens, show_parse, dev_mode, show_stages))


#cd python\language_creation\reqk\success\v3.1
#python reqkMathShell.py
