import customtkinter as ctk
from typing import Dict

from project.core import Utils
from project.frames import ContainerFrame, SidebarFrame

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class Application(ctk.CTk, Utils):
    frames: Dict = {}
    model_path: str = ""
    sidebar: SidebarFrame
    container: ContainerFrame

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.wm_title("Kanbii Application")
        self.geometry("700x450")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.container = ContainerFrame(self)
        self.container.grid_columnconfigure(0, weight=1, uniform='a')
        self.container.grid_rowconfigure(0, weight=1, uniform='a')
        self.container.grid(row=0, column=1, sticky="nsew")

        self.sidebar = SidebarFrame(self)
        self.sidebar.grid_rowconfigure(0, weight=1, uniform='a')
        self.sidebar.grid_rowconfigure(1, weight=2, uniform='a')
        self.sidebar.grid_rowconfigure(2, weight=1, uniform='a')
        self.sidebar.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
