from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.search, name="asset_search"),
    path('<search_id>', views.search, name="link"),
    path(r'get_assets/', views.get_assets, name='get_assets'),
    path('detail/<int:pk>/', views.AssetDetailView.as_view(), name="detail"),
    path('update/<int:pk>', views.AssetUpdateView.as_view(), name="update"),
    path(r'save_search/', views.save_quick_search, name="save_search"),
]
