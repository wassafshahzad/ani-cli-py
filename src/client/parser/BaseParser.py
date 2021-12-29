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
        tag = self.soup.select(self.pageination_selector) or None
        if tag:
            tag = tag[-1].parent if tag[-1].name == "a" else tag[-1] #always check sibling of li tag
            return {
                "previous_page": tag.previous_sibling or None, 
                "next_page": tag.next_sibling or None }
        return {}