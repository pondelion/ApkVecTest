from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List
import threading


class BaseCrawler(metaclass=ABCMeta):

    def __init__(self):
        self._data = None
        self._single_finish_callbacks = []
        self._complete_callbacks = []
        self._fail_callbacks = []

    def _crawl_worker(
        self,
        on_single_finish_callbacks: List[Callable[[Dict], None]]=list(),
        on_complete_callbacks: List[Callable[[Dict], None]]=list(),
        on_fail_callbacks: List[Callable[[str], None]]=list(),
    ):
        try:
            for filepath in self._crawl():
                [callback(filepath) for callback in on_single_finish_callbacks]
        except Exception as e:
            [callback(e) for callback in on_fail_callbacks]
            return

        [callback(self._data) for callback in on_complete_callbacks]

    def crawl(
        self,
        async_: bool=False,
        on_single_finish_callback: Callable[[Dict], None]=None,
        on_complete_callback: Callable[[Dict], None]=None,
        on_fail_callback: Callable[[str], None]=None,
    ):
        self.add_single_finish_callback(on_single_finish_callback)
        self.add_complete_callback(on_complete_callback)
        self.add_fail_callback(on_fail_callback)

        if async_:
            thread = threading.Thread(
                target=self._crawl_worker,
                args=([
                    self._finish_callbacks,
                    self._fail_callbacks
                ])
            )
            thread.start()
            return thread
        else:
            self._data = self._crawl()

    def add_single_finish_callback(
        self,
        callback: Callable[[Dict], None]
    ):
        if callback is None:
            return

        if not isinstance(callback, list):
            callback = [callback]

        self._single_finish_callbacks += callback

    def add_complete_callback(
        self,
        callback: Callable[[Dict], None]
    ):
        if callback is None:
            return

        if not isinstance(callback, list):
            callback = [callback]

        self._complete_callbacks += callback

    def add_fail_callback(
        self,
        callback: Callable[[str], None]
    ):
        if callback is None:
            return

        if not isinstance(callback, list):
            callback = [callback]

        self._fail_callbacks += callback

    @abstractmethod
    def _crawl(self):
        """Subclass must yealds local filepath of saved crawled data
        """
        raise NotImplementedError
