from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import reverse
from .models import Page, Menu
from .forms import PageAdminForm, MenuAdminForm


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ('title', 'slug', 'content_type_badge', 'status_badge', 'preview_action', 'updated_at')
    list_filter = ('status', 'content_type', 'created_at')
    search_fields = ('title', 'slug', 'meta_description', 'html_content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_published', 'make_draft']

    fieldsets = (
        ("Informasi Umum & Identitas Halaman", {
            'fields': ('title', 'slug', 'status', 'content_type', 'meta_description', 'banner_image')
        }),
        ("Konten HTML (CKEditor 5)", {
            'fields': ('html_content',),
        }),
        ("Dokumen PDF (PDF Preview)", {
            'fields': ('pdf_file',),
        }),
        ("Berkas Unduhan (File Download)", {
            'fields': ('file_download',),
        }),
        ("Tautan Redirect (External / Internal Link)", {
            'fields': ('external_url', 'internal_url'),
        }),
    )

    class Media:
        js = ('cms/js/admin_page_form.js',)
        css = {
            'all': ('cms/css/admin_cms.css',)
        }

    @admin.display(description="Jenis Konten")
    def content_type_badge(self, obj):
        return mark_safe(f'<span class="cms-badge cms-badge-type">{obj.get_content_type_display()}</span>')

    @admin.display(description="Status Publikasi")
    def status_badge(self, obj):
        if obj.status == 'published':
            return mark_safe('<span class="cms-badge cms-badge-published">● Published</span>')
        return mark_safe('<span class="cms-badge cms-badge-draft">○ Draft</span>')

    @admin.display(description="Pratinjau")
    def preview_action(self, obj):
        preview_url = reverse('cms_page_detail', kwargs={'slug': obj.slug}) + '?preview=1'
        return mark_safe(f'<a href="{preview_url}" target="_blank" class="cms-preview-btn">👁️ Preview</a>')

    @admin.action(description="Ubah status menjadi Published (Terbitkan)")
    def make_published(self, request, queryset):
        count = queryset.update(status='published')
        self.message_user(request, f"{count} halaman berhasil diterbitkan (Published).")

    @admin.action(description="Ubah status menjadi Draft (Simpan Konsep)")
    def make_draft(self, request, queryset):
        count = queryset.update(status='draft')
        self.message_user(request, f"{count} halaman diubah menjadi Draft.")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    form = MenuAdminForm
    list_display = ('order', 'drag_handle', 'title_hierarchy', 'parent', 'page_target_display', 'target', 'is_active')
    list_display_links = ('title_hierarchy',)
    list_editable = ('order', 'is_active', 'target')
    list_filter = ('is_active', 'target', 'parent')
    search_fields = ('title', 'url_override', 'page__title')
    actions = ['activate_menus', 'deactivate_menus']

    fieldsets = (
        ("Pengaturan Menu", {
            'fields': ('title', 'parent', 'order', 'is_active', 'icon_class')
        }),
        ("Target Konten & Tautan", {
            'fields': ('page', 'url_override', 'target'),
            'description': 'Pilih halaman CMS terkait ATAU masukkan Custom URL jika ingin mengarahkan menu ke tautan khusus.'
        }),
    )

    class Media:
        js = ('cms/js/admin_menu_sortable.js',)
        css = {
            'all': ('cms/css/admin_cms.css',)
        }

    @admin.display(description="")
    def drag_handle(self, obj):
        return mark_safe('<span class="cms-drag-handle" title="Drag & drop baris ini untuk mengubah urutan">☰</span>')

    @admin.display(description="Nama Menu Navigasi")
    def title_hierarchy(self, obj):
        icon = f'<i class="{obj.icon_class}" style="margin-right:6px; color:#0d9488;"></i>' if obj.icon_class else ''
        if obj.parent:
            if obj.parent.parent:
                return mark_safe(f'<span style="padding-left:36px; color:#64748b;">└─── {icon}<strong>{obj.title}</strong></span>')
            return mark_safe(f'<span style="padding-left:18px; color:#475569;">└── {icon}<strong>{obj.title}</strong></span>')
        return mark_safe(f'<span>{icon}<strong>{obj.title}</strong></span>')

    @admin.display(description="Tujuan Halaman / Link")
    def page_target_display(self, obj):
        if obj.url_override:
            return mark_safe(f'<code style="font-size:11px;">{obj.url_override}</code> (Custom)')
        if obj.page:
            type_label = obj.page.get_content_type_display()
            return mark_safe(f'<span>{obj.page.title}</span> <span class="cms-badge cms-badge-type">{type_label}</span>')
        return mark_safe('<em style="color:#94a3b8;"># (Dropdown Parent)</em>')

    @admin.action(description="Aktifkan menu terpilih")
    def activate_menus(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} menu berhasil diaktifkan.")

    @admin.action(description="Nonaktifkan menu terpilih")
    def deactivate_menus(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} menu dinonaktifkan.")
