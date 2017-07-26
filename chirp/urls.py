"""chirp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

# as este folosit pt a eticheta views (folosesc eticheta)
from django.contrib.auth import views as auth_views

from message.views import RegisterView, TimelineView, MyProfileView, ProfileView, MessageView, follow_user, \
    unfollow_user, ProfilesView

# se adauga la link-ul paginii web: http://127.0.0.1:8000/    -->    register/
#il folosesc in template/base.html     astfel-->   <a href="{% url 'register' %}" ...>

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TimelineView.as_view(), name='index'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='logout'),
    url(r'^message/$', MessageView.as_view(), name='message'),
    url(r'^my-profile/$', login_required(MyProfileView.as_view()), name='my-profile'),
    url(r'^profile/(?P<slug>[-\w]+)/$', login_required(ProfileView.as_view()), name='profile'),

    url(r'^follow/(?P<username>[-\w]+)/$', login_required(follow_user), name='follow_user'),

    url(r'^unfollow/(?P<username>[-\w]+)/$', login_required(unfollow_user), name='unfollow_user'),

    url(r'^profiles/$', login_required(ProfilesView.as_view()), name='profiles'),
]