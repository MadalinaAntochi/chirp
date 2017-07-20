from django.contrib import admin

# Register your models here.

# pt a vedea in pagina web (cand ma loghez ca superuser) tabela Message
from message.models import Message

admin.site.register(Message)