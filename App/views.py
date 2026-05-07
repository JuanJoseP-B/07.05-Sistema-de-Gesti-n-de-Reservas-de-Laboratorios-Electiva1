import csv

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView, DeleteView, FormView, ListView, TemplateView, UpdateView,
)

from .forms import FiltroReservaForm, RegistroDocenteForm, ReservaForm
from .models import Reserva


class RegistroDocenteView(FormView):
    template_name = 'App/registro.html'
    form_class = RegistroDocenteForm
    success_url = reverse_lazy('reserva_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('reserva_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class EsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'App/reserva_lista.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        if self.request.user.is_staff:
            qs = Reserva.objects.select_related('usuario').all()
        else:
            qs = Reserva.objects.filter(usuario=self.request.user)

        fecha = self.request.GET.get('fecha')
        laboratorio = self.request.GET.get('laboratorio')

        if fecha:
            qs = qs.filter(fecha=fecha)
        if laboratorio:
            qs = qs.filter(laboratorio__icontains=laboratorio)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filtro_form'] = FiltroReservaForm(self.request.GET or None)
        return ctx


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'App/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nueva Reserva'
        return ctx


class ReservaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'App/reserva_form.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        reserva = self.get_object()
        return reserva.usuario == self.request.user and reserva.estado == 'pendiente'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Reserva'
        return ctx


class ReservaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reserva
    template_name = 'App/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva_list')

    def test_func(self):
        reserva = self.get_object()
        return reserva.usuario == self.request.user and reserva.estado == 'pendiente'


class ReservaCambiarEstadoView(LoginRequiredMixin, EsAdminMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk)
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['aprobada', 'rechazada']:
            reserva.estado = nuevo_estado
            reserva.save()
        return redirect('reserva_list')


class EstadisticasView(LoginRequiredMixin, EsAdminMixin, TemplateView):
    template_name = 'App/estadisticas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total'] = Reserva.objects.count()
        ctx['por_estado'] = Reserva.objects.values('estado').annotate(total=Count('id'))
        ctx['por_laboratorio'] = (
            Reserva.objects.values('laboratorio')
            .annotate(total=Count('id'))
            .order_by('-total')
        )
        return ctx


class ExportarCSVView(LoginRequiredMixin, EsAdminMixin, View):
    def get(self, request):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="reservas.csv"'
        response.write('﻿')  # BOM para que Excel abra correctamente con tildes

        writer = csv.writer(response)
        writer.writerow([
            'Usuario', 'Laboratorio', 'Fecha',
            'Hora inicio', 'Hora fin', 'Estado', 'Motivo', 'Fecha creación',
        ])

        for r in Reserva.objects.select_related('usuario').all():
            writer.writerow([
                r.usuario.get_full_name() or r.usuario.username,
                r.laboratorio,
                r.fecha,
                r.hora_inicio.strftime('%H:%M'),
                r.hora_fin.strftime('%H:%M'),
                r.get_estado_display(),
                r.motivo,
                r.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
            ])

        return response
