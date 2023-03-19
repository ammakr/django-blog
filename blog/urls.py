

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts', views.PostsView.as_view(), name='posts'),
    path('posts/<slug:slug>', views.SingleView.as_view(), name='single'),
    path('later', views.LaterView.as_view(), name='later')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
