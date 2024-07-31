import threading
from abc import ABC, abstractmethod
from typing import Callable

from sentence_transformers import SentenceTransformer


class BaseWorker(threading.Thread, ABC):
    def __init__(self, **kwargs):
        """
        Initializes the BaseListener thread.

        Args:
            callback (Callable, optional): The function to call with the recorded audio. Defaults to None.
            kwargs: Additional keyword arguments to pass to the threading.Thread initializer.
        """
        super().__init__(daemon=True, **kwargs)
        self._stop_event = threading.Event()

    @abstractmethod
    def run(self):
        """
        The entry point for the thread. This method should be overridden by subclasses.
        """
        pass

    def stop(self):
        """
        Stops the thread by setting the stop event and joining the thread.
        """
        self._stop_event.set()  # Signal the thread to stop
        self.join()  # Wait for the thread to finish

    def stopped(self) -> bool:
        """
        Checks if the stop event has been set.

        Returns:
            bool: True if the stop event is set, False otherwise.
        """
        return self._stop_event.is_set()  # Return the status of the stop event

    def is_running(self):
        return self.is_alive()


class LoadModelAndCorpusWorker(BaseWorker):
    def __init__(self, model_name: str, corpus: str, callback: Callable, **kwargs):
        super().__init__(**kwargs)
        self.corpus = corpus
        self.callback = callback
        self.model_name = model_name

    def run(self):
        print("Loading model!")
        model = SentenceTransformer(
            f'./transformers-cache/{self.model_name}',
            cache_folder='./transformers-cache'
        )
        print("Loading Corpus!")
        corpus_list = self.corpus.lower().split(",")
        corpus_embeddings = model.encode(corpus_list, convert_to_tensor=True)
        self.callback(model, corpus_embeddings, corpus_list)
