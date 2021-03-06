from xml.dom.minidom import parse

doc = parse('01.xml')

root = doc.documentElement

textboxs = root.getElementsByTagName('textbox')
textcontent=''
bVerticalBegin = False

outfile = open('01.txt', 'w')

for textbox in textboxs:
	textlines = textbox.getElementsByTagName('textline')
	for textline in textlines:
		texts = textline.getElementsByTagName('text')
		#判断是否是竖着的字，如果是的话，第一个是字，第二个是换行
		if len(texts)==2:
			bVerticalBegin = True
			textcontent =textcontent + texts[0].childNodes[0].data
		else:
			for text in texts:
				if text.childNodes[0].data != '\n':
					textcontent = textcontent + text.childNodes[0].data
					#print(type(text))
					#print(textcontent)
			#处理换行，如果textline里面的倒数第二个text是句号，倒数第一个是换行，那么就是一个换行
			if((texts[-1].childNodes[0].data == '\n') and (texts[-2].childNodes[0].data == '。')):
				textcontent = textcontent +'\n'
	    #print(textcontent)
	outfile.write(textcontent)
	outfile.write('\n')
	if bVerticalBegin:
		bVerticalBegin = False

	textcontent = ''

outfile.close()	

