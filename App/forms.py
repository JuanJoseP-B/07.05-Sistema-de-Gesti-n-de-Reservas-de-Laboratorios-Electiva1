from django import forms
from django.contrib.auth.models import User
from .models import Reserva


class RegistroDocenteForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_staff = False  # siempre docente
        if commit:
            user.save()
        return user


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['laboratorio', 'fecha', 'hora_inicio', 'hora_fin', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'laboratorio': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        fecha = cleaned_data.get('fecha')
        laboratorio = cleaned_data.get('laboratorio')

        if hora_inicio and hora_fin:
            if hora_fin <= hora_inicio:
                raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')

        if fecha and laboratorio and hora_inicio and hora_fin:
            conflictos = Reserva.objects.filter(
                laboratorio__iexact=laboratorio,
                fecha=fecha,
                estado__in=['pendiente', 'aprobada'],
            ).exclude(pk=self.instance.pk if self.instance.pk else None)

            for reserva in conflictos:
                if not (hora_fin <= reserva.hora_inicio or hora_inicio >= reserva.hora_fin):
                    raise forms.ValidationError(
                        f'Conflicto de horario: ya existe una reserva en "{laboratorio}" '
                        f'de {reserva.hora_inicio.strftime("%H:%M")} a {reserva.hora_fin.strftime("%H:%M")}.'
                    )

        return cleaned_data


class FiltroReservaForm(forms.Form):
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    laboratorio = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del laboratorio'})
    )
