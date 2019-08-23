from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views

app_name = 'rfid'
urlpatterns = [
                  path('', views.IndexView.as_view(), name='index'),

                  path('add_card/', views.add_card, name='add_card'),
                  path('add_card_scan/', views.AddCardScanView.as_view(), name='add_card_scan'),

                  path('write_card/', views.write_card, name='write_card'),
                  path('write_card_scan/', views.WriteCardScanView.as_view(), name='write_card_scan'),

                  path('info_card/', views.info_card, name='info_card'),
                  path('info_card_scan/', views.InfoCardScanView.as_view(), name='info_card_scan'),

                  path('delete_card/', views.delete_card, name='delete_card'),
                  path('delete_card_scan/', views.DeleteCardScanView.as_view(), name='delete_card_scan'),

                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('logs', views.logs, name='logs'),

                  path('access/', views.AccessMainView.as_view(), name='access_main'),
                  path('access/result/', views.access_result, name='access_result'),
                  path('access/result/<int:card_id>/', views.access_result, name='access_result'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
