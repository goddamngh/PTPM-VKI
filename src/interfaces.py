from abc import ABC, abstractmethod

class UserInteraction(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Запрашивает у пользователя строку."""
        pass

    @abstractmethod
    def show_output(self, message: str) -> None:
        """Выводит сообщение пользователю."""
        pass


class ConsoleInteraction(UserInteraction):
    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def show_output(self, message: str) -> None:
        print(message)

class ExternalDependency(ABC):
    @abstractmethod
    def send_data(self, data: str) -> bool:
        """Отправляет строку данных во внешнюю систему."""
        pass

class EmailServerDependency(ExternalDependency):
    def send_data(self, data: str) -> bool:
        print(f"[ИМИТАЦИЯ EMAIL] Отправка данных: {data}")
        return True