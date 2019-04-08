import factory
from .models import MyAttachFile


class MyAttachFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MyAttachFile
