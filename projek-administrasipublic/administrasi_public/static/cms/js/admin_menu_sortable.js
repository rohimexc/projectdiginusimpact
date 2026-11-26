/* Drag and Drop Reordering for Django Admin Menu */
document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('#result_list');
    if (!table) return;

    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    const rows = tbody.querySelectorAll('tr');
    let draggedRow = null;

    // Toast notification function
    function showToast(message, isError = false) {
        let toast = document.getElementById('cms-order-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'cms-order-toast';
            toast.style.position = 'fixed';
            toast.style.bottom = '24px';
            toast.style.right = '24px';
            toast.style.padding = '12px 20px';
            toast.style.borderRadius = '8px';
            toast.style.color = '#fff';
            toast.style.fontWeight = 'bold';
            toast.style.fontSize = '13px';
            toast.style.zIndex = '9999';
            toast.style.boxShadow = '0 4px 14px rgba(0,0,0,0.2)';
            toast.style.transition = 'opacity 0.3s ease';
            document.body.appendChild(toast);
        }
        toast.style.backgroundColor = isError ? '#e11d48' : '#0d9488';
        toast.textContent = message;
        toast.style.opacity = '1';
        toast.style.display = 'block';
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => { toast.style.display = 'none'; }, 300);
        }, 3000);
    }

    // CSRF helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Make rows draggable
    rows.forEach(row => {
        row.setAttribute('draggable', 'true');
        row.style.cursor = 'grab';

        row.addEventListener('dragstart', function(e) {
            draggedRow = this;
            this.style.opacity = '0.5';
            this.style.backgroundColor = '#e0f2fe';
            e.dataTransfer.effectAllowed = 'move';
        });

        row.addEventListener('dragend', function() {
            this.style.opacity = '';
            this.style.backgroundColor = '';
            draggedRow = null;
            document.querySelectorAll('#result_list tbody tr').forEach(r => r.style.borderTop = '');
        });

        row.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            if (draggedRow && draggedRow !== this) {
                this.style.borderTop = '2px solid #0d9488';
            }
        });

        row.addEventListener('dragleave', function() {
            this.style.borderTop = '';
        });

        row.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderTop = '';
            if (draggedRow && draggedRow !== this) {
                tbody.insertBefore(draggedRow, this);
                saveNewOrder();
            }
        });
    });

    function saveNewOrder() {
        const currentRows = tbody.querySelectorAll('tr');
        const items = [];
        currentRows.forEach((r, idx) => {
            // Find ID from checkbox input or link
            const checkbox = r.querySelector('input.action-select');
            let id = null;
            if (checkbox) {
                id = checkbox.value;
            } else {
                const link = r.querySelector('th a');
                if (link) {
                    const match = link.href.match(/\/(\d+)\/change\//);
                    if (match) id = match[1];
                }
            }

            if (id) {
                items.push({ id: parseInt(id), order: idx });
                // Also update order input field if present in changelist
                const orderInput = r.querySelector('input[name$="-order"]');
                if (orderInput) orderInput.value = idx;
            }
        });

        if (items.length === 0) return;

        fetch('/cms/api/reorder-menus/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: JSON.stringify({ items: items })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                showToast('✓ Urutan menu berhasil disimpan secara realtime!');
            } else {
                showToast('Gagal menyimpan urutan: ' + (data.message || 'Error'), true);
            }
        })
        .catch(err => {
            console.error('Error reordering menus:', err);
            showToast('Koneksi bermasalah saat menyimpan urutan.', true);
        });
    }
});
