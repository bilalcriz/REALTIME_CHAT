from django.forms import ModelForm
from .models import *


class ChatMessageForm(ModelForm):

  class Meta:
    model = ChatMessage
    fields = ['body']