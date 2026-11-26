from django import forms
from .models import Page, Menu


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'meta_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Deskripsi singkat atau subjudul halaman...'}),
            'external_url': forms.URLInput(attrs={'placeholder': 'https://siga-8.untad.ac.id'}),
            'internal_url': forms.TextInput(attrs={'placeholder': '/berita/ atau /event/'}),
            'slug': forms.TextInput(attrs={'placeholder': 'contoh: profil-prodi'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').strip().lower()
        reserved_slugs = ['admin', 'dashboard', 'login', 'logout', 'register', 'api', 'media', 'static', 'page']
        if slug in reserved_slugs:
            raise forms.ValidationError(f"Slug '{slug}' adalah rute sistem reserved dan tidak dapat digunakan.")
        return slug


class MenuAdminForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'icon_class': forms.TextInput(attrs={'placeholder': 'fas fa-book, fas fa-university'}),
            'url_override': forms.TextInput(attrs={'placeholder': 'https://... atau /custom-url/'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Cegah memilih diri sendiri atau anak langsung sebagai parent di dropdown form
            descendants = self._get_descendants(self.instance)
            exclude_ids = [self.instance.pk] + [d.pk for d in descendants]
            self.fields['parent'].queryset = Menu.objects.exclude(pk__in=exclude_ids)

    def _get_descendants(self, menu):
        descendants = []
        for child in menu.children.all():
            descendants.append(child)
            descendants.extend(self._get_descendants(child))
        return descendants
