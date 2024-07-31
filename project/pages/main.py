from typing import Any

import customtkinter as ctk


class MainPage(ctk.CTkFrame):
    def __init__(self, parent: Any, controller: Any, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.controller = controller

        lbl = ctk.CTkLabel(
            self,
            text="This is a Main Page"
        )
        lbl.grid(
            row=0, column=0, padx=20
        )
