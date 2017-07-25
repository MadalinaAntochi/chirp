from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.edit import CreateView, FormView

from message.forms import RegisterForm, MessageForm

from django.views.generic.list import ListView

#
from django.contrib.auth.models import User

from message.models import Message, Follow

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


# facuta de mine ( m-a ajutat Martin )
class MessageView(CreateView):
    form_class = MessageForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return redirect(self.get_success_url())


class ProfileBaseView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileBaseView, self).get_context_data(**kwargs)
        context["chirps"] = Message.objects.filter(user=self.get_object())

        following = Follow.objects.filter(following_user=self.request.user)
        context["following"] = [f.followed_user for f in following]

        followers = Follow.objects.filter(followed_user=self.request.user)
        context["followers"] = [f.following_user for f in following]

        return context


class MyProfileView(ProfileBaseView):
    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(ProfileBaseView):
    def get_slug_field(self):
        return "username"




def follow_user(request, username):
    print(username)

    user = get_object_or_404(User, username=username)
    try:
        follow = Follow(followed_user=user, following_user=request.user)
        follow.save()
        messages.info(request, "You are now following {0}".format(username))
    except IntegrityError:
        messages.error(request, "You are already following this user")


    return redirect('profile', username)