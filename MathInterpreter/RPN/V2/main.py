import reqkLexer

if __name__ == '__main__':

	running = True
	fn = '<stdin>'
	newline_count = 0
	data = []
	print("Welcome!") #print("Type ':h' for a list of commands!")
	print("Type ':c' for a list of commands!")
	while running:
		text = input(">> ") 

		if len(text) == 0 or text.count(' ') == len(text):
			continue
	
		elif text[0:2] == ':c':
			reqkLexer.commands()
			continue

		elif text[0:2] == ':h':
			reqkLexer.help()
			continue

		elif text[0:2] == ':f':  # file open
			text, fail = reqkLexer.file_opener(text)
			if fail == 1:
				print(text)
				continue
			
			#print('>> '+text)

		elif text in ['q', ':q']:
			break

		curr_text = ''
		data.clear()
		newline_count = 0
		for idx, char in enumerate(text):
			curr_text += char
			if char == '\n' or idx == len(text)-1:
				newline_count += 1
				data.append(curr_text)
				curr_text = ''

		if newline_count:
			for idx, section in enumerate(data):
				print(reqkLexer.main(fn, section.strip()))
		else:
			print(reqkLexer.main(fn, text))