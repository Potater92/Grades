
from tkinter import *
from logic import *

class GUI:
    def __init__(self, master: Tk) -> None:
        """
        Initialize the GUI.

        Args:
            master: The Tkinter master widget.
        """
        self.master = master
        master.title("Student Grades")

        self.name_entry = Entry(master, width=20)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)
        Label(master, text="Student name:").grid(row=0, column=0, sticky='w')

        self.attempts_entry = Entry(master, width=5)
        self.attempts_entry.grid(row=1, column=1, pady=5, padx=5)
        Label(master, text="No of attempts:").grid(row=1, column=0, sticky='w')
        self.attempts_entry.bind("<KeyRelease>", self.validate_attempts)

        self.submit_button = Button(master, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=100, column=0, columnspan=2, pady=5)

        self.status_label = Label(master, text="")
        self.status_label.grid(row=101, column=0, columnspan=2)

        self.score_entries = []
        self.score_labels = []

    def validate_attempts(self, event=None) -> None:
        """
        Validate the number of attempts entered.

        Args:
            event: The Tkinter event (default None).
        """
        try:
            attempts = int(self.attempts_entry.get())
            if attempts > 4:
                self.status_label.config(text="Only up to 4 attempts are allowed.", fg='red')
                return
            elif attempts <= 0:
                self.status_label.config(text="Number of attempts must be a positive integer.", fg='red')
                return
            else:
                self.status_label.config(text="")
            self.update_score_fields(attempts)
        except ValueError:
            self.status_label.config(text="Number of attempts must be a valid integer.", fg='red')

    def update_score_fields(self, attempts: int) -> None:
        """
        Update score entry fields based on the number of attempts.

        Args:
            attempts: The number of attempts.
        """
        for entry in self.score_entries:
            entry.grid_forget()
        for label in self.score_labels:
            label.grid_forget()
        self.score_entries = []
        self.score_labels = []

        for i in range(attempts):
            entry = Entry(self.master, width=10)
            entry.grid(row=2 + i, column=1, pady=2, padx=5)
            label = Label(self.master, text=f"Score {i+1}:")
            label.grid(row=2 + i, column=0, sticky='w')
            self.score_entries.append(entry)
            self.score_labels.append(label)

    def on_submit(self) -> None:
        """
        Process the submitted scores.
        """
        name = self.name_entry.get().strip()
        if not name:
            self.status_label.config(text="Student name cannot be empty.", fg='red')
            return

        scores = [entry.get().strip() or "0" for entry in self.score_entries]  # Assume 0 for empty fields

        if not all(score.isdigit() for score in scores):
            self.status_label.config(text="All scores must be numeric.", fg='red')
            return

        if any(int(score) < 0 or int(score) > 100 for score in scores):
            self.status_label.config(text="Scores must be between 0 and 100.", fg='red')
            return

        message, success = process_scores(name, len(scores), scores)
        self.status_label.config(text=message, fg='green' if success else 'red')
        if success:
            self.clear_entries()

    def clear_entries(self) -> None:
        """
        Clear all entry fields.
        """
        self.name_entry.delete(0, END)
        self.attempts_entry.delete(0, END)
        for entry in self.score_entries:
            entry.delete(0, END)

