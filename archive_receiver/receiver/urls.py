from django.urls import path
from receiver.views import IndexView, ReceiveFileView

from archive_receiver.settings import RECEIVE_URL_SECRET

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(f"{RECEIVE_URL_SECRET}/", ReceiveFileView.as_view(), name="receive_file"),
]
