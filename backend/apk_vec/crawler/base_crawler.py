from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List
import threading


class BaseCrawler(metaclass=ABCMeta):

    def __init__(self):
        self._data = None
        self._finish_callbacks = []
        self._fail_callbacks = []

    def _crawl_worker(
        self,
        on_finish_callbacks: List[Callable[[Dict], None]]=list(),
        on_fail_callbacks: List[Callable[[str], None]]=list(),
    ):
        try:
            self._data = self._crawl()
        except Exception as e:
            [callback(e) for callback in on_fail_callbacks]
            return

        [callback(self._data) for callback in on_finish_callbacks]

    def crawl(
        self,
        async_: bool=False,
        on_finish_callback: Callable[[Dict], None]=None,
        on_fail_callback: Callable[[str], None]=None,
    ):
        if on_finish_callback is not None:
            if not isinstance(on_finish_callback, list):
                on_finish_callback = [on_finish_callback]
            self._finish_callbacks += on_finish_callback

        if on_fail_callback is not None:
            if not isinstance(on_fail_callback, list):
                on_fail_callback = [on_fail_callback]
            self._fail_callbacks += on_fail_callback

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

    def add_finish_callback(
        self,
        callback: Callable[[Dict], None]
    ):
        if not isinstance(callback, list):
            callback = [callback]

        self._finish_callbacks += callback

    def add_fail_callback(
        self,
        callback: Callable[[str], None]
    ):
        if not isinstance(callback, list):
            callback = [callback]

        self._fail_callbacks += callback

    @abstractmethod
    def _crawl(self):
        raise NotImplementedError
