from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='reserva_list', permanent=False)),
    path('registro/', views.RegistroDocenteView.as_view(), name='registro'),
    path('reservas/', views.ReservaListView.as_view(), name='reserva_list'),
    path('reservas/nueva/', views.ReservaCreateView.as_view(), name='reserva_create'),
    path('reservas/<int:pk>/editar/', views.ReservaUpdateView.as_view(), name='reserva_update'),
    path('reservas/<int:pk>/eliminar/', views.ReservaDeleteView.as_view(), name='reserva_delete'),
    path('reservas/<int:pk>/estado/', views.ReservaCambiarEstadoView.as_view(), name='reserva_estado'),
    path('estadisticas/', views.EstadisticasView.as_view(), name='estadisticas'),
    path('exportar/csv/', views.ExportarCSVView.as_view(), name='exportar_csv'),
]