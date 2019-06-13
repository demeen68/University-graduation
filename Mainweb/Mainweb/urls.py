"""Mainweb URL Configuration

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
from django.conf.urls import include
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from background_ms.views import Index_layoutView
from user.views import SendKeyWordsEmailView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', Index_layoutView.as_view(), name='index_layout'),
    url(r'^backms/', include('background_ms.urls', namespace='backms')),
    url(r'^user/', include('user.urls', namespace='user')),
    # just for test
    # url(r'^test$', TemplateView.as_view(template_name='change_passwd.html')),
    url(r'^test$', SendKeyWordsEmailView.as_view()),
]

urlpatterns += staticfiles_urlpatterns()
