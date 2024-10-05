import os
from unittest.mock import patch, mock_open

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, override_settings

from archive_receiver.settings import RECEIVE_URL_SECRET
from receiver.models import ReceivedFile

TARGET_FOLDER = "test_files"


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_get(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Ping OK")


# Create a dummy file-like object to use in tests
class ReceiveFileViewTest(TestCase):

    @override_settings(RECEIVE_URL_SECRET=RECEIVE_URL_SECRET)
    def setUp(self):
        self.client = Client()
        self.url = f"/{RECEIVE_URL_SECRET}/"
        os.makedirs(TARGET_FOLDER, exist_ok=True)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.join", return_value=os.path.join(TARGET_FOLDER, "test_file.txt"))
    def test_receive_file_post(self, mock_path_join, mock_open_file):
        file_name = "test_file.bin"
        file_content = b"Hello, this is a test file."

        response = self.client.post(
            self.url,
            {"file": SimpleUploadedFile(file_name, file_content)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Saved")
        mock_open_file().write.assert_called_once_with(file_content)
        self.assertEqual(ReceivedFile.objects.all().count(), 1)
