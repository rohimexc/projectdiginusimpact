from .models import Menu


def cms_navigation(request):
    """
    Context processor untuk menyediakan struktur menu navbar dinamis dari CMS ke seluruh template.
    Mendukung menu hirarki bertingkat (parent, child, nested child).
    Menu nonaktif atau halaman berstatus Draft otomatis disembunyikan untuk pengunjung umum.
    """
    is_staff = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

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

        visible_menus = []
        for menu in root_menus:
            if not is_visible(menu):
                continue

            active_children = []
            for child in menu.children.filter(is_active=True).order_by('order', 'id'):
                if not is_visible(child):
                    continue

                # Cek submenu bertingkat (level 3)
                nested_children = []
                for sub in child.children.filter(is_active=True).order_by('order', 'id'):
                    if is_visible(sub):
                        nested_children.append(sub)

                child.nested_children_list = nested_children
                active_children.append(child)

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
