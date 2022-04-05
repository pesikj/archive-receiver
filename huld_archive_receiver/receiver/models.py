from django.db import models


class ReceivedFile(models.Model):
    received_on = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=200)
