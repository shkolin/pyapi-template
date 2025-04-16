from pathlib import Path
from typing import Any
from typing import Optional
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template
from jinja2 import TemplateNotFound

from app.service.templater.exception import TemplateNotFoundError
from app.service.templater.interface import TemplaterInterface


class Templater(TemplaterInterface):
    def __init__(self, frontend_base_url: str) -> None:
        self.__frontend_base_url = frontend_base_url
        search_path = Path(__file__).parent.parent.parent.parent.absolute() / 'templates'
        environment = Environment(
            loader=FileSystemLoader([search_path]),
            autoescape=True
        )
        environment.globals['url'] = self.__url
        self.jinja_env = environment

    def get_template(self, name: str) -> Template:
        try:
            template = self.jinja_env.get_template(f'{name}.html')
        except TemplateNotFound:
            raise TemplateNotFoundError
        return template

    def __url(self, path: Optional[str] = None, fragment: Optional[str] = None, **kwargs: Any) -> str:
        base_url = self.__frontend_base_url
        url_parts = list(urlparse(base_url))
        url_parts[2] = path or ''
        url_parts[4] = urlencode(kwargs) if kwargs else ''
        url_parts[5] = fragment if fragment else ''
        return str(urlunparse(url_parts))
