from enum import Enum

class APIkey(Enum):
    PRODUCION_KEY = ("RGAPI-82d303c3-356f-4cbe-83b6-6ac2ca16567c")

    @property
    def str_key(self):
        return self.value