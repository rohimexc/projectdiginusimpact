from django.utils import timezone
from .models import Pengunjung, PengunjungTotal


def get_client_ip(request):
    """Mendapatkan alamat IP asli pengunjung meskipun berada di balik proxy / load balancer"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def statistik_pengunjung(request):
    """
    Context processor otomatis untuk:
    1. Mencatat kunjungan unik pengunjung ke database setiap hari.
    2. Menyediakan variabel 'pengunjung_hari_ini' dan 'pengunjung_total' ke seluruh template secara global.
    """
    today = timezone.localdate()
    path = request.path_info or ''

    # Abaikan request internal: admin, static, media, ckeditor, favicon
    is_asset_or_admin = any(
        path.startswith(prefix) for prefix in (
            '/admin/', '/static/', '/media/', '/ckeditor5/', '/favicon.ico'
        )
    )

    if not is_asset_or_admin:
        try:
            # Pastikan sesi aktif tersedia
            if not request.session.session_key:
                request.session.save()

            session_key = request.session.session_key
            today_str = str(today)

            # Cek apakah sesi ini sudah tercatat hari ini
            if request.session.get('visited_today') != today_str:
                ip = get_client_ip(request)
                ua = request.META.get('HTTP_USER_AGENT', '')[:250]

                # Catat ke database
                Pengunjung.objects.create(
                    ip_address=ip,
                    session_key=session_key,
                    user_agent=ua,
                    path=path[:250],
                    tanggal=today
                )
                request.session['visited_today'] = today_str
        except Exception:
            pass

    # Hitung total kunjungan dan pengunjung hari ini
    try:
        config = PengunjungTotal.objects.first()
        base_total = config.total_awal if config else 6320
        base_today = config.hari_ini_awal if config else 24

        total_db = Pengunjung.objects.count()
        today_db = Pengunjung.objects.filter(tanggal=today).count()

        total_pengunjung = base_total + total_db
        hari_ini_pengunjung = base_today + today_db
    except Exception:
        total_pengunjung = 6320
        hari_ini_pengunjung = 24

    return {
        'pengunjung_hari_ini': f"{hari_ini_pengunjung:04d}",
        'pengunjung_total': f"{total_pengunjung:06d}",
    }
