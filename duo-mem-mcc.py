import pandas as pd
import numpy as np
from tkinter import *
from tkinter import messagebox as mb


class Quiz:
	def __init__(self, n):
		
		self.q_no = 0
		self.total_q = n
		self.correct=0
		self.wrong_list=[]
		
		self.display_question()

		self.opt_selected=IntVar()
		self.opts=self.radio_buttons()
		
		self.display_options()
		
		self.buttons()		

	def display_result(self):
		
		score = int(self.correct / self.total_q * 100)
		result = f"Score: {score}%"
		wrong_words = question[self.wrong_list]
		
		mb.showinfo("Result", f"{result}\nWrong words:\n{wrong_words}")


	def check_ans(self, q_no):		
		if self.opt_selected.get() == answer[q_no]+1:
			return True

	def next_btn(self):
		
		if self.check_ans(self.q_no):			
			self.correct += 1
		else:
			self.wrong_list.append(self.q_no)
		
		self.q_no += 1
		
		if self.q_no==self.total_q:
			self.display_result()
			gui.destroy()
		else:
			self.display_question()
			self.display_options()


	def buttons(self):
		
		quit_button = Button(gui, text="Quit", command=gui.destroy,
		width=5,bg="black", fg="black",font=("ariel",16," bold"))
		
		quit_button.place(x=100,y=320)


	def display_options(self):
		val=0
		
		self.opt_selected.set(0)

		for option in options[self.q_no]:
			print(self.opts, val)
			self.opts[val]['text']=option
			val+=1

		res = Label(gui, text=f"Score: {self.correct}/{self.q_no}")
		res.place(x=100, y=280)


	def display_question(self):
		
		q_no = Label(gui, text=question[self.q_no], width=60,
		font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		
		q_no.place(x=70, y=70)


	def radio_buttons(self):
		q_list = []
		y_pos = 100
		
		while len(q_list) < options.shape[1]:
			
			radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected, command=self.next_btn,
			value = len(q_list)+1,font = ("ariel",14))
			q_list.append(radio_btn)
	
			radio_btn.place(x = 80, y = y_pos)
			y_pos += 30
		
		return q_list
		

gui = Tk()
gui.geometry("300x400")
gui.title("Duo+Memrise Quiz")

url = "https://raw.githubusercontent.com/ddundo/norsk/main/data/duomem_dict.csv"
data = pd.read_csv(url, sep=";").sample(frac=1)
question = data['engelsk'].to_numpy()
correct = data['norsk'].to_numpy()

_opts = [correct, np.random.permutation(correct), np.random.permutation(correct), np.random.permutation(correct)]
options = np.squeeze(np.dstack(_opts))

options = options.swapaxes(-1, -1)
for ndx in np.ndindex(options.shape[:-1]):
	np.random.shuffle(options[ndx])

_ans2d = np.repeat(correct, 4).reshape(-1, 4)
_, answer = np.where(options == _ans2d)

quiz = Quiz(10)  # 10 questions per quiz
gui.mainloop()
