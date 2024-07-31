import customtkinter as ctk

from project.core import Utils


class ProgressBarDialog(ctk.CTkToplevel, Utils):
    def __init__(self, master, **kwargs):
        ctk.CTkToplevel.__init__(self, master, **kwargs)
        self.geometry("400x80")
        self.wm_title("Copy Model!")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)

        self.copy_lbl = ctk.CTkLabel(self, text="Copying!")
        self.copy_lbl.grid(row=0, column=0, padx=(10, 0), sticky="we")

        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=0, column=1, padx=(0, 10), sticky="we")
        self.progressbar.start()
