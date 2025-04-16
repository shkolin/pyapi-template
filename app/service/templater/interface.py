from abc import ABC
from abc import abstractmethod
from jinja2 import Template


class TemplaterInterface(ABC):
    @abstractmethod
    def get_template(self, name: str) -> Template:
        raise NotImplementedError
