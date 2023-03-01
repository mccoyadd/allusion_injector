import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Allusions")

big_frame = tk.Frame(root)
big_frame.pack()

w = 80

### text input 

text_frame = tk.Frame(big_frame,pady=10)
text_frame.pack()

text = tk.Text(text_frame,height=15,width=75,font=("Arial", 15))
text.focus_set()
text.pack()

### arrow up frame

arrow_frame = tk.Frame(big_frame)
arrow_frame.pack()
arrow_up = tk.Label(arrow_frame,text="⬆")
arrow_up.pack()

### loaded option

bw = 3

loaded_frame = tk.Frame(big_frame)
loaded_frame.pack(padx=5)

loadup=tk.Label(loaded_frame, text="^`",width=bw)
loadup.pack(side=tk.LEFT)
loadup.pack()

loaded  = tk.Label(loaded_frame,height=4,width=w,text="",
	wraplength=550,justify="left",relief=tk.RAISED)
loaded.pack()


### arrow up frame

arrow_frame2 = tk.Frame(big_frame)
arrow_frame2.pack()
arrow_up2 = tk.Label(arrow_frame2,text="⬆")
arrow_up2.pack()

### options

option_frame = tk.Frame(big_frame)
option_frame.pack(padx=5)

#### 1

option_height = 4
wl = 550 # wraplength

option_frame1 = tk.Frame(option_frame)
option_frame1.pack()
button1=tk.Label(option_frame1, text="^1",width=bw)
button1.pack(side=tk.LEFT)
opt1 = tk.Label(option_frame1,height=option_height,width=w,
	wraplength=wl,relief=tk.RIDGE)
opt1.pack()

#### 2

option_frame2 = tk.Frame(option_frame)
option_frame2.pack()
button2=tk.Label(option_frame2, text="^2",width=bw)
button2.pack(side=tk.LEFT)
opt2 = tk.Label(option_frame2,height=option_height,width=w,
	wraplength=wl,relief=tk.RIDGE)
opt2.pack()

#### 3

option_frame3 = tk.Frame(option_frame,)
option_frame3.pack()
button3=tk.Label(option_frame3, text="^3",width=bw)
button3.pack(side=tk.LEFT)
opt3 = tk.Label(option_frame3,height=option_height,width=w,
	wraplength=wl,relief=tk.RIDGE)
opt3.pack()

#### 4

option_frame4 = tk.Frame(option_frame)
option_frame4.pack()
button4=tk.Label(option_frame4, text="^4",width=bw)
button4.pack(side=tk.LEFT)
opt4 = tk.Label(option_frame4,height=option_height,width=w,
	wraplength=wl,relief=tk.RIDGE)
opt4.pack()

#### 5

option_frame5 = tk.Frame(option_frame)
option_frame5.pack()
button5=tk.Label(option_frame5, text="^5",width=bw)
button5.pack(side=tk.LEFT)
opt5 = tk.Label(option_frame5,height=option_height,width=w,
	wraplength=wl,relief=tk.RIDGE)
opt5.pack()

######

info_frame = tk.Frame(big_frame,width=70)
info_frame.pack(fill=tk.X)


from datetime import datetime
#import os
# timestamp = datetime.now().strftime("%m/%d/%Y_%H:%M")

import to_html

def print_out(e=None):
	timestamp = datetime.now().strftime("%m-%d-%Y_%H:%M")
	tkinter_tagged_text = text.dump("1.0", "end")
	filename = "output/output_%s.html" % timestamp
	text_converted_to_html = to_html.write_data_as_html(tkinter_tagged_text,filename), 
	# with open("output/"+text_converted_to_html,'w') as f:
	# 	f.write(text_converted_to_html,"output")
	messagebox.showinfo("Message","saved to %s" % filename)

print_button = tk.Button(info_frame, text="💾",command=print_out,padx=5,pady=5)
print_button.pack(side=tk.LEFT,padx=5,pady=5)

# spacer = tk.Label(info_frame)
# spacer.pack(side=tk.LEFT)

target_name = tk.Label(info_frame, fg='green', text="•")
target_name.place(x=377,y=12)#tk.RIGHT)

article_name = tk.Label(info_frame, fg='red', text="•")
article_name.pack(side=tk.RIGHT,padx=5,pady=5)#tk.RIGHT)


######

import allusion_engine

#### BINDING

num2option = {
	1:opt1,
	2:opt2,
	3:opt3,
	4:opt4,
	5:opt5,
}

num2allusion = {
	1:None,
	2:None,
	3:None,
	4:None,
	5:None,
}

loaded_allusion = None

loaded_empty_text = "~"

cool_off = 10 ## don't always offer allusions

used_cores = [] ## keep track so don't get offered again

def get_allusions(e):
	global cool_off
	print(cool_off)
	if cool_off==0:
		current_text = text.get("1.0",'end-1c')
		allusions = allusion_engine.get_allusions_for_text(current_text,used_cores=used_cores) 
		if allusions!=[]:
			cool_off = 10 ## reset
			target_name.config(text=allusions[0]['target'])
			#article_name.config(text=loaded_allusion[1])
		else:
			target_name.config(text="•")
		for i in range(5):
			if len(allusions)>=i+1:
				num2allusion[i+1] = allusions[i]
				num2option[i+1].config(text=allusions[i]["ready_allusion"])
			else:
				num2allusion[i+1] = None
				num2option[i+1].config(text="")
	else:
		cool_off-=1 # get closer to adding allusions
	### show the target



def load(e):
	print("load!")
	keynum = int(e.keysym)
	#option = num2option[keynum]
	to_load = num2allusion[keynum]
	if to_load!=None:	
		global loaded_allusion
		loaded_allusion = to_load
		loaded.config(text=loaded_allusion["ready_allusion"])
		article_name.config(text=loaded_allusion["article"])



def insert(e):
	print("insert!")
	global loaded_allusion
	if loaded_allusion!=None:
		text_to_insert = loaded_allusion["ready_allusion"]
		if text_to_insert!=loaded_empty_text:
			tags = (loaded_allusion['article'],"wiki")
			cursor_position = text.index(tk.INSERT)
			#print(cursor_position)
			#text.insert(cursor_position,"\u200c"+text_to_insert+"\u200c\u200c")
			text.insert(cursor_position,text_to_insert,tags)
			text.tag_configure('wiki', foreground='#3535cc')
		global used_cores
		#print(loaded_allusion)
		used_cores.append(loaded_allusion["core_allusion"])
		loaded.config(text="")
		article_name.config(text=loaded_allusion["article"])
		loaded_allusion = None	



root.bind("<space>", get_allusions)
root.bind("<Control-Key-1>", load)
root.bind("<Control-Key-2>", load)
root.bind("<Control-Key-3>", load)
root.bind("<Control-Key-4>", load)
root.bind("<Control-Key-5>", load)
root.bind("<Control-Key-p>", print_out)
root.bind("<Control-Key-`>", insert)


root.mainloop()