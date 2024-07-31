from tkinter import END
from typing import Any

import customtkinter as ctk


class CTkIntEntry(ctk.CTkEntry):
    def __init__(self, master: Any, min_value: int = None, max_value: int = None, **kwargs):
        ctk.CTkEntry.__init__(
            self,
            master,
            corner_radius=5,
            border_width=1,
            border_color="#fefefe",
            **kwargs
        )

        self.min_value = min_value
        self.max_value = max_value

        reg = master.register(self.validate)
        self.configure(
            validate="key",
            validatecommand=(reg, '%P'),
        )

    def validate(self, value) -> bool:
        try:
            if value == '':
                self.insert(END, '0')
                return True
            value = int(value)
            if self.min_value and value < self.min_value:
                return False
            if self.max_value and value > self.max_value:
                return False
            self.configure(border_color="gray")
            return True
        except ValueError:
            self.configure(border_color="red")
            self.insert(END, '0')
            return False
