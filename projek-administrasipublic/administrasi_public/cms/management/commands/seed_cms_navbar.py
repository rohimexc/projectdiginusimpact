from django.core.management.base import BaseCommand
from cms.models import Page, Menu


class Command(BaseCommand):
    help = "Seed initial CMS Menus and sample Pages matching the existing website structure"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Memulai seeding data CMS Menu & Halaman..."))

        # 1. Bersihkan menu lama jika kosong atau bangun ulang dengan aman
        # Buat Halaman Demo CMS
        sample_page, _ = Page.objects.get_or_create(
            slug='panduan-mahasiswa-baru',
            defaults={
                'title': 'Panduan Mahasiswa Baru',
                'content_type': 'html',
                'status': 'published',
                'meta_description': 'Informasi resmi dan panduan orientasi bagi mahasiswa baru Program Studi Administrasi Publik FISIP UNTAD.',
                'html_content': '''
                    <h2>Selamat Datang di Program Studi Administrasi Publik</h2>
                    <p>Program Studi Sarjana Administrasi Publik Fakultas Ilmu Sosial dan Ilmu Politik Universitas Tadulako menyambut hangat seluruh mahasiswa baru.</p>
                    <blockquote>Pendidikan tata kelola sektor publik yang adaptif, berintegritas, dan berwawasan lingkungan.</blockquote>
                    <h3>Tahapan Penting Mahasiswa Baru:</h3>
                    <ul>
                        <li>Registrasi akun Siakad UNTAD</li>
                        <li>Pengisian Kartu Rencana Studi (KRS)</li>
                        <li>Orientasi Pengenalan Kehidupan Kampus bagi Mahasiswa Baru (PKKMB)</li>
                        <li>Pertemuan Penasihat Akademik (PA)</li>
                    </ul>
                '''
            }
        )

        # 2. Definisikan Struktur Menu Lengkap
        menus_data = [
            {
                'title': 'Beranda',
                'url_override': '/',
                'order': 1,
                'icon_class': 'fas fa-home',
                'target': '_self',
                'children': []
            },
            {
                'title': 'Tentang',
                'url_override': '#',
                'order': 2,
                'icon_class': 'fas fa-info-circle',
                'target': '_self',
                'children': [
                    {'title': 'Profil Program Studi', 'url_override': '/tentang/profil/', 'order': 1, 'icon_class': 'fas fa-university', 'target': '_self'},
                    {'title': 'Sejarah & Dasar Hukum', 'url_override': '/tentang/sejarah/', 'order': 2, 'icon_class': 'fas fa-scale-balanced', 'target': '_self'},
                    {'title': 'Visi, Misi & Tujuan', 'url_override': '/tentang/visi_misi/', 'order': 3, 'icon_class': 'fas fa-bullseye', 'target': '_self'},
                    {'title': 'Profil Lulusan', 'url_override': '/tentang/profil_lulusan/', 'order': 4, 'icon_class': 'fas fa-user-graduate', 'target': '_self'},
                    {'title': 'Sertifikat Akreditasi', 'url_override': '/tentang/akreditasi/', 'order': 5, 'icon_class': 'fas fa-award', 'target': '_self'},
                ]
            },
            {
                'title': 'Galeri',
                'url_override': '/galeri/',
                'order': 3,
                'icon_class': 'fas fa-images',
                'target': '_self',
                'children': []
            },
            {
                'title': 'Berita',
                'url_override': '/berita/',
                'order': 4,
                'icon_class': 'fas fa-newspaper',
                'target': '_self',
                'children': []
            },
            {
                'title': 'Event',
                'url_override': '/event/',
                'order': 5,
                'icon_class': 'fas fa-calendar-alt',
                'target': '_self',
                'children': []
            },
            {
                'title': 'Akademik',
                'url_override': '#',
                'order': 6,
                'icon_class': 'fas fa-graduation-cap',
                'target': '_self',
                'children': [
                    {'title': 'SIGA-8', 'url_override': 'https://siga-8.untad.ac.id', 'order': 1, 'icon_class': 'fas fa-desktop', 'target': '_blank'},
                    {'title': 'Kurikulum', 'url_override': '/akademik/kurikulum/', 'order': 2, 'icon_class': 'fas fa-book-open', 'target': '_self'},
                    {'title': 'Jadwal Perkuliahan', 'url_override': '/akademik/jadwal/', 'order': 3, 'icon_class': 'fas fa-calendar-alt', 'target': '_self'},
                    {'title': 'RPS', 'url_override': '/akademik/rps/', 'order': 4, 'icon_class': 'fas fa-file-signature', 'target': '_self'},
                    {'title': 'Panduan Akademik', 'url_override': '/akademik/panduan/', 'order': 5, 'icon_class': 'fas fa-book-bookmark', 'target': '_self'},
                    {'title': 'Panduan Maba (CMS)', 'page': sample_page, 'url_override': '', 'order': 6, 'icon_class': 'fas fa-file-circle-check', 'target': '_self'},
                ]
            },
            {
                'title': 'Staf',
                'url_override': '#',
                'order': 7,
                'icon_class': 'fas fa-users',
                'target': '_self',
                'children': [
                    {'title': 'Tenaga Pengajar', 'url_override': '/dosen/', 'order': 1, 'icon_class': 'fas fa-chalkboard-teacher', 'target': '_self'},
                    {'title': 'Tenaga Kependidikan', 'url_override': '/kependidikan/', 'order': 2, 'icon_class': 'fas fa-user-gear', 'target': '_self'},
                ]
            },
            {
                'title': 'Kemahasiswaan & Alumni',
                'url_override': '#',
                'order': 8,
                'icon_class': 'fas fa-user-graduate',
                'target': '_self',
                'children': [
                    {'title': 'Portal Kemahasiswaan UNTAD', 'url_override': 'https://kemahasiswaan.untad.ac.id', 'order': 1, 'icon_class': 'fas fa-external-link-alt', 'target': '_blank'},
                    {'title': 'Ikatan Alumni (IKA) UNTAD', 'url_override': 'https://alumni.untad.ac.id', 'order': 2, 'icon_class': 'fas fa-user-tie', 'target': '_blank'},
                ]
            },
        ]

        # Simpan ke Database
        created_count = 0
        for item in menus_data:
            parent_menu, created = Menu.objects.update_or_create(
                title=item['title'],
                parent=None,
                defaults={
                    'url_override': item['url_override'],
                    'order': item['order'],
                    'icon_class': item['icon_class'],
                    'target': item['target'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1

            for child_data in item.get('children', []):
                child_menu, c_created = Menu.objects.update_or_create(
                    title=child_data['title'],
                    parent=parent_menu,
                    defaults={
                        'url_override': child_data.get('url_override', ''),
                        'page': child_data.get('page', None),
                        'order': child_data['order'],
                        'icon_class': child_data['icon_class'],
                        'target': child_data['target'],
                        'is_active': True,
                    }
                )
                if c_created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Berhasil memuat struktur menu CMS! Total menu siap: {Menu.objects.count()} (Menu baru dibuat: {created_count})"))
