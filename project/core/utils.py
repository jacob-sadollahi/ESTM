import os
from glob import glob
from typing import List, Any
import customtkinter as ctk
from PIL import Image


class Utils:
    static_folder: str = './static-files'
    model_folder: str = "./transformers-cache"

    def get_models_dirs(self) -> List:
        return list(sorted([
            model for model in glob(f"{self.model_folder}/*")
            if os.path.isdir(model)
        ], key=lambda x: os.path.getmtime(x)))

    def get_models_names(self) -> List:
        return list(map(
            lambda s: s.replace(f"{self.model_folder}/", ""), self.get_models_dirs()
        ))

    def get_logo(self, parent: Any) -> ctk.CTkLabel:
        logo = ctk.CTkImage(
            light_image=Image.open(f"{self.static_folder}/images/logo-light.png"),
            dark_image=Image.open(f"{self.static_folder}/images/logo-dark.png"),
            size=(169, 48),
        )
        return ctk.CTkLabel(parent, image=logo, text="")
