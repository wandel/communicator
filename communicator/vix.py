import os
import typing
import tempfile

import vix

from communicator import generic


class Communicator(generic.Communicator):
    vixobj: vix.VixVM

    @property
    def connected(self) -> bool:
        return self.vixobj.is_running

    @property
    def platform(self) -> str:
        return None

    @property
    def architecture(self) -> str:
        return None

    def __init__(self, vixobj: vix.VixVM, username: str, password: str):
        self.vixobj = vixobj
        self.vixobj.login(username, password, require_interactive=True)

    def execute(
        self, path: str, args: str = None, stdin: bytes = None
    ) -> typing.Tuple[int, str, str]:
        assert not stdin, "stdin is not supported yet"
        job = self.vixobj.proc_run(path, command_line=args, should_block=True)
        return job.exit_code, None, None

    def upload(self, path: str, data: bytes):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            try:
                f.write(data)
                f.close()
                self.vixobj.copy_host_to_guest(f.name, path)
            finally:
                os.unlink(f.name)

    def download(self, path: str) -> bytes:
        with tempfile.NamedTemporaryFile("rb", delete=False) as tmp:
            try:
                tmp.close()
                self.vixobj.copy_guest_to_host(path, tmp.name)
                with open(tmp.name, "rb") as f:
                    return f.read()
            finally:
                os.unlink(tmp.name)
