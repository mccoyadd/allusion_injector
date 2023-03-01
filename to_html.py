## converts tagged tkinter output to html
## references to wikipedia articles are made into pandoc-style footnotes

def prep_string(astring):
	astring = astring.replace("\n","<br>")
	astring = astring.replace(" ","&nbsp;")
	return astring


def title_prep(astring):
	"""
	converting title string to something for the url
	"""
	return astring.replace(" ","_")

def process_tkinter(data):
	html_string = ""
	tool_tip = ""
	nc = 1  
	notes_section = '<section id="footnotes" class="footnotes footnotes-end-of-document" role="doc-endnotes"><hr /><ol/>'
	for thing in data:
		if thing[0]=="text":
			html_string+=prep_string(thing[1])
		elif (thing[0]=="tagon" and thing[1]=="wiki"):
			html_string+="<span class='allusion'>"
		elif (thing[0]=="tagoff" and thing[1]=="wiki"):
			if tool_tip!="":
				html_string+=tool_tip+"</span>"
				tool_tip="" # reset
			else:
				html_string+="**here**</span>"
		elif (thing[0]=="tagoff" and thing[1]!="wiki"): ## allusion label
			note_number = '<a href="#fn%s" class="footnote-ref" id="fnref%s" role="doc-noteref"><sup>%s</sup></a>' % (nc,nc,nc)
			note = '<li id="fn%s"><p><span class="wikiref">wikipedia.org/wiki/%s</span><a href="#fnref%s" class="footnote-back" role="doc-backlink">↩︎</a></p></li>' % (nc,title_prep(thing[1]),nc)
			nc+=1
			if "**here**" not in html_string:
				tool_tip = note_number
			else:
				html_string = html_string.replace("**here**",note_number)
			notes_section+=note
	html_string+=notes_section+"</ol></section>"
	return html_string

def dress_up_html(html_string):
	html_dressed = """
	<!DOCTYPE html>
	<html>
	<head>
	<style>
	.allusion{color:#8a8a8a;}
	.footnotes{color:#8a8a8a;font-size: 14px;}
	.footnote-ref{text-decoration:none;}
	.footnote-back{text-decoration:none;}
	.wikiref{font-family: "Courier",monospace;font-size: 12px;};
	</style>
	</head>
	<body>
	%s
	</body>
	</html> 
	""" % html_string
	return html_dressed

def write_data_as_html(data,file_name="test.html"):
	inside_html = process_tkinter(data)
	output_html = dress_up_html(inside_html)
	with open(file_name,'w') as f:
		f.write(output_html)

def main():
	tkinter_data = [["text", "this is the point of it and the point of love and lo", "1.0"], ["tagon", "wiki", "1.52"], ["tagon", "A'sha Hamdan", "1.52"], ["text", "OF A DAYLAMITE WOMAN WHO HELPED FREE HIM", "1.52"], ["tagoff", "A'sha Hamdan", "1.92"], ["tagoff", "wiki", "1.92"], ["text", " and\n", "1.92"], ["text", "that's so cool and ", "2.0"], ["tagon", "wiki", "2.19"], ["tagon", "Diadochi", "2.19"], ["text", "ALEXANDER'S BIRTH, AN ACT THAT\n", "2.19"], ["text", " SUGGESTS LOVE MAY HAVE BEEN A MOTIVE AS WELL", "3.0"], ["tagoff", "wiki", "3.45"], ["tagoff", "Diadochi", "3.45"], ["text", "\n", "3.45"], ["text", "\n", "4.0"], ["text", "so what", "5.0"], ["mark", "current", "5.7"], ["mark", "tk::anchor1", "5.7"], ["mark", "insert", "5.7"], ["text", "\n", "5.7"]]
	write_data_as_html(tkinter_data)


if __name__ == '__main__':
	main()