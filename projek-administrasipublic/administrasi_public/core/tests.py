import io
from PIL import Image
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from .models import SiteSetting, SocialMedia, QuickLink
from .validators import validate_favicon_file, validate_site_logo_file
from .context_processors import site_settings_processor

User = get_user_model()


class SiteSettingModelTest(TestCase):
    def setUp(self):
        self.setting = SiteSetting.get_settings()

    def test_singleton_pattern(self):
        """Memastikan hanya ada 1 record konfigurasi dengan pk=1"""
        self.assertEqual(self.setting.pk, 1)

        # Mencoba membuat instance baru dengan pk berbeda
        new_setting = SiteSetting(header_title="Test Titik Dua")
        new_setting.save()
        self.assertEqual(new_setting.pk, 1)
        self.assertEqual(SiteSetting.objects.count(), 1)

        # Delete tidak boleh menghapus instance
        new_setting.delete()
        self.assertEqual(SiteSetting.objects.count(), 1)

    def test_clean_whatsapp_property(self):
        """Memastikan konversi nomor WhatsApp ke format wa.me (628xxx) bekerja akurat"""
        self.setting.contact_whatsapp = "085330144401"
        self.assertEqual(self.setting.clean_whatsapp, "6285330144401")

        self.setting.contact_whatsapp = "+62 811-450-000"
        self.assertEqual(self.setting.clean_whatsapp, "62811450000")

        self.setting.contact_whatsapp = "85211223344"
        self.assertEqual(self.setting.clean_whatsapp, "6285211223344")

        self.setting.contact_whatsapp = ""
        self.assertEqual(self.setting.clean_whatsapp, "6285330144401")

    def test_social_media_mapping(self):
        """Memastikan mapping ikon bawaan untuk platform sosial media bekerja benar"""
        fb = SocialMedia.objects.create(
            site_setting=self.setting,
            platform='facebook',
            url='https://facebook.com/untad',
            order=1,
            is_active=True
        )
        self.assertEqual(fb.get_icon_class(), 'bi bi-facebook')
        self.assertEqual(fb.get_fa_icon_class(), 'fab fa-facebook-f')

        ig = SocialMedia.objects.create(
            site_setting=self.setting,
            platform='instagram',
            url='https://instagram.com/untad',
            order=2,
            is_active=True
        )
        self.assertEqual(ig.get_icon_class(), 'bi bi-instagram')

    def test_quick_link_urls(self):
        """Memastikan get_url() mengembalikan URL tautan web atau berkas unduhan"""
        ql_web = QuickLink.objects.create(
            site_setting=self.setting,
            title='SIGA-8',
            url='https://siga-8.untad.ac.id',
            open_in_new_tab=True
        )
        self.assertEqual(ql_web.get_url(), 'https://siga-8.untad.ac.id')
        self.assertFalse(ql_web.is_file)


class SiteSettingContextProcessorTest(TestCase):
    def setUp(self):
        self.setting = SiteSetting.get_settings()
        self.client = Client()

        # Tambahkan akun sosial media aktif dan tidak aktif
        SocialMedia.objects.create(
            site_setting=self.setting,
            platform='instagram',
            url='https://instagram.com/active',
            is_active=True
        )
        SocialMedia.objects.create(
            site_setting=self.setting,
            platform='youtube',
            url='https://youtube.com/inactive',
            is_active=False
        )
        SocialMedia.objects.create(
            site_setting=self.setting,
            platform='tiktok',
            url='',  # URL kosong
            is_active=True
        )

        QuickLink.objects.create(
            site_setting=self.setting,
            title='Link Aktif',
            url='/akademik/',
            is_active=True
        )
        QuickLink.objects.create(
            site_setting=self.setting,
            title='Link Nonaktif',
            url='/secret/',
            is_active=False
        )

    def test_context_processor_output(self):
        """Memastikan context processor hanya memuat item aktif dan terisi URL-nya"""
        class MockRequest:
            pass

        data = site_settings_processor(MockRequest())
        self.assertIn('site_settings', data)
        self.assertIn('social_medias', data)
        self.assertIn('quick_links', data)

        social_urls = [s.url for s in data['social_medias']]
        self.assertIn('https://instagram.com/active', social_urls)
        self.assertNotIn('https://youtube.com/inactive', social_urls)
        self.assertNotIn('', social_urls)

        quick_titles = [q.title for q in data['quick_links']]
        self.assertIn('Link Aktif', quick_titles)
        self.assertNotIn('Link Nonaktif', quick_titles)


