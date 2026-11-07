from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Kolom yang ditampilkan pada tabel data
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    
    # 1. FILTER: Opsi penyaringan data di sidebar kanan
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    
    # 2. SEARCH: Bilah pencarian akun berdasarkan username, nama, atau email
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # 3. SORT: Pengurutan default (terbaru berdasarkan tanggal bergabung)
    ordering = ('-date_joined',)

    # Penyesuaian form detail edit di dalam panel admin Django
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informasi Tambahan & Role', {'fields': ('role', 'nomor_telepon', 'alamat')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informasi Tambahan & Role', {'fields': ('role', 'email', 'nomor_telepon')}),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('waktu', 'user', 'aksi', 'deskripsi')
    
    # Filter log berdasarkan aksi dan rentang waktu
    list_filter = ('aksi', 'waktu')
    
    # Pencarian log berdasarkan nama user atau keterangan
    search_fields = ('user__username', 'aksi', 'deskripsi')
    
    # Urutkan dari aktivitas yang paling baru
    ordering = ('-waktu',)