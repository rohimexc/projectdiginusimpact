import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from cms.models import Page, Menu
from cms.context_processors import cms_navigation

User = get_user_model()


class CMSModelTests(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username='admin_staff',
            password='Password123!',
            is_staff=True
        )

    def test_page_validations(self):
        # 1. Reserved slug check
        page_reserved = Page(title='Test Admin', slug='admin', content_type='html')
        with self.assertRaises(ValidationError):
            page_reserved.full_clean()

        # 2. HTML Published without content should raise error
        page_html = Page(title='Test HTML', slug='test-html', content_type='html', status='published', html_content='')
        with self.assertRaises(ValidationError):
            page_html.full_clean()

        # 3. PDF without file should raise error
        page_pdf = Page(title='Test PDF', slug='test-pdf', content_type='pdf')
        with self.assertRaises(ValidationError):
            page_pdf.full_clean()

        # 4. PDF with wrong extension
        fake_txt = SimpleUploadedFile("dokumen.txt", b"isi dokumen", content_type="text/plain")
        page_wrong_pdf = Page(title='Test PDF', slug='test-pdf', content_type='pdf', pdf_file=fake_txt)
        with self.assertRaises(ValidationError):
            page_wrong_pdf.full_clean()

        # 5. External link without http/https
        page_ext = Page(title='Test Ext', slug='test-ext', content_type='external_link', external_url='ftp://siga.com')
        with self.assertRaises(ValidationError):
            page_ext.full_clean()

        # 6. Internal link without starting slash
        page_int = Page(title='Test Int', slug='test-int', content_type='internal_link', internal_url='berita/')
        with self.assertRaises(ValidationError):
            page_int.full_clean()

    def test_menu_circular_parent_prevention(self):
        menu_a = Menu.objects.create(title='Menu A', order=1)
        menu_b = Menu.objects.create(title='Menu B', parent=menu_a, order=2)
        menu_c = Menu.objects.create(title='Menu C', parent=menu_b, order=3)

        # 1. Self parent prevention
        menu_a.parent = menu_a
        with self.assertRaises(ValidationError):
            menu_a.clean()

        # 2. Circular reference: A -> B -> C -> A
        menu_a.parent = menu_c
        with self.assertRaises(ValidationError):
            menu_a.clean()

    def test_menu_dynamic_url_resolution(self):
        page_html = Page.objects.create(
            title='Halaman Statis',
            slug='halaman-statis',
            content_type='html',
            status='published',
            html_content='<p>Konten</p>'
        )
        page_ext = Page.objects.create(
            title='Halaman Luar',
            slug='halaman-luar',
            content_type='external_link',
            external_url='https://siga-8.untad.ac.id'
        )
        page_int = Page.objects.create(
            title='Halaman Dalam',
            slug='halaman-dalam',
            content_type='internal_link',
            internal_url='/berita/'
        )

        menu_1 = Menu.objects.create(title='Menu 1', page=page_html)
        menu_2 = Menu.objects.create(title='Menu 2', page=page_ext)
        menu_3 = Menu.objects.create(title='Menu 3', page=page_int)
        menu_override = Menu.objects.create(title='Menu Override', url_override='https://untad.ac.id')

        self.assertEqual(menu_1.get_url(), reverse('cms_page_detail', kwargs={'slug': 'halaman-statis'}))
        self.assertEqual(menu_2.get_url(), 'https://siga-8.untad.ac.id')
        self.assertEqual(menu_2.get_target(), '_blank')
        self.assertEqual(menu_3.get_url(), '/berita/')
        self.assertEqual(menu_override.get_url(), 'https://untad.ac.id')


class CMSViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff_cms',
            password='StaffPassword123!',
            is_staff=True
        )
        self.published_page = Page.objects.create(
            title='Profil Mahasiswa',
            slug='profil-mahasiswa',
            content_type='html',
            status='published',
            html_content='<h2>Profil Mahasiswa FISIP</h2>'
        )
        self.draft_page = Page.objects.create(
            title='Draft Dokumen',
            slug='draft-dokumen',
            content_type='html',
            status='draft',
            html_content='<h2>Dokumen Masih Rahasia</h2>'
        )

    def test_published_page_accessible(self):
        url = reverse('cms_page_detail', kwargs={'slug': 'profil-mahasiswa'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profil Mahasiswa FISIP')

    def test_draft_page_public_404_and_staff_preview_200(self):
        url = reverse('cms_page_detail', kwargs={'slug': 'draft-dokumen'})
        
        # Public visitor gets 404
        response_anon = self.client.get(url)
        self.assertEqual(response_anon.status_code, 404)

        # Staff with ?preview=1 gets 200
        self.client.login(username='staff_cms', password='StaffPassword123!')
        response_staff = self.client.get(url + '?preview=1')
        self.assertEqual(response_staff.status_code, 200)
        self.assertContains(response_staff, 'Dokumen Masih Rahasia')
        self.assertContains(response_staff, 'Mode Pratinjau (Draft)')

    def test_external_and_internal_link_redirects(self):
        page_ext = Page.objects.create(
            title='Redirect Ext',
            slug='redirect-ext',
            content_type='external_link',
            external_url='https://siga-8.untad.ac.id'
        )
        page_int = Page.objects.create(
            title='Redirect Int',
            slug='redirect-int',
            content_type='internal_link',
            internal_url='/event/'
        )

        resp_ext = self.client.get(reverse('cms_page_detail', kwargs={'slug': 'redirect-ext'}))
        self.assertRedirects(resp_ext, 'https://siga-8.untad.ac.id', fetch_redirect_response=False)

        resp_int = self.client.get(reverse('cms_page_detail', kwargs={'slug': 'redirect-int'}))
        self.assertRedirects(resp_int, '/event/', fetch_redirect_response=False)

    def test_ajax_menu_reorder(self):
        m1 = Menu.objects.create(title='Menu 1', order=1)
        m2 = Menu.objects.create(title='Menu 2', order=2)

        self.client.login(username='staff_cms', password='StaffPassword123!')
        url = reverse('cms_reorder_menus')
        payload = {
            'items': [
                {'id': m1.id, 'order': 10},
                {'id': m2.id, 'order': 5},
            ]
        }
        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        m1.refresh_from_db()
        m2.refresh_from_db()
        self.assertEqual(m1.order, 10)
        self.assertEqual(m2.order, 5)
