from django.db import models


class ImportRTplanDCM(models.Model):
    rtplan = models.FileField()