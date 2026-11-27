from django.core.management.base import BaseCommand
from cms.models import SiteSetting, SocialMedia, QuickLink, Menu, Page


class Command(BaseCommand):
    help = "Mengisi data awal CMS, Site Settings, Quick Links, dan Menu Navigasi"

    def handle(self, *args, **options):
        self.stdout.write("Memulai inisialisasi data awal CMS...")

        # 1. Inisialisasi SiteSetting
        setting = SiteSetting.get_solo()
        setting.header_title = "Administrasi Publik"
        setting.header_subtitle = "FISIP Universitas Tadulako"
        setting.footer_title = "Administrasi Publik"
        setting.footer_subtitle = "FISIP Universitas Tadulako"
        setting.footer_description = (
            "Program Studi Administrasi Publik Fakultas Ilmu Sosial dan Ilmu Politik "
            "Universitas Tadulako berorientasi pada integritas akademik, kualitas pendidikan, "
            "dan relevansi keprofesian dalam tata kelola publik."
        )
        setting.footer_short_address = "Kampus Bumi Tadulako, Tondo, Palu, Sulawesi Tengah"
        setting.contact_title = "Hubungi Kami"
        setting.contact_subtitle = "Hubungi sekretariat Program Studi atau kunjungi kantor kami langsung."
        setting.contact_address = "Jl. Soekarno Hatta No.KM.9, Tondo, Kec. Mantikulore, Kota Palu, Sulawesi Tengah 94148"
        setting.contact_phone = "085330144401"
        setting.contact_whatsapp = "6285330144401"
        setting.contact_email = "Admpublik.FISIP@untad.ac.id"
        setting.save()
        self.stdout.write(self.style.SUCCESS("✓ SiteSetting berhasil diperbarui."))

        # 2. Inisialisasi Sosial Media
        social_data = [
            ('instagram', 'https://instagram.com/admpublik_untad', 1),
            ('facebook', 'https://facebook.com/admpublik_untad', 2),
            ('youtube', 'https://youtube.com/@admpublik_untad', 3),
        ]
        for platform, url, order in social_data:
            SocialMedia.objects.get_or_create(
                setting=setting,
                platform=platform,
                defaults={'url': url, 'order': order, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS("✓ Akun Sosial Media awal berhasil dibuat."))

        # 3. Inisialisasi Tautan Cepat Footer
        quick_links_data = [
            ('Website FISIP', '#', False, 1),
            ('Website UNTAD', 'https://untad.ac.id', True, 2),
            ('Website Kepegawaian', '#', False, 3),
            ('SIGA-8', 'https://siga-8.untad.ac.id', True, 4),
            ('Dosen Prodi Administrasi Publik', '/tenaga-pengajar/', False, 5),
            ('Sertifikat Akreditasi', '/tentang/sertifikat/', False, 6),
        ]
        for title, url, open_new, order in quick_links_data:
            QuickLink.objects.get_or_create(
                setting=setting,
                title=title,
                defaults={'url': url, 'open_in_new_tab': open_new, 'order': order, 'is_active': True}
            )
        self.stdout.write(self.style.SUCCESS("✓ Tautan Cepat Footer berhasil dibuat."))

        # 4. Inisialisasi Menu Navigasi Awal (Navbar)
        # Root Menus
        menu_beranda, _ = Menu.objects.get_or_create(
            title="Beranda",
            defaults={'custom_url': '/#beranda', 'order': 1, 'is_active': True}
        )

        menu_tentang, _ = Menu.objects.get_or_create(
            title="Tentang",
            defaults={'custom_url': '/#sambutan', 'order': 2, 'is_active': True}
        )

        sub_tentang = [
            ('Profil Program Studi', '/tentang/profil/', 1),
            ('Sejarah & Dasar Hukum', '/tentang/sejarah/', 2),
            ('Visi, Misi & Tujuan', '/tentang/visi/', 3),
            ('Profil Lulusan', '/tentang/profil-lulusan/', 4),
            ('Sertifikat Akreditasi', '/tentang/sertifikat/', 5),
        ]
        for title, url, order in sub_tentang:
            Menu.objects.get_or_create(
                title=title,
                parent=menu_tentang,
                defaults={'custom_url': url, 'order': order, 'is_active': True}
            )

        menu_akademik, _ = Menu.objects.get_or_create(
            title="Akademik",
            defaults={'custom_url': '/akademik/', 'order': 3, 'is_active': True}
        )

        sub_akademik = [
            ('SIGA-8', 'https://siga-8.untad.ac.id', '_blank', 1),
            ('Kurikulum', '/akademik/kurikulum/', '_self', 2),
            ('Jadwal Perkuliahan', '/akademik/jadwal-perkuliahan/', '_self', 3),
            ('RPS', '/akademik/rps/', '_self', 4),
            ('Panduan Akademik', '/akademik/panduan-akademik/', '_self', 5),
        ]
        for title, url, target, order in sub_akademik:
            Menu.objects.get_or_create(
                title=title,
                parent=menu_akademik,
                defaults={'custom_url': url, 'target': target, 'order': order, 'is_active': True}
            )

        menu_staf, _ = Menu.objects.get_or_create(
            title="Staf",
            defaults={'custom_url': '#', 'order': 4, 'is_active': True}
        )

        sub_staf = [
            ('Tenaga Pengajar', '/tenaga-pengajar/', 1),
            ('Tenaga Kependidikan', '/tenaga-pendidik/', 2),
        ]
        for title, url, order in sub_staf:
            Menu.objects.get_or_create(
                title=title,
                parent=menu_staf,
                defaults={'custom_url': url, 'order': order, 'is_active': True}
            )

        menu_berita, _ = Menu.objects.get_or_create(
            title="Berita",
            defaults={'custom_url': '/berita/', 'order': 5, 'is_active': True}
        )

        menu_galeri, _ = Menu.objects.get_or_create(
            title="Galeri Kegiatan",
            defaults={'custom_url': '/galeri-kegiatan/', 'order': 6, 'is_active': True}
        )

        # Contoh 1 Halaman CMS Published untuk demonstrasi
        sample_page, _ = Page.objects.get_or_create(
            slug='pedoman-akademik-mahasiswa',
            defaults={
                'title': 'Pedoman Akademik Mahasiswa',
                'content_type': 'html',
                'status': 'published',
                'meta_description': 'Panduan resmi pedoman akademik bagi seluruh mahasiswa Program Studi Administrasi Publik.',
                'html_content': (
                    '<h3>Pedoman Umum Akademik</h3>'
                    '<p>Buku pedoman ini memuat ketentuan umum mengenai proses registrasi, penyusunan KRS, '
                    'standar kehadiran perkuliahan, tata cara ujian, serta prosedur pengajuan seminar dan skripsi.</p>'
                    '<ul>'
                    '<li>Registrasi dan pengisian KRS melalui portal resmi.</li>'
                    '<li>Batas minimal kehadiran kuliah tatap muka 75%.</li>'
                    '<li>Ketentuan kelulusan dan predikat yudisium.</li>'
                    '</ul>'
                )
            }
        )

        self.stdout.write(self.style.SUCCESS("✓ Struktur Menu Navigasi awal dan Halaman CMS berhasil diinisialisasi."))
        self.stdout.write(self.style.SUCCESS("Selesai!"))
