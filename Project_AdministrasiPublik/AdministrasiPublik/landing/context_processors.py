from django.utils import timezone


def visitor_count_processor(request):
    """
    Context processor otomatis untuk mencatat dan menghitung jumlah pengunjung web:
    - Hari ini: Dihitung berdasarkan sesi unik per tanggal hari ini
    - Total: Dihitung secara kumulatif dengan baseline 6320
    """
    try:
        from .models import PengunjungWeb

        # Pastikan sesi aktif untuk pengunjung
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        today = timezone.localdate()

        # Dapatkan IP address (mendukung reverse proxy / load balancer di PythonAnywhere)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Catat pengunjung unik per hari
        if session_key:
            PengunjungWeb.objects.get_or_create(
                tanggal=today,
                session_key=session_key,
                defaults={'ip_address': ip}
            )

        # Hitung statistik pengunjung
        count_hari_ini = PengunjungWeb.objects.filter(tanggal=today).count()
        total_count = 6320 + PengunjungWeb.objects.count()

        return {
            'pengunjung_hari_ini': f"{count_hari_ini:04d}",
            'total_pengunjung': f"{total_count:06d}"
        }
    except Exception:
        return {
            'pengunjung_hari_ini': '0001',
            'total_pengunjung': '006321'
        }
