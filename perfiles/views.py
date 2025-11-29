from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PerfilCandidato, PerfilEmpresa
from .forms import PerfilCandidatoForm, PerfilEmpresaForm


# ============================================================
# REDIRECCIÓN PRINCIPAL SEGÚN PERFIL Y ESTADO
# ============================================================
@login_required
def perfil_inicio(request):
    user = request.user

    # --------------------------------------------------------
    # EMPRESA
    # --------------------------------------------------------
    if user.rol == 'empresa':
        perfil = PerfilEmpresa.objects.filter(usuario=user).first()

        # Si NO tiene perfil aún → crearlo y enviarlo a completarlo
        if not perfil:
            perfil = PerfilEmpresa.objects.create(usuario=user, nombre_empresa=user.first_name)
            return redirect('perfiles:perfil_empresa')

        # Si ya está completo
        if perfil.completado:
            return redirect('perfiles:dashboard_empresa')

        # Si no está completo
        return redirect('perfiles:perfil_empresa')

    # --------------------------------------------------------
    # CANDIDATO
    # --------------------------------------------------------
    if user.rol == 'candidato':
        perfil = PerfilCandidato.objects.filter(usuario=user).first()

        if not perfil:
            perfil = PerfilCandidato.objects.create(usuario=user)
            return redirect('perfiles:perfil_candidato')

        if perfil.completado:
            return redirect('perfiles:dashboard_candidato')

        return redirect('perfiles:perfil_candidato')

    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------
    if user.rol == 'admin':
        return redirect('/admin/')

    return redirect('/')


# ============================================================
# PERFIL CANDIDATO (FORMULARIO)
# ============================================================
@login_required
def perfil_candidato(request):
    perfil = PerfilCandidato.objects.get(usuario=request.user)

    if request.method == "POST":
        form = PerfilCandidatoForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            perfil.completado = True
            perfil.save()
            return redirect('perfiles:dashboard_candidato')
    else:
        form = PerfilCandidatoForm(instance=perfil)

    return render(request, 'perfiles/perfil_candidato.html', {
        'form': form,
        'perfil': perfil,
    })


# ============================================================
# PERFIL EMPRESA (FORMULARIO)
# ============================================================
@login_required
def perfil_empresa(request):
    perfil = PerfilEmpresa.objects.get(usuario=request.user)

    if request.method == "POST":
        form = PerfilEmpresaForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            perfil.completado = True
            perfil.save()
            return redirect('perfiles:dashboard_empresa')
    else:
        form = PerfilEmpresaForm(instance=perfil)

    return render(request, 'perfiles/perfil_empresa.html', {
        'form': form,
        'perfil': perfil,
    })


# ============================================================
# DASHBOARD CANDIDATO
# ============================================================
@login_required
def dashboard_candidato(request):
    perfil = get_object_or_404(PerfilCandidato, usuario=request.user)
    return render(request, 'perfiles/dashboard_candidato.html', {'perfil': perfil})


# ============================================================
# DASHBOARD EMPRESA
# ============================================================
@login_required
def dashboard_empresa(request):
    perfil = get_object_or_404(PerfilEmpresa, usuario=request.user)
    return render(request, 'perfiles/dashboard_empresa.html', {'perfil': perfil})
