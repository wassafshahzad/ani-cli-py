from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseClient(ABC):

    # Headers to bypass reCapcha
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169"
        "Safari/537.36",
        "referer": "https://www.google.com/",
    }

    @abstractmethod
    def get_anime(self, name):
        pass

    @abstractmethod
    def get_episode_page(self, name):
        pass
    
    @abstractmethod
    def next_page(self):
        pass

    @abstractmethod
    def previous_page(self):
        pass