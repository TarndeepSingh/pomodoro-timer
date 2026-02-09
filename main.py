import math
import tkinter as tk
from tkinter import messagebox


class PomodoroApp:
    # ---------------------------- CONSTANTS ------------------------------- #
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"

    WORK_MIN = 25
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 20

    def __init__(self, window: tk.Tk):
        self.window = window
        self.reps = 0
        self.timer_id = None
        self.is_running = False

        self._setup_ui()

    # ---------------------------- UI SETUP ------------------------------- #
    def _setup_ui(self):
        self.window.title("Pomodoro Timer")
        self.window.config(padx=100, pady=50, bg=self.YELLOW)

        self.title_label = tk.Label(
            text="Timer",
            fg=self.GREEN,
            bg=self.YELLOW,
            font=(self.FONT_NAME, 50)
        )
        self.title_label.grid(column=1, row=0)

        self.canvas = tk.Canvas(
            width=200,
            height=224,
            bg=self.YELLOW,
            highlightthickness=0
        )

        try:
            self.tomato_img = tk.PhotoImage(file="tomato.png")
            self.canvas.create_image(100, 112, image=self.tomato_img)
        except tk.TclError:
            messagebox.showwarning(
                "Image Missing",
                "tomato.png not found. Running without image."
            )

        self.timer_text = self.canvas.create_text(
            100,
            130,
            text="00:00",
            fill="white",
            font=(self.FONT_NAME, 35, "bold")
        )
        self.canvas.grid(column=1, row=1)

        self.start_button = tk.Button(
            text="Start",
            highlightthickness=0,
            command=self.start_timer
        )
        self.start_button.grid(column=0, row=2)

        self.reset_button = tk.Button(
            text="Reset",
            highlightthickness=0,
            command=self.reset_timer
        )
        self.reset_button.grid(column=2, row=2)

        self.check_marks = tk.Label(
            fg=self.GREEN,
            bg=self.YELLOW,
            font=(self.FONT_NAME, 20)
        )
        self.check_marks.grid(column=1, row=3)

    # ---------------------------- TIMER CONTROLS ------------------------------- #
    def start_timer(self):
        if self.is_running:
            return  # prevent multiple timers

        self.is_running = True
        self.reps += 1

        work_sec = self.WORK_MIN * 60
        short_break_sec = self.SHORT_BREAK_MIN * 60
        long_break_sec = self.LONG_BREAK_MIN * 60

        if self.reps % 8 == 0:
            self._set_title("Long Break", self.RED)
            self._count_down(long_break_sec)
        elif self.reps % 2 == 0:
            self._set_title("Break", self.PINK)
            self._count_down(short_break_sec)
        else:
            self._set_title("Work", self.GREEN)
            self._count_down(work_sec)

    def reset_timer(self):
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

        self.reps = 0
        self.is_running = False
        self._set_title("Timer", self.GREEN)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.check_marks.config(text="")

    # ---------------------------- COUNTDOWN ------------------------------- #
    def _count_down(self, count: int):
        minutes = count // 60
        seconds = count % 60

        self.canvas.itemconfig(
            self.timer_text,
            text=f"{minutes:02d}:{seconds:02d}"
        )

        if count > 0:
            self.timer_id = self.window.after(
                1000, self._count_down, count - 1
            )
        else:
            self.is_running = False
            self._update_checkmarks()
            self.start_timer()

    # ---------------------------- HELPERS ------------------------------- #
    def _set_title(self, text: str, color: str):
        self.title_label.config(text=text, fg=color)

    def _update_checkmarks(self):
        work_sessions = self.reps // 2
        self.check_marks.config(text="✔" * work_sessions)


# ---------------------------- MAIN ------------------------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
