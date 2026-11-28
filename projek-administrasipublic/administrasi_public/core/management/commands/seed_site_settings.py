from django.core.management.base import BaseCommand
from core.models import SiteSetting, SocialMedia, QuickLink


class Command(BaseCommand):
    help = 'Mengisi konfigurasi bawaan SiteSetting, SocialMedia, dan QuickLink'

    def handle(self, *args, **options):
        self.stdout.write("Memeriksa konfigurasi SiteSetting...")
        setting = SiteSetting.get_settings()
        self.stdout.write(self.style.SUCCESS(f"SiteSetting siap: {setting.header_title} (ID {setting.pk})"))

        # Default Quick Links (sesuai footer bawaan)
        default_quick_links = [
            {'title': 'Portal SIGA-8 UNTAD', 'url': 'https://siga-8.untad.ac.id', 'open_in_new_tab': True, 'order': 1},
            {'title': 'Website Resmi UNTAD', 'url': 'https://untad.ac.id', 'open_in_new_tab': True, 'order': 2},
            {'title': 'Website Resmi FISIP', 'url': 'https://fisip.untad.ac.id', 'open_in_new_tab': True, 'order': 3},
            {'title': 'Kurikulum & RPS', 'url': '/akademik/kurikulum/', 'open_in_new_tab': False, 'order': 4},
            {'title': 'Jadwal Perkuliahan', 'url': '/akademik/jadwal/', 'open_in_new_tab': False, 'order': 5},
            {'title': 'Panduan Skripsi & Magang', 'url': '/akademik/panduan/', 'open_in_new_tab': False, 'order': 6},
        ]

        for item in default_quick_links:
            ql, created = QuickLink.objects.get_or_create(
                site_setting=setting,
                title=item['title'],
                defaults={
                    'url': item['url'],
                    'open_in_new_tab': item['open_in_new_tab'],
                    'order': item['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f"  + Ditambahkan QuickLink: {item['title']}")

        # Default Social Media
        default_socials = [
            {'platform': 'instagram', 'url': 'https://instagram.com/admpublik_untad', 'order': 1},
            {'platform': 'facebook', 'url': 'https://facebook.com/admpublikuntad', 'order': 2},
            {'platform': 'youtube', 'url': 'https://youtube.com/@admpublikuntad', 'order': 3},
            {'platform': 'linkedin', 'url': 'https://linkedin.com/school/universitas-tadulako', 'order': 4},
        ]

        for item in default_socials:
            sm, created = SocialMedia.objects.get_or_create(
                site_setting=setting,
                platform=item['platform'],
                defaults={
                    'url': item['url'],
                    'order': item['order'],
                    'is_active': True,
                }
            )
            if created:
                self.stdout.write(f"  + Ditambahkan SocialMedia: {item['platform']}")

        self.stdout.write(self.style.SUCCESS("Berhasil menyelesaikan seeding Site Settings!"))
