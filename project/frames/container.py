from typing import Any, Dict

import customtkinter as ctk

from project.pages import MainPage, EvaluationPage


class ContainerFrame(ctk.CTkFrame):
    """
    Container Page
    """

    def __init__(self, parent: Any, **kwargs):
        ctk.CTkFrame.__init__(self, parent, corner_radius=0, fg_color="transparent", **kwargs)
        self.controller = parent
        self.pages: Dict = {}
        # self.go_to_main_page()
        self.go_to_evaluation_page()

    def show_page(self, page: Any, refresh: bool = False):
        if page not in self.pages.keys() or refresh:
            self.pages[page] = page(self, controller=self.controller)
            self.pages[page].grid(row=0, column=0, sticky="nsew")
        else:
            self.pages[page].tkraise()

    def go_to_main_page(self, refresh: bool = False):
        print("Go to main page!")
        self.show_page(MainPage, refresh=refresh)

    def go_to_evaluation_page(self, refresh: bool = False):
        print("Go to evaluation page!")
        self.show_page(EvaluationPage, refresh=refresh)
