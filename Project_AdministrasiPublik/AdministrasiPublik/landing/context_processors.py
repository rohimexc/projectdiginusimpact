import uuid
from django.utils import timezone


def visitor_count_processor(request):
    """
    Context processor otomatis untuk mencatat dan menghitung jumlah pengunjung web:
    - Hari ini: Dihitung dengan baseline 20 + jumlah kunjungan aktif
    - Total: Dihitung secara kumulatif dengan baseline 6320 + jumlah kunjungan
    """
    try:
        from .models import PengunjungWeb

        # Pastikan sesi aktif untuk pengunjung
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key or 'anon'

        today = timezone.localdate()

        # Dapatkan IP address (mendukung reverse proxy / load balancer di PythonAnywhere)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Catat setiap kunjungan ke database agar selalu bertambah dinamis
        # Menggunakan suffix unik agar setiap kunjungan / refresh tercatat tanpa bentrok unique_together
        visit_key = f"{session_key}_{uuid.uuid4().hex[:8]}"
        PengunjungWeb.objects.create(
            tanggal=today,
            session_key=visit_key,
            ip_address=ip
        )

        # Baseline: jika baru/reset, minimal langsung 20
        BASE_HARI_INI = 20
        BASE_TOTAL = 6320

        count_hari_ini = BASE_HARI_INI + PengunjungWeb.objects.filter(tanggal=today).count()
        total_count = BASE_TOTAL + PengunjungWeb.objects.count()

        return {
            'pengunjung_hari_ini': f"{count_hari_ini:04d}",
            'total_pengunjung': f"{total_count:06d}"
        }
    except Exception:
        return {
            'pengunjung_hari_ini': '0020',
            'total_pengunjung': '006340'
        }

