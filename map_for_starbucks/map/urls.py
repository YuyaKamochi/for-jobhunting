from django.urls import path
from . import views

app_name = "map"

urlpatterns = [
    path('', views.MapView.as_view(), name='map'),
    path('excel/', views.ExcelView.as_view(), name='excel'),
    path('excel/update_data/', views.UpdateDataView, name='update_data'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('import_list/', views.import_list.as_view(),name='import_list'),
    path('add_shop/', views.AddShopView.as_view(), name='add_shop'),
]
