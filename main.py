import tkinter as tk


class TypingTest:
    def __init__(self):
        self.words = self.get_words()
        self.user_written_words = []
        self.crr_ind: int = -1

        self.font = ("Arial", 15, "bold")

        # SETTING UP THE UI
        self.win = tk.Tk()
        self.win.title("Typing Test")
        self.win.geometry("450x420")
        self.win.config(padx=20, pady=20)

        self.win.after_id = None
        # Bindings
        self.win.bind("<Return>", self.start_game)

        self.canvas = tk.Canvas(self.win, width=400, height=300)
        self.canvas.grid(row=1, column=0, columnspan=3)

        self.img = tk.PhotoImage(file="card.png")
        self.canvas.create_image(205, 150, image=self.img)

        self.canvas_text = self.canvas.create_text(
            200, 150,
            text="        Welcome To Typing Test\n      Press Enter To Submit Text.\nWhen ready Press Enter To Start!",
            font=self.font, fill="white"
        )

        self.text_box = tk.Entry(width=40)
        self.text_box.grid(row=4, column=1)

        self.timer = tk.Label(text="Time Left: 1:00", font=self.font)


    @staticmethod
    def get_words() -> list[str]:
        with open("words.txt") as f:
            return f.read().split('\n')[:-1]

    def run(self):
        self.win.eval('tk::PlaceWindow . center')
        self.win.resizable(False, False)
        self.win.mainloop()

    def start_game(self, _):
        self.text_box.focus()
        self.timer.grid(row=3, column=1)

        self.start_timer()  # 1 min
        self.win.bind("<Return>", self.update_label)
        self.get_new_text()

    def restart_game(self, _=None):
        self.__init__()

    def count_down(self, count):
        if count > 0:
            self.win.after_id = self.win.after(1000, self.count_down, count - 1)
        else:
            self.win.after_id = None

        if count:
            time_left = f"Time Left: {count}"

            if count < 10:
                time_left.replace(' ', ' 0')
        else:
            time_left = "Time's Up!"
            self.text_box.config(state="readonly")
            self.timer.grid_forget()

            self.win.unbind("<Return>")

            self.canvas.itemconfig(self.canvas_text, text="Calculating Score!")

            self.calculate_score()

        self.timer.config(text=time_left)

    def start_timer(self):
        if self.win.after_id is not None:
            self.win.after_cancel(self.win.after_id)

        self.count_down(60)

    def flash(self, widget, color: str, time: int):
        widget.config(background=color)

        if time:
            self.win.after(time, func=lambda: self.flash(widget, "white", time=0))

    def get_new_text(self):
        self.crr_ind += 1
        if self.crr_ind > (len(self.words) - 1):
            print("Game Ended!")
            self.win.unbind('<Return>')
        else:
            print("Game Started")
            self.canvas.itemconfig(self.canvas_text, text=self.words[self.crr_ind])

    def update_label(self, _=None):
        word_typed = self.text_box.get().strip()

        self.text_box.delete(0, tk.END)
        self.get_new_text()

        self.user_written_words.append(word_typed)

        if word_typed == self.words[self.crr_ind - 1]:
            self.flash(self.text_box, color="lime", time=200)
        else:
            self.flash(self.text_box, color="red", time=200)

    def calculate_score(self):
        num_of_characters_typed = 0
        time_taken = 1  # 1 min
        correctly_typed_chars = 0

        self.win.bind("<Return>", func=self.restart_game)

        if not self.user_written_words:  # if user didn't type anything
            self.canvas.itemconfig(self.canvas_text, text=f"WPM: 0\nAccuracy: 0%")
            return


        for ind, word in enumerate(self.user_written_words):
            original_word = self.words[ind]

            for i, char in enumerate(word):
                try:
                    if char == original_word[i]:
                        correctly_typed_chars += 1

                except IndexError:
                    pass

        for word in self.user_written_words:
            num_of_characters_typed += len(word)

        wpm = round(
            (num_of_characters_typed/5) / time_taken,
            2
        )

        accuracy = round((correctly_typed_chars / num_of_characters_typed) * 100, 2)

        if accuracy.is_integer():
            accuracy = int(accuracy)

        self.canvas.itemconfig(self.canvas_text, text=f"WPM: {wpm}\nAccuracy: {accuracy}%")


app = TypingTest()
app.run()

