import os
import tempfile
import unittest.mock

import vix
import pytest

import communicator


def load_data(data: bytes):
    def inner(src, dst):
        with open(dst, "rb") as f:
            assert data == f.read()

    return inner


class VixTestCase(unittest.TestCase):
    def test_connected(self):
        mock = unittest.mock.Mock()
        instance = communicator.Vix(mock, "username", "password")

        with unittest.mock.patch.object(mock, "is_running", True):
            assert instance.connected

        with unittest.mock.patch.object(mock, "is_running", False):
            assert not instance.connected

    def test_execute(self):
        mock = unittest.mock.Mock()
        instance = communicator.Vix(mock, "username", "password")

        with unittest.mock.patch.object(
            mock, "proc_run", return_value=unittest.mock.sentinel
        ):
            status, stdout, stderr = instance.execute("ping")
            assert status == unittest.mock.sentinel.exit_code
            assert stdout is None
            assert stderr is None

    def test_upload(self):
        mock = unittest.mock.Mock()
        instance = communicator.Vix(mock, "username", "password")

        expected = os.urandom(4096)

        def side_effect(src, dst):
            with open(src, "rb") as f:
                assert expected == f.read()

        with unittest.mock.patch.object(
            mock, "copy_host_to_guest", side_effect=side_effect
        ):
            instance.upload("C:\\temp\\test.txt", expected)

    def test_download(self):
        mock = unittest.mock.Mock()
        instance = communicator.Vix(mock, "username", "password")

        expected = os.urandom(4096)

        def side_effect(src, dst):
            with open(dst, "wb") as f:
                f.write(expected)

        with unittest.mock.patch.object(
            mock, "copy_guest_to_host", side_effect=side_effect
        ):
            data = instance.download("C:\\temp\\test.txt")
        assert data == expected
