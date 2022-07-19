import pytest

import communicator


def test_generic():
    instance = communicator.Communicator()
    with pytest.raises(NotImplementedError):
        assert instance.connected

    with pytest.raises(NotImplementedError):
        status, stdout, stderr = instance.execute("ping")

    with pytest.raises(NotImplementedError):
        instance.upload("C:\\temp\\test.txt", b"Hello!")

    with pytest.raises(NotImplementedError):
        data = instance.download("C:\\temp\\test.txt")
