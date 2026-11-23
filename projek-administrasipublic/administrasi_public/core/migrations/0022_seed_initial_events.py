from django.db import migrations
from datetime import date

def seed_events(apps, schema_editor):
    Event = apps.get_model('core', 'Event')
    if not Event.objects.exists():
        events_data = [
            {
                'judul': 'Seminar Nasional: Transformasi Digital Tata Kelola Publik Menuju Smart Governance',
                'slug': 'seminar-nasional-transformasi-digital',
                'kategori': 'Seminar',
                'tanggal_mulai': date(2026, 11, 28),
                'waktu': '08.30 WITA - 12.30 WITA',
                'lokasi': 'Auditorium FISIP Universitas Tadulako / Zoom Meeting',
                'poster': 'event_posters/poster_seminar_nasional.jpg',
                'deskripsi': '<p>Seminar nasional membahas strategi transformasi digital sektor publik dan tata kelola berbasis smart governance.</p>',
                'link_pendaftaran': 'https://bit.ly/daftar-seminar-ap',
                'is_active': True,
            },
            {
                'judul': 'Kuliah Tamu: Kebijakan Publik Berbasis Bukti (Evidence-Based Policy Making)',
                'slug': 'kuliah-tamu-kebijakan-publik-berbasis-bukti',
                'kategori': 'Kuliah Tamu',
                'tanggal_mulai': date(2026, 12, 5),
                'waktu': '09.00 WITA - 11.30 WITA',
                'lokasi': 'Ruang Teater FISIP Universitas Tadulako',
                'poster': 'event_posters/poster_kuliah_tamu.jpg',
                'deskripsi': '<p>Kuliah tamu bersama pakar kebijakan publik nasional membahas implementasi evidence-based policy making di Indonesia.</p>',
                'link_pendaftaran': 'https://bit.ly/kuliah-tamu-ap',
                'is_active': True,
            },
            {
                'judul': 'Workshop Metodologi Penelitian Kualitatif & Analisis Kebijakan Kontemporer',
                'slug': 'workshop-metodologi-penelitian-kualitatif',
                'kategori': 'Workshop',
                'tanggal_mulai': date(2026, 12, 12),
                'waktu': '08.00 WITA - 16.00 WITA',
                'lokasi': 'Lab Komputer & Kebijakan Publik FISIP UNTAD',
                'poster': 'event_posters/poster_workshop_metopel.jpg',
                'deskripsi': '<p>Workshop intensif penulisan tugas akhir dan analisis data kualitatif menggunakan NVivo.</p>',
                'link_pendaftaran': 'https://bit.ly/workshop-metopel-ap',
                'is_active': True,
            },
            {
                'judul': 'Rembuk Alumni & Lokakarya Kurikulum Administrasi Publik 2027',
                'slug': 'rembuk-alumni-lokakarya-kurikulum-2027',
                'kategori': 'Agenda Prodi',
                'tanggal_mulai': date(2026, 12, 20),
                'waktu': '13.00 WITA - Selesai',
                'lokasi': 'Ruang Rapat Senat FISIP Universitas Tadulako',
                'poster': 'event_posters/poster_rembuk_alumni.jpg',
                'deskripsi': '<p>Pertemuan silaturahmi alumni dan peninjauan kurikulum OBE Prodi Administrasi Publik FISIP UNTAD.</p>',
                'link_pendaftaran': '',
                'is_active': True,
            },
        ]
        for ev in events_data:
            Event.objects.create(**ev)

def rollback_events(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_event'),
    ]

    operations = [
        migrations.RunPython(seed_events, rollback_events),
    ]
