
class MissingSearchItemError(Exception):
    def __init__(self):
        self.message = "\"search_item\" as 2nd argument is missing."
        super().__init__(self.message)
