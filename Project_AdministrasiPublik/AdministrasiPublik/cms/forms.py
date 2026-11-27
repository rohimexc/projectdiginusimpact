from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Page, Menu, SiteSetting, SocialMedia, QuickLink


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'content_type', 'status', 'meta_description',
            'html_content', 'file', 'external_url', 'internal_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'placeholder': 'Contoh: Kurikulum Program Studi'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm font-mono',
                'placeholder': 'kurikulum-program-studi'
            }),
            'content_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm font-semibold',
                'id': 'dashboardContentTypeSelect'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm font-semibold'
            }),
            'meta_description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'placeholder': 'Ringkasan singkat isi halaman...'
            }),
            'html_content': CKEditor5Widget(config_name='extends'),
            'file': forms.FileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100 cursor-pointer border border-slate-300 rounded-xl'
            }),
            'external_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'placeholder': 'https://siga-8.untad.ac.id'
            }),
            'internal_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'placeholder': '/berita/ atau /tenaga-pendidik/'
            }),
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['title', 'parent', 'page', 'custom_url', 'target', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'placeholder': 'Nama yang tampil di Navbar'
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm'
            }),
            'page': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm'
            }),
            'custom_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm font-mono',
                'placeholder': 'Opsional: misal /berita/ atau https://...'
            }),
            'target': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-600 focus:outline-none text-xs sm:text-sm',
                'min': '1'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jika sedang mengedit, jangan izinkan memilih dirinya sendiri sebagai parent
        if self.instance and self.instance.pk:
            self.fields['parent'].queryset = Menu.objects.exclude(pk=self.instance.pk)


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'header_title', 'header_subtitle', 'favicon', 'header_logo',
            'footer_title', 'footer_subtitle', 'footer_description', 'footer_short_address', 'footer_logo',
            'contact_title', 'contact_subtitle', 'contact_address', 'contact_phone', 'contact_whatsapp', 'contact_email',
            'maps_embed_url'
        ]
        widgets = {
            # Header
            'header_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'header_subtitle': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'favicon': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 border border-slate-300 rounded-xl p-2', 'id': 'settingFaviconInput'}),
            'header_logo': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 border border-slate-300 rounded-xl p-2', 'id': 'settingHeaderLogoInput'}),
            # Footer
            'footer_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'footer_subtitle': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'footer_description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'footer_short_address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'footer_logo': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 border border-slate-300 rounded-xl p-2', 'id': 'settingFooterLogoInput'}),
            # Kontak
            'contact_title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'contact_subtitle': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'contact_address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'contact_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm font-mono', 'placeholder': '628xxxxxxxx'}),
            'contact_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm'}),
            'maps_embed_url': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 text-xs sm:text-sm font-mono'}),
        }


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'url', 'order', 'is_active']
        widgets = {
            'platform': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs'}),
            'url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs', 'placeholder': 'https://...'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs', 'min': '1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-teal-600 rounded border-slate-300'}),
        }


class QuickLinkForm(forms.ModelForm):
    class Meta:
        model = QuickLink
        fields = ['title', 'url', 'file', 'open_in_new_tab', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs', 'placeholder': 'Judul Tautan'}),
            'url': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs', 'placeholder': 'URL (opsional jika file diisi)'}),
            'file': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 border border-slate-300 rounded-xl p-1.5'}),
            'open_in_new_tab': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-teal-600 rounded border-slate-300'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-300 text-xs', 'min': '1'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-teal-600 rounded border-slate-300'}),
        }
