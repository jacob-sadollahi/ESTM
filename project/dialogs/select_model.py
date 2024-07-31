import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

from ..core import Utils


class SelectModelDialog(ctk.CTkToplevel, Utils):
    current_model_name: str

    def __init__(self, parent):
        ctk.CTkToplevel.__init__(self, parent)
        self.geometry("300x150")
        self.wm_title("Select Model!")
        self.grid_rowconfigure(
            0, weight=1
        )
        self.grid_columnconfigure(
            1, weight=1
        )

        self.lbl = ctk.CTkLabel(
            self, text='Select Your model to evaluate!'
        )
        self.lbl.pack(
            fill=ctk.X, padx=10, pady=(10, 0)
        )

        variables = tk.StringVar()
        self.select_model_cb = ttk.Combobox(
            self, textvariable=variables
        )
        self.select_model_cb['state'] = 'readonly'
        self.select_model_cb['values'] = self.get_models_names()
        self.select_model_cb.pack(
            fill=ctk.X, padx=10, pady=10
        )
        self.select_model_cb.current(0)

        self.select_model_btn = ctk.CTkButton(
            self,
            text="Select as a current model",
            command=self.set_current_model_name,
        )
        self.select_model_btn.pack(
            fill=ctk.X, padx=10, pady=(0, 10)
        )

    def set_current_model_name(self):
        self.current_model_name = self.select_model_cb.get()
        self.destroy()

    def get_current_model_name(self):
        return self.current_model_name
