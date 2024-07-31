from typing import Any

import customtkinter as ctk

from project.core import Utils


class SidebarFrame(ctk.CTkFrame, Utils):
    def __init__(self, parent: Any, **kwargs):
        ctk.CTkFrame.__init__(self, parent, corner_radius=0, **kwargs)

        self.header = ctk.CTkFrame(self, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="nsew")

        self.body = ctk.CTkFrame(self, corner_radius=0)
        self.body.grid(row=1, column=0, sticky="nsew")

        self.footer = ctk.CTkFrame(self, corner_radius=0)
        self.footer.grid(row=2, column=0, sticky="nsew")

        self.logo = self.get_logo(self.header)
        self.logo.grid(row=0, column=0, padx=10, pady=20)

        ctk.CTkLabel(
            self.body, text="Training Center!"
        ).grid(
            row=0, column=0,
        )

        self.home_btn = ctk.CTkButton(
            self.footer, text="Home", command=parent.container.go_to_main_page,
        )
        self.home_btn.grid(
            row=1, column=0, padx=10, pady=(8, 0), sticky="sew",
        )

        self.train_new_model_btn = ctk.CTkButton(
            self.footer, text="Train new model", command=self.open_input_dialog_event
        )
        self.train_new_model_btn.grid(
            row=2, column=0, padx=10, pady=5, sticky="sew",
        )

        self.evaluation_model_btn = ctk.CTkButton(
            self.footer, text="Evaluation Model", command=parent.container.go_to_evaluation_page
        )
        self.evaluation_model_btn.grid(
            row=3, column=0, sticky="sew", padx=10, pady=(0, 10)
        )

    def train_new_model(self):
        print("ok")

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())
