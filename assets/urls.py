from django.urls import path
from .views import DashboardView, AssetListView, AssetCreateView, SignUpView, MaintenanceCreateView,AssetUpdateView, AssetDeleteView, AssetHistoryView, AssetRevertView, AssetMaintenanceView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/', AssetListView.as_view(), name='asset-list'),
    path('create/', AssetCreateView.as_view(), name='asset-create'),
    path('update/<int:pk>/', AssetUpdateView.as_view(), name='asset_update'),
    path('delete/<int:pk>/', AssetDeleteView.as_view(), name='asset_delete'),
    path('register/', SignUpView.as_view(), name='register'),
    path('asset/<int:pk>/logs', AssetMaintenanceView.as_view(), name='asset_maintenance_logs'),
    path('asset/<int:pk>/maintain', MaintenanceCreateView.as_view(), name='asset_maintain'),
    path('<int:pk>/history/', AssetHistoryView.as_view(), name = 'asset_history'),
    path('<int:pk>/history/<int:history_id>/revert', AssetRevertView.as_view(), name='asset_revert')
]