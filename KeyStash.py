import config


class KeyInfo:
    key: str
    status: str

    def __init__(self, key):
        self.key = key
        self.status = "ok"


class KeyStash:
    keys_info: list[KeyInfo] = []
    last: int = 0

    def __init__(self):
        self.keys_info = [KeyInfo(key) for key in config.API_KEYS]

    def next_key(self) -> str | None:
        total = len(self.keys_info)
        for _ in range(total):
            self.last = (self.last + 1) % total
            cur = self.keys_info[self.last]
            if cur.status == "ok":
                return cur.key

        return None

    def update_status(self, key: str, status: str):
        info = next((info for info in self.keys_info if info.key == key), None)

        if info:
            info.status = status
