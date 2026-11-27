from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Page, Menu, SiteSetting, SocialMedia, QuickLink


# ==========================================
# 1. PAGE ADMIN
# ==========================================

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'content_type_badge', 'status_badge', 'updated_at', 'action_buttons')
    list_filter = ('content_type', 'status', 'created_at')
    search_fields = ('title', 'slug', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20

    fieldsets = (
        ("Informasi Utama", {
            'fields': ('title', 'slug', 'content_type', 'status', 'meta_description')
        }),
        ("Konten Halaman (Sesuaikan dengan Jenis Konten)", {
            'fields': ('html_content', 'file', 'external_url', 'internal_url'),
            'description': "Field di bawah ini akan aktif dan relevan sesuai Jenis Konten yang dipilih di atas."
        }),
    )

    def content_type_badge(self, obj):
        colors = {
            'html': '#0f766e',
            'pdf': '#b45309',
            'external_link': '#1d4ed8',
            'internal_link': '#6d28d9',
            'dropdown': '#475569',
            'file_download': '#047857',
        }
        color = colors.get(obj.content_type, '#475569')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;">{}</span>',
            color,
            obj.get_content_type_display()
        )
    content_type_badge.short_description = "Jenis Konten"

    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html('<span style="color: #047857; font-weight: bold; background: #ecfdf5; padding: 2px 8px; border-radius: 4px;">Published</span>')
        return format_html('<span style="color: #b45309; font-weight: bold; background: #fffbeb; padding: 2px 8px; border-radius: 4px;">Draft</span>')
    status_badge.short_description = "Status"

    def action_buttons(self, obj):
        if obj.status == 'published':
            url = reverse('cms:page_detail', kwargs={'slug': obj.slug})
            label = "Lihat Live ↗"
            bg = "#0f6b6b"
        else:
            url = reverse('cms:page_detail', kwargs={'slug': obj.slug}) + '?preview=1'
            label = "Preview Draft ↗"
            bg = "#d97706"
        return format_html(
            '<a href="{}" target="_blank" style="display: inline-block; padding: 3px 8px; background: {}; color: white; border-radius: 4px; text-decoration: none; font-size: 11px; font-weight: bold;">{}</a>',
            url, bg, label
        )
    action_buttons.short_description = "Aksi"

    class Media:
        js = ('cms/js/admin_page_toggle.js',)


# ==========================================
# 2. MENU ADMIN
# ==========================================

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_hierarchy', 'parent', 'page_or_url', 'target', 'is_active')
    list_display_links = ('menu_hierarchy',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('title', 'page__title', 'custom_url')
    list_per_page = 30
    ordering = ('order', 'id')

    fieldsets = (
        ("Informasi Menu", {
            'fields': ('title', 'parent', 'order', 'is_active')
        }),
        ("Tujuan Navigasi", {
            'fields': ('page', 'custom_url', 'target'),
            'description': "Pilih Halaman CMS ATAU isi URL Kustom jika menu berupa link luar / anchor section."
        }),
    )

    def menu_hierarchy(self, obj):
        indent = "&mdash;&mdash; " if obj.parent else ""
        if obj.parent and obj.parent.parent:
            indent = "&mdash;&mdash;&mdash;&mdash; "
        return format_html('<span style="font-weight: {}; color: {};">{}{}</span>', 
                           'bold' if not obj.parent else 'normal',
                           '#0f6b6b' if not obj.parent else '#334155',
                           format_html(indent), 
                           obj.title)
    menu_hierarchy.short_description = "Nama Menu Navigasi"

    def page_or_url(self, obj):
        if obj.page:
            return format_html('<b>Halaman:</b> {} <span style="color:#64748b;">(/p/{})</span>', obj.page.title, obj.page.slug)
        if obj.custom_url:
            return format_html('<b>URL:</b> <code>{}</code>', obj.custom_url)
        return format_html('<span style="color:#94a3b8;">(Dropdown Only)</span>')
    page_or_url.short_description = "Tujuan Link"


# ==========================================
# 3. SITE SETTINGS ADMIN
# ==========================================

class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1
    fields = ('platform', 'url', 'order', 'is_active')
    ordering = ('order', 'id')


class QuickLinkInline(admin.TabularInline):
    model = QuickLink
    extra = 1
    fields = ('title', 'url', 'file', 'open_in_new_tab', 'order', 'is_active')
    ordering = ('order', 'id')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    inlines = [QuickLinkInline, SocialMediaInline]

    fieldsets = (
        ("Identitas Situs & Header", {
            'fields': (
                'header_title', 'header_subtitle',
                'favicon', 'preview_favicon',
                'header_logo', 'preview_header_logo'
            ),
            'description': "Atur judul nama web, subjudul fakultas, favicon, dan logo navbar header."
        }),
        ("Pengaturan Footer", {
            'fields': (
                'footer_title', 'footer_subtitle', 'footer_description', 'footer_short_address',
                'footer_logo', 'preview_footer_logo'
            ),
            'description': "Atur logo footer, identitas, deskripsi profil prodi, dan alamat ringkas."
        }),
        ("Informasi Kontak & Lokasi", {
            'fields': (
                'contact_title', 'contact_subtitle',
                'contact_address', 'contact_phone', 'contact_whatsapp', 'contact_email',
                'maps_embed_url'
            ),
            'description': "Informasi kontak sekretariat, link WhatsApp chat, dan peta lokasi."
        }),
    )

    readonly_fields = ('preview_favicon', 'preview_header_logo', 'preview_footer_logo')

    def preview_favicon(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="max-height: 48px; max-width: 48px; border: 1px solid #e2e8f0; padding: 4px; border-radius: 6px; background: #fff;" />', obj.favicon.url)
        return "Belum ada favicon diunggah."
    preview_favicon.short_description = "Preview Favicon Saat Ini"

    def preview_header_logo(self, obj):
        if obj.header_logo:
            return format_html('<img src="{}" style="max-height: 50px; background: #0f6b6b; padding: 6px; border-radius: 8px;" />', obj.header_logo.url)
        return "Belum ada logo header diunggah (menggunakan logo bawaan)."
    preview_header_logo.short_description = "Preview Logo Header Saat Ini"

    def preview_footer_logo(self, obj):
        if obj.footer_logo:
            return format_html('<img src="{}" style="max-height: 50px; background: #005f5f; padding: 6px; border-radius: 8px;" />', obj.footer_logo.url)
        return "Belum ada logo footer diunggah."
    preview_footer_logo.short_description = "Preview Logo Footer Saat Ini"

    def has_add_permission(self, request):
        # Mencegah duplikasi: Hanya satu instance SiteSetting yang diizinkan
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)

    class Media:
        js = ('cms/js/admin_live_preview.js',)


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('platform', 'is_active')
    search_fields = ('url',)


@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'file', 'open_in_new_tab', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'open_in_new_tab')
    search_fields = ('title', 'url')
