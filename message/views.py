from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.db.utils import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.edit import CreateView, FormView

from message.forms import RegisterForm, MessageForm

from django.views.generic.list import ListView

#
from django.contrib.auth.models import User

from message.models import Message, Follow, Like


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
    # get_queryset = obtineti setul de interogari, aici se returneaza o lista care indeplineste niste conditii
    def get_queryset(self):
        # returneaza mesajele user-ului daca e logat altfel le returneaza pe toate
        #if self.request.user.is_authenticated:
        #    return Message.objects.filter(user=self.request.user).order_by("-created")
        #else:
        #    return Message.objects.all().order_by("-created")

        # -created = descrescator dupa data crearii
        return Message.objects.all().order_by("-created")


# facuta de mine ( m-a ajutat Martin )
class MessageView(CreateView):
    form_class = MessageForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return redirect(self.get_success_url())

# DetailView ( e legat de url ->slug=care se refera la un camp unic din tabela )  are functii:
# def get_context_data(..) = obtine date de context
# def get_object(..)
# def get_slug_field(..)

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

        following = Follow.objects.filter(following_user=self.get_object())
        context["following1"] = [f.followed_user for f in following]

        followers = Follow.objects.filter(followed_user=self.get_object())
        context["followers1"] = [f.following_user for f in followers]
        return context


class MyProfileView(ProfileBaseView):
    def get_object(self, queryset=None):
        return self.request.user


class ProfileView(ProfileBaseView):
    def get_slug_field(self):
        return "username"



def follow_user(request, username):
    #print(username)

    user = get_object_or_404(User, username=username)
    try:
        #imi creaza un follow in baza de date
        follow = Follow(followed_user=user, following_user=request.user)
        follow.save()

        messages.info(request, "You are now following {0}".format(username))

    except IntegrityError:
        messages.error(request, "You are already following this user")


    return redirect('profile', username)


# m-a ajutat Martin
def unfollow_user(request, username):

    user = get_object_or_404(User, username=username)
    try:
        # imi returneaza un follow din baza de date
        follow = Follow.objects.get(followed_user=user,following_user=request.user)
        follow.delete()

        messages.info(request, "You are now unfollowing {0}".format(username))

    except IntegrityError:
        messages.error(request, "You are already unfollowing this user")


    return redirect('profile', username)


class ProfilesView(ListView):
    model = User
    template_name = 'profiles.html'

    #ListView are functii care returneaza automat niste liste; de aceea se obtin atat de usor toti user-ii in functie de modelul dat: User
    context_object_name = 'users'

@csrf_exempt
def like_message(request):
    if request.method=='POST':
        #print('Sunt aici')

        message_id = request.POST.get('id')
        print (message_id)

        like_value = bool(int(request.POST.get('like')))
        print (like_value)

        message = get_object_or_404(Message, id=message_id)

        # daca apas pe like de 2 ori at se sterge like-ul, idem pt dislike
        try:
            like = Like.objects.get(user=request.user, message = message)

            if like.like == like_value:
                like.delete()
            else:
                like.like=like_value
                like.save()
        except Like.DoesNotExist:
            like=Like(user=request.user, message=message, like=like_value)
            like.save()

    return  JsonResponse({'succes':'true'})