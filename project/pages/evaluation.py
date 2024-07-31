import pathlib
import shutil

import customtkinter as ctk
from tkinter import messagebox, ttk, CENTER, TclError
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Any
import csv

import torch

from project.core import Utils
from project.core.workers import LoadModelAndCorpusWorker
from project.widgets import CTkIntEntry

KANBII_SKILLS = """PHP,Bartending,Drink Preparation,Knowledge of Alcoholic Beverages,Bar Equipment Operation"""
KANBII_SKILLS = ",".join(KANBII_SKILLS.split(",")[:200])


class EvaluationPage(ctk.CTkFrame, Utils):
    def __init__(self, parent: Any, controller: Any, **kwargs):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent", **kwargs)
        self.container = parent
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.grid_rowconfigure(0, weight=1)
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=1)
        self.footer.grid_columnconfigure(2, weight=1)
        self.footer.grid(row=3, column=0, sticky='nsew')

        ctk.CTkLabel(
            self, text="Evaluation results"
        ).grid(
            row=0, padx=10, pady=10
        )

        self.models = self.get_models_names()
        self.select_model_cb = ctk.CTkComboBox(
            self, values=self.models, border_width=0, button_color="#f1f1f1", state='readonly'
        )
        self.select_model_cb.grid(
            row=1, column=0, padx=10, sticky="we"
        )
        if self.models:
            self.select_model_cb.set(self.models[0])

        self.eval_data_txt = ctk.CTkTextbox(self)
        self.eval_data_txt.grid(row=2, padx=10, sticky='nsew')
        self.eval_data_txt.insert(0.0, KANBII_SKILLS)

        self.upload_model_btn = ctk.CTkButton(
            self.footer, text="Upload Your Model", command=self.upload_model
        )
        self.upload_model_btn.grid(
            row=0, column=0, sticky="e"
        )

        self.select_model_to_evaluate_btn = ctk.CTkButton(
            self.footer, text="Evaluation", command=self.evaluation
        )
        self.select_model_to_evaluate_btn.grid(
            row=0, column=1, sticky="w", padx=8
        )

    def evaluation(self):
        model_name = self.select_model_cb.get()
        if not model_name:
            self.select_model_cb.configure(border_color="red", border_width=1, button_color="red")
        corpus = str(self.eval_data_txt.get(0.0, 'end'))

        def callback(model_, embedding_, corpus_list):
            self.select_model_to_evaluate_btn.configure(
                text="Evaluation", state="enable",
            )
            EvaluationTestPage(
                self.container, corpus_list, model_, embedding_
            ).grid(
                row=0, column=0, sticky="nsew"
            )

        worker = LoadModelAndCorpusWorker(model_name, corpus, callback)
        worker.start()
        self.select_model_to_evaluate_btn.configure(
            text="Loading Evaluation", state="disabled",
        )

    def upload_model(self) -> None:
        print("Open a dialog to select your model")
        model_path = askopenfilename(
            defaultextension=".zip",
        )
        if model_path:
            self.copy_model(model_path)

    def copy_model(self, model_path) -> None:
        file_obj = pathlib.Path(model_path)
        file_ext = file_obj.suffix
        model_name = file_obj.name[:-(len(file_ext) + 1)]
        print("Your file Ext:", file_ext)
        if file_ext not in ['.zip']:
            print("File type not supported!")
            messagebox.showerror('File Type', 'Error: File type not supported please select a file with .zip!')
            return None

        shutil.unpack_archive(model_path, f"{self.model_folder}/{model_name}", "zip")
        print("Archive file unpacked successfully.")

        self.container.go_to_evaluation_page(refresh=True)


class EvaluationTestPage(ctk.CTkFrame):
    def __init__(self, parent: Any, corpus, model: Any, corpus_embeddings, **kwargs):
        ctk.CTkFrame.__init__(self, parent, fg_color="transparent", **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=8)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.model = model
        self.corpus = corpus
        self.corpus_embeddings = corpus_embeddings

        ctk.CTkLabel(self, text="Evaluation your model!").grid(
            row=0, column=0, sticky="nsew",
        )

        self.query_var = ctk.StringVar()
        self.query_var.set("Bartending")
        self.limit_result_var = ctk.IntVar(
            value=(100 if len(self.corpus) > 100 else len(self.corpus))
        )

        self.form_data_frm = ctk.CTkFrame(self, fg_color="transparent")
        self.form_data_frm.grid_rowconfigure(0, weight=1)
        self.form_data_frm.grid_columnconfigure(0, weight=9)
        self.form_data_frm.grid_columnconfigure(1, weight=1)
        self.form_data_frm.grid_columnconfigure(2, weight=1)
        self.form_data_frm.grid(row=1, column=0, sticky="nsew")

        ctk.CTkEntry(
            self.form_data_frm, textvariable=self.query_var,
        ).grid(row=0, column=0, padx=10, sticky="ew")

        CTkIntEntry(
            self.form_data_frm,
            min_value=0,
            max_value=len(corpus),
            width=30,
            textvariable=self.limit_result_var
        ).grid(row=0, column=1, padx=(0, 10), sticky="ew")

        ctk.CTkButton(
            self.form_data_frm, text="Evaluation", command=self.show_evaluation_result
        ).grid(row=0, column=2, sticky="w")

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure(
            "Treeview",
            background="#d3d3d3",
            rowheight=25,
        )
        self.result_tbl = ttk.Treeview(
            self, columns=('index', 'sentence', 'score'), show="headings",
        )
        self.result_tbl.heading('index', text='Index')
        self.result_tbl.column("index", anchor=CENTER, width=50)
        self.result_tbl.heading('score', text='Score')
        self.result_tbl.column("score", anchor=CENTER)
        self.result_tbl.heading('sentence', text='Sentence')
        self.result_tbl.column("sentence", anchor=CENTER)
        self.result_tbl.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.show_evaluation_result()

        self.download_results_btn = ctk.CTkButton(self, text="Download results", command=self.download_results)
        self.download_results_btn.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")

    def show_evaluation_result(self):
        try:
            self.limit_result_var.get()
        except TclError as e:
            print(e)
            self.limit_result_var.set(
                100 if len(self.corpus) > 100 else len(self.corpus)
            )
        self.result_tbl.delete(*self.result_tbl.get_children())
        query_embedding = self.model.encode(str(self.query_var.get()).lower(), convert_to_tensor=True)
        similarity_scores = self.model.similarity(query_embedding, self.corpus_embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=self.limit_result_var.get())
        print(f"Top {self.limit_result_var.get()} most similar sentences in corpus:")
        i = 0
        for score, idx in zip(scores, indices):
            self.result_tbl.insert(
                parent='', index=i, values=(int(idx), self.corpus[idx], "{:.4f}".format(score))
            )
            i += 1

    def download_results(self):
        path = asksaveasfilename(
            title="Save Model Result"
        )
        if not path:
            print("Path not specified!")
            return
        data = [
            ['index', 'sentence', 'score']
        ]
        for item in self.result_tbl.get_children():
            data.append(self.result_tbl.item(item).get('values'))

        with open(f'{path}.csv', "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
            print("File saved!")
