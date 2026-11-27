from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import AuditLog, RiwayatLogin

# Fungsi helper untuk mencatat audit log aktivitas
def catat_log(user, pesan):
    AuditLog.objects.create(user=user, aktivitas=pesan)

# Fungsi helper untuk mencatat riwayat login otomatis
def catat_riwayat_login(user, request):
    ip = request.META.get('REMOTE_ADDR')
    RiwayatLogin.objects.create(user=user, ip_address=ip)

# Halaman Manajemen User (sekaligus nampilin 20 riwayat login terakhir)
@login_required(login_url='landing:login')
def manajemen_user_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak! Halaman khusus Super Admin.")
        return redirect('landing:dashboard_admin')
    
    users = User.objects.all().order_by('-date_joined')
    riwayat_login = RiwayatLogin.objects.all().order_by('-waktu_login')[:20]
    
    return render(request, 'landing/admin/manajemen_user.html', {
        'users': users,
        'riwayat_login': riwayat_login
    })

# Halaman Audit Log Aktivitas Admin
@login_required(login_url='landing:login')
def audit_log_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak!")
        return redirect('landing:dashboard_admin')
        
    logs = AuditLog.objects.all().order_by('-waktu')
    return render(request, 'landing/admin/audit_log.html', {'logs': logs})