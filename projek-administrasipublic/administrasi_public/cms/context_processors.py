from .models import Menu


def cms_navigation(request):
    """
    Context processor untuk menyediakan struktur menu navbar dinamis dari CMS ke seluruh template.
    Mendukung menu hirarki bertingkat (parent, child, nested child).
    Menu nonaktif atau halaman berstatus Draft otomatis disembunyikan untuk pengunjung umum.
    Menghitung status `is_active_link` untuk menandai halaman yang sedang aktif di navbar.
    """
    user = getattr(request, 'user', None)
    is_staff = bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

    try:
        root_menus = Menu.objects.filter(is_active=True, parent__isnull=True).prefetch_related(
            'children',
            'children__children',
            'page',
            'children__page',
            'children__children__page'
        ).order_by('order', 'id')

        def is_visible(item):
            # Jika item terhubung ke Halaman CMS dan statusnya Draft, hanya staf yang dapat melihatnya
            if item.page and item.page.status == 'draft' and not is_staff:
                return False
            return True

        current_path = getattr(request, 'path', '')

        def is_url_active(url):
            if not url:
                return False
            u = url.strip().rstrip('/')
            c = current_path.strip().rstrip('/')
            if not u or u == '/':
                return c == '' or c == '/'
            if u.startswith('http://') or u.startswith('https://'):
                return False
            u_lower = u.lower()
            c_lower = c.lower()
            if c_lower == u_lower:
                return True
            if c_lower.startswith(u_lower + '/'):
                return True
            return False

        visible_menus = []
        for menu in root_menus:
            if not is_visible(menu):
                continue

            menu_is_active = is_url_active(menu.get_url())

            active_children = []
            for child in menu.children.filter(is_active=True).order_by('order', 'id'):
                if not is_visible(child):
                    continue

                child_is_active = is_url_active(child.get_url())

                # Cek submenu bertingkat (level 3)
                nested_children = []
                for sub in child.children.filter(is_active=True).order_by('order', 'id'):
                    if is_visible(sub):
                        sub_is_active = is_url_active(sub.get_url())
                        sub.is_active_link = sub_is_active
                        if sub_is_active:
                            child_is_active = True
                        nested_children.append(sub)

                child.is_active_link = child_is_active
                if child_is_active:
                    menu_is_active = True
                child.nested_children_list = nested_children
                active_children.append(child)

            menu.is_active_link = menu_is_active
            menu.children_list = active_children
            visible_menus.append(menu)

        return {
            'cms_menus': visible_menus
        }
    except Exception:
        # Menghindari error saat migrasi database awal jika tabel belum terbuat
        return {
            'cms_menus': []
        }
