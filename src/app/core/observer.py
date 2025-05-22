from abc import abstractmethod, ABC
from typing import List


class Observer(ABC):
    @abstractmethod
    def on_notification(self, message: str) -> None:
        raise NotImplementedError(
            "Subclasses must implement the on_notification method"
        )


class Observable(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def add_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify_observers(self, message: str) -> None:
        for observer in self._observers:
            observer.on_notification(message)
