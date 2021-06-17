from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


def outer_function(a, b):
	def inner_function(c, d):
		return c + d
	
	return inner_function(a, b)


result = outer_function(5, 10)

try:
	data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
	original_data = pandas.read_csv("data/br-pt-to-eng-words-1-500.csv")
	to_learn = original_data.to_dict(orient="records")
else:
	to_learn = data.to_dict(orient="records")


# Add the language as the first line in the csv (Portuguese, English)
def next_card():
	global current_card, flip_timer
	window.after_cancel(flip_timer)
	current_card = random.choice(to_learn)
	canvas.itemconfig(card_title, text="Portuguese", fill="black")
	canvas.itemconfig(card_word, text=current_card["Portuguese"], fill="black")
	canvas.itemconfig(card_background, image=card_front)
	flip_timer = window.after(3000, func=flip_card)


def flip_card():
	canvas.itemconfig(card_title, text="English", fill="white")
	canvas.itemconfig(card_word, text=current_card["English"], fill="white")
	canvas.itemconfig(card_background, image=card_back)


def is_know():
	to_learn.remove(current_card)
	data = pandas.DataFrame(to_learn)
	data.to_csv("data/words_to_learn.csv", index=False)
	next_card()


window = Tk()
window.title("Flip recall Portuguese to English")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_background = canvas_image = canvas.create_image(400, 263, image=card_front)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 25, "normal"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 50, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_know)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