class SiteSettingValidatorTest(TestCase):
    def test_favicon_validator(self):
        """Memastikan validasi ukuran file dan ekstensi favicon"""
        # Ekstensi salah
        bad_file = SimpleUploadedFile("test.exe", b"fake binary data", content_type="application/octet-stream")
        with self.assertRaises(ValidationError):
            validate_favicon_file(bad_file)

        # Ukuran melebihi 500 KB
        large_content = b"x" * (600 * 1024)
        large_file = SimpleUploadedFile("large.png", large_content, content_type="image/png")
        with self.assertRaises(ValidationError):
            validate_favicon_file(large_file)

    def test_logo_validator(self):
        """Memastikan validasi ukuran logo maksimal 2 MB"""
        large_content = b"x" * (3 * 1024 * 1024)
        large_file = SimpleUploadedFile("large_logo.png", large_content, content_type="image/png")
        with self.assertRaises(ValidationError):
            validate_site_logo_file(large_file)


class SiteSettingAdminViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin_site',
            email='admin@untad.ac.id',
            password='password123'
        )
        self.regular_user = User.objects.create_user(
            username='regular_user',
            password='password123'
        )

    def test_access_denied_for_regular_user(self):
        """User non-admin dialihkan ke login dan tidak bisa mengakses dashboard pengaturan"""
        self.client.login(username='regular_user', password='password123')
        response = self.client.get(reverse('admin_kelola_pengaturan'))
        self.assertEqual(response.status_code, 302)

    def test_access_granted_for_admin(self):
        """Admin berhasil membuka dashboard pengaturan website"""
        self.client.login(username='admin_site', password='password123')
        response = self.client.get(reverse('admin_kelola_pengaturan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pengaturan Website (Site Settings)')
        self.assertContains(response, 'Identitas & Header')
        self.assertContains(response, 'Pengaturan Footer')

    def test_post_update_settings(self):
        """Admin berhasil mengirimkan pembaruan konfigurasi via POST"""
        self.client.login(username='admin_site', password='password123')
        post_data = {
            'header_title': 'Administrasi Publik Unggul',
            'header_subtitle': 'FISIP Universitas Tadulako 2026',
            'footer_title': 'Administrasi Publik Footer',
            'footer_subtitle': 'FISIP UNTAD',
            'footer_description': 'Deskripsi baru yang diperbarui.',
            'footer_short_address': 'Palu, Sulawesi Tengah',
            'contact_title': 'Hubungi Kami',
            'contact_subtitle': 'Sekretariat Prodi',
            'contact_address': 'Kampus Tondo Palu',
            'contact_phone': '0451-999999',
            'contact_whatsapp': '081234567890',
            'contact_email': 'info@untad.ac.id',
            # Management forms untuk formsets
            'social-TOTAL_FORMS': '0',
            'social-INITIAL_FORMS': '0',
            'social-MIN_NUM_FORMS': '0',
            'social-MAX_NUM_FORMS': '1000',
            'quick-TOTAL_FORMS': '0',
            'quick-INITIAL_FORMS': '0',
            'quick-MIN_NUM_FORMS': '0',
            'quick-MAX_NUM_FORMS': '1000',
            'active_tab': 'identitas',
        }
        response = self.client.post(reverse('admin_kelola_pengaturan'), post_data)
        self.assertEqual(response.status_code, 302)

        setting = SiteSetting.get_settings()
        self.assertEqual(setting.header_title, 'Administrasi Publik Unggul')
        self.assertEqual(setting.clean_whatsapp, '6281234567890')


class BeritaUrlRoutingTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_berita_url_lowercase_and_uppercase(self):
        """Memastikan baik /berita/ (lowercase) maupun /Berita/ (uppercase) dapat diakses dan tidak 404"""
        res_lower = self.client.get('/berita/')
        self.assertEqual(res_lower.status_code, 200)

        res_upper = self.client.get('/Berita/')
        self.assertEqual(res_upper.status_code, 200)

    def test_berita_slider_carousel_rendered(self):
        """Memastikan fitur slider/carousel sorotan berita dirender dengan benar seperti galeri"""
        response = self.client.get('/berita/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sorotan_berita', response.context)
        self.assertIn('berita-sorotan-swiper', response.content.decode('utf-8'))
        self.assertIn('sorotan-berita-prev', response.content.decode('utf-8'))
        self.assertIn('sorotan-berita-next', response.content.decode('utf-8'))

