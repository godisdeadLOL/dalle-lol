class KeyStashEmptyException(Exception):
    pass


class GenerationFailedException(Exception):
    def __init__(self, detail, status_code=400):
        self.status_code = status_code
        self.detail = detail


class RegenerateException(Exception):
    pass
