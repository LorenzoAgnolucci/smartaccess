from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'rfid'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),
                  path('add_card/', views.add_card, name='add_card'),
                  path('add_card_scan/', views.AddCardScanView.as_view(), name='add_card_scan'),
                  path('write_card/', views.write_card, name='write_card'),
                  path('write_card_scan/', views.WriteCardScanView.as_view(), name='write_card_scan'),
                  path('access/', views.AccessMainView.as_view(), name='access_main'),
                  path('access/result/', views.access_result, name='access_result'),
                  path('access/result/<int:card_id>/', views.access_result, name='access_result'),
                  path('accounts/', include('django.contrib.auth.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
