from dataclasses import dataclass
from typing import Type
from bs4 import BeautifulSoup


@dataclass
class BaseParser:
    obj_selector: str
    page_html: str
    pageination_selector: str = ''

    def __post_init__(self) -> None:
        self.soup = self._get_parser()
    
    def _get_parser(self):
        return BeautifulSoup(self.page_html, 'html.parser')

    def get_links(self):
        return self.soup.select(self.obj_selector)

    def get_tag_sibling(self):
        tag = self.soup.select(self.pageination_selector)[-1] or None
        if tag:
            tag = tag.parent if tag.name == "a" else tag #always check sibling of li tag
            return [ 
                tag.previous_sibling or None, 
                tag.next_sibling or None ]
        return []