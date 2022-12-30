import os

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from receiver.models import ReceivedFile
from huld_archive_receiver.settings import TARGET_FOLDER


class IndexView(View):
    def get(self, request):
        return HttpResponse("Ping OK")


@method_decorator(csrf_exempt, name='dispatch')
class ReceiveFileView(View):
    def post(self, request):
        for filename, received_file in request.FILES.items():
            with open(os.path.join(TARGET_FOLDER, filename), "wb") as file:
                file.write(received_file.read())
                received_file_record = ReceivedFile(filename=filename)
                received_file_record.save()
        return HttpResponse('Saved', status=200)
