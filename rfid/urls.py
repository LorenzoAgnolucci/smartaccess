from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'rfid'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('add_card/', views.add_card, name='add_card'),
                  path('write_card/', views.write_card, name='write_card'),
                  path('access/', views.AccessMainView.as_view(), name='access_main'),
                  path('access/result/', views.access_result, name='access_result'),
                  path('access/result/<int:card_id>/', views.access_result, name='access_result')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
