from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView

from message.forms import RegisterForm

from django.views.generic.list import ListView


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    #ma duce pe pagina principala
    success_url = "/"

class TimelineView(ListView):
    template_name = 'index.html'
    def get_queryset(self):
        # implement the logic
        pass