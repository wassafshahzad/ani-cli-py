import requests
from .AnimeClient import BaseClient
from .parser.BaseParser import BaseParser
from .Page import Page

class GogoAnimeClient(BaseClient):
    
    BASE_URL= "https://www1.gogoanime.cm/{}"
    BASE_SEARCH_URL=BASE_URL.format("/search.html?keyword={name}")
    ANIME_SELECTOR = "p.name a"
    ANIME_PAGINATION_SELECTOR = "ul.pagination-list li.selected"
    EPISODE_SELECTOR = "ul#episode_related li a"
    EPISODE_PAGINATION_SELECTOR= "ul#episode_page li a.active"
    CURRENT_OBJ_SELECTOR = ANIME_SELECTOR
    CURRENT_PAGINATION_SELECTOR = ANIME_PAGINATION_SELECTOR

    
    def __init__(self):
        self.requester = requests.Session()
        self.requester.headers.update(GogoAnimeClient.HEADERS)
    
    @staticmethod
    def _change_elector(type):
        GogoAnimeClient.CURRENT_OBJ_SELECTOR = getattr(GogoAnimeClient, f"{type}_SELECTOR")
        GogoAnimeClient.CURRENT_PAGINATION_SELECTOR = getattr(GogoAnimeClient, f"{type}_PAGINATION_SELECTOR")

    
    def get_search_page(self, link, items_selector, pagination_selector):
        value = 3
        page = self.requester.get(link, timeout=(3.05,value)).text
        self.page_parser = BaseParser(items_selector, page, pagination_selector)
        links = self.page_parser.get_links()
        pagination = self.page_parser.get_tag_sibling()
        return Page(**pagination, obj=links)
    

    def get_anime(self, name):
        GogoAnimeClient._change_elector("ANIME")
        link = GogoAnimeClient.BASE_SEARCH_URL.format(name=name)
        return self.get_search_page(link, 
            GogoAnimeClient.CURRENT_OBJ_SELECTOR, 
            GogoAnimeClient.CURRENT_PAGINATION_SELECTOR)
    
    def next_page(self,page):
        link = GogoAnimeClient.BASE_URL.format(page.next_page.a["href"])
        return self.get_search_page(link, 
            GogoAnimeClient.CURRENT_OBJ_SELECTOR, 
            GogoAnimeClient.CURRENT_PAGINATION_SELECTOR)

    def previous_page(self, page):
        link = GogoAnimeClient.BASE_URL.format(
            page.previous_page.a["href"])
        return self.get_search_page(link, 
            GogoAnimeClient.CURRENT_OBJ_SELECTOR, 
            GogoAnimeClient.CURRENT_PAGINATION_SELECTOR)
    
    def get_episode_page(self, index, page):
        GogoAnimeClient._change_elector("EPISODE")
        link = GogoAnimeClient.BASE_URL.format(page.obj[index]["href"])
        return self.get_search_page(link, 
            GogoAnimeClient.CURRENT_OBJ_SELECTOR, 
            GogoAnimeClient.CURRENT_PAGINATION_SELECTOR)

if __name__ == "__main__":
    obj = GogoAnimeClient()
    page = obj.get_anime("nar")
    page = obj.next_page(page)
    page = obj.get_episode_page(0, page)