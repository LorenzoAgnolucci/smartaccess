from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path('add_card/', views.add_card, name='add_card'),
                  path('write_card/', views.write_card, name='write_card'),
                  path('access/', views.access, name='access')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
