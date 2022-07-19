import os
import typing
import tempfile

import virtualbox

from communicator import generic


class Communicator(generic.Communicator):
    machine: virtualbox.library.IMachine

    @property
    def connected(self) -> bool:
        return self.machine.state == virtualbox.library.MachineState(5)

    @property
    def platform(self) -> str:
        return None

    @property
    def architecture(self) -> str:
        return None

    def __init__(self, machine: virtualbox.library.IMachine, username: str, password: str):
        self.machine = machine

    def execute(self, path: str, args: str = None, stdin: bytes = None) -> typing.Tuple[int, str, str]:
        raise NotImplementedError

    def upload(self, path: str, data: bytes):
        raise NotImplementedError

    def download(self, path: str) -> bytes:
        raise NotImplementedError
