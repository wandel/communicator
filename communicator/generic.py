import typing


class Communicator:

    @property
    def connected(self) -> bool:
        raise NotImplementedError

    @property
    def platform(self) -> str:
        return None

    @property
    def architecture(self) -> str:
        return None

    def execute(self, path: str, args: str = None, stdin=bytes) -> typing.Tuple[int, str, str]:
        raise NotImplementedError

    def upload(self, path: str, data: bytes):
        raise NotImplementedError

    def download(self, path: str) -> bytes:
        raise NotImplementedError
