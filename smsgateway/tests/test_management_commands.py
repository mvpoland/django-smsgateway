import mock

from django.core.management import call_command
from django.test import TestCase


class RecvSmsesCommandTestCase(TestCase):
    def setUp(self):
        self.recv_smses_mock = mock.patch(
            "smsgateway.management.commands.recv_smses.recv_smses"
        ).start()
        self.addCleanup(mock.patch.stopall)

    def test_success(self):
        # arrange
        args = ()
        kwargs = {"backend": "weirdo"}

        # act
        call_command("recv_smses", *args, **kwargs)

        # assert
        self.recv_smses_mock.assert_called_once_with("weirdo", False)

    def test_success_explicit_run_async(self):
        # arrange
        args = (
            "--run_async",
        )
        kwargs = {"backend": "weirdo"}

        # act
        call_command("recv_smses", *args, **kwargs)

        # assert
        self.recv_smses_mock.assert_called_once_with("weirdo", True)


class SendSmsesCommandTestCase(TestCase):
    def setUp(self):
        self.send_smses_mock = mock.patch(
            "smsgateway.management.commands.send_smses.send_smses"
        ).start()
        self.addCleanup(mock.patch.stopall)

    def test_success(self):
        # arrange
        args = ()
        kwargs = {}

        # act
        call_command("send_smses", *args, **kwargs)

        # assert
        self.send_smses_mock.assert_called_once_with(False, None, None)
