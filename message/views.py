from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.edit import CreateView

from message.forms import RegisterForm, MessageForm

from django.views.generic.list import ListView

#
from django.contrib.auth.models import User

from message.models import Message

# cred ca la pagina -> template_name, apare formularul -> form_class

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'

    #ma duce pe pagina principala
    success_url = "/"

# nu merge.....................

# vizualizare cronologica a mesajelor user-ilor
class TimelineView(ListView):
    template_name = 'index.html'

    #model='message'

    def get_queryset(self):
        # implement the logic
        if self.request.user.is_authenticated:
            return Message.objects.filter(user=self.request.user)
        else:
            return Message.objects.all()



class MessageView(CreateView):
    form_class = MessageForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return redirect(self.get_success_url())