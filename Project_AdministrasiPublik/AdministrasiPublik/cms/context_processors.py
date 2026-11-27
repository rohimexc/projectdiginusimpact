from .models import SiteSetting, Menu


def site_settings_context(request):
    """
    Context processor global untuk menyediakan identitas situs, footer, kontak,
    sosial media, dan tautan cepat ke seluruh template (base.html, dll).
    """
    try:
        settings_obj = SiteSetting.get_solo()
        quick_links = settings_obj.quick_links.filter(is_active=True).order_by('order', 'id')
        social_media = settings_obj.social_media_list.filter(
            is_active=True
        ).exclude(url__exact='').order_by('order', 'id')
        whatsapp_url = f"https://wa.me/{settings_obj.get_whatsapp_clean}"
    except Exception:
        settings_obj = None
        quick_links = []
        social_media = []
        whatsapp_url = "https://wa.me/6285330144401"

    return {
        'site_setting': settings_obj,
        'site_settings': settings_obj,  # alias pendukung
        'site_quick_links': quick_links,
        'site_social_media': social_media,
        'whatsapp_chat_url': whatsapp_url,
    }


def cms_menus_context(request):
    """
    Context processor global untuk menyediakan struktur menu navigasi dinamis (termasuk submenu bertingkat)
    secara otomatis ke navbar desktop, tablet, dan mobile.
    """
    try:
        user_is_staff = request.user.is_authenticated and request.user.is_staff
        
        # Ambil seluruh menu aktif dalam 1 query optimal
        all_menus = list(
            Menu.objects.filter(is_active=True)
            .select_related('page', 'parent')
            .order_by('order', 'id')
        )
        
        menu_dict = {}
        root_menus = []

        for m in all_menus:
            # Sembunyikan menu jika mengarah ke halaman berstatus Draft (kecuali admin/staff)
            if m.page and m.page.status == 'draft' and not user_is_staff:
                continue
            m.submenus = []
            menu_dict[m.id] = m

        for m in menu_dict.values():
            if m.parent_id and m.parent_id in menu_dict:
                menu_dict[m.parent_id].submenus.append(m)
            elif not m.parent_id:
                root_menus.append(m)
    except Exception:
        root_menus = []

    return {
        'cms_navbar_menus': root_menus,
        'has_cms_menus': len(root_menus) > 0,
    }
