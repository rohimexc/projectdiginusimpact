/**
 * =================================================================
 * 1. STATE & STORAGE MANAGEMENT
 * =================================================================
 */
// Objek penampung master opsi kategori berdasarkan jenis transaksi.
// Dipisah jadi object supaya gampang ditarik dinamis sesuai dropdown jenis.
const categories = {
    income: ["Gaji", "Bonus", "THR", "Investasi"],
    expense: ["Makanan", "Transportasi", "ATK & Cetak", "Tagihan", "Hiburan"]
};

// Mengambil data dari localStorage saat aplikasi pertama kali dimuat.
// Menggunakan JSON.parse untuk ubah string JSON ke array objek, 
// dan short-circuit (|| []) agar tidak error null saat data masih kosong.
let transactions = JSON.parse(localStorage.getItem('transactions')) || [];

// State aktif untuk filter tabel & pencarian
let activeFilterType = 'all';
let activeFilterCategory = 'all';
let activeSearchQuery = '';

/**
 * =================================================================
 * 2. DOM SELECTION (JEMBATAN HTML KE JAVASCRIPT)
 * =================================================================
 */
const balanceEl = document.getElementById('balance');
const moneyPlusEl = document.getElementById('money-plus');
const moneyMinusEl = document.getElementById('money-minus');
const datatableBody = document.getElementById('datatable-body');
const dataCountEl = document.getElementById('data-count');
const form = document.getElementById('form');
const formTitleEl = document.getElementById('form-title');
const formErrorEl = document.getElementById('form-error');
const typeSelect = document.getElementById('type');
const categorySelect = document.getElementById('category');
const descriptionInput = document.getElementById('description');
const amountInput = document.getElementById('amount');
const editIdInput = document.getElementById('edit-id');
const submitBtn = document.getElementById('submit-btn');
const cancelEditBtn = document.getElementById('cancel-edit-btn');
const filterTypeEl = document.getElementById('filter-type');
const filterCategoryEl = document.getElementById('filter-category');
const searchInput = document.getElementById('search-input');
const resetBtn = document.getElementById('reset-btn');
const loadingOverlay = document.getElementById('loading-overlay');
const toastContainer = document.getElementById('toast-container');

/**
 * =================================================================
 * 3. HELPER STORAGE & SIMULASI LOADING ASYNC
 * =================================================================
 */
// Menyimpan array transactions ke localStorage agar persistent (tidak hilang saat refresh)
const saveToLocalStorage = () => {
    localStorage.setItem('transactions', JSON.stringify(transactions));
};

// Simulasi loading state async (memakai Promise & setTimeout) 
// untuk memenuhi kriteria fitur loading state saat mutasi data berat/simpan.
const simulateAsyncOperation = (callback, delay = 250) => {
    loadingOverlay.classList.remove('hidden');
    setTimeout(() => {
        try {
            callback();
        } catch (err) {
            handleError(err);
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    }, delay);
};

// Fungsi Error Handling terpusat
const handleError = (error) => {
    console.error("Terjadi error aplikasi:", error);
    showToast(error.message || 'Terjadi kesalahan sistem!', 'error');
};

// Sistem Toast Notification (Tantangan Tambahan)
const showToast = (message, type = 'success') => {
    const toast = document.createElement('div');
    const bgClass = type === 'error' ? 'bg-rose-600 text-white' : 'bg-slate-800 text-white';
    toast.className = `${bgClass} px-4 py-3 rounded-xl shadow-lg text-xs font-semibold flex items-center justify-between gap-3 animate-fade-in`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="text-white/70 hover:text-white font-bold">&times;</button>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
        if (toast.parentElement) toast.remove();
    }, 3000);
};

/**
 * =================================================================
 * 4. RENDER & VALIDASI FORM DINAMIS KATEGORI
 * =================================================================
 */
// Merender opsi kategori di form berdasar pilihan select jenis
const renderFormCategories = () => {
    categorySelect.innerHTML = '';
    const selectedType = typeSelect.value;
    categories[selectedType].forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
};

// Mengisi dropdown filter kategori secara dinamis dari gabungan kategori yang ada
const renderFilterCategories = () => {
    const currentVal = filterCategoryEl.value;
    filterCategoryEl.innerHTML = '<option value="all">Semua Kategori</option>';
    const allCats = [...categories.income, ...categories.expense];
    allCats.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        filterCategoryEl.appendChild(option);
    });
    filterCategoryEl.value = currentVal;
};

// Validasi form transaksi (menggunakan try...catch sesuai aturan error handling)
const validateTransactionForm = (desc, amount) => {
    try {
        if (!desc.trim()) {
            throw new Error('Keterangan transaksi wajib diisi!');
        }
        if (isNaN(amount) || amount <= 0) {
            throw new Error('Nominal harus berupa angka lebih besar dari 0!');
        }
        formErrorEl.classList.add('hidden');
        return true;
    } catch (err) {
        formErrorEl.textContent = err.message;
        formErrorEl.classList.remove('hidden');
        return false;
    }
};

/**
 * =================================================================
 * 5. FORMATTER MATA UANG
 * =================================================================
 */
// Format angka jadi Rupiah pakai Intl.NumberFormat standar Indonesia
const formatRp = (num) => {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(Math.abs(num));
};

/**
 * =================================================================
 * 6. KALKULASI & RENDER DATATABLE
 * =================================================================
 */
// Menghitung total income, expense, dan balance menggunakan .reduce()
const updateDashboardValues = (filteredData) => {
    const income = filteredData
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    const expense = filteredData
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    const balance = income - expense;

    balanceEl.innerText = formatRp(balance);
    moneyPlusEl.innerText = `+ ${formatRp(income)}`;
    moneyMinusEl.innerText = `- ${formatRp(expense)}`;
};

// Render utama list/datatable dan filter state
const renderApp = () => {
    // 1. Filter data array berdasarkan pencarian dan dropdown filter
    const filteredData = transactions.filter(t => {
        const matchesType = activeFilterType === 'all' || t.type === activeFilterType;
        const matchesCategory = activeFilterCategory === 'all' || t.category === activeFilterCategory;
        const matchesSearch = t.description.toLowerCase().includes(activeSearchQuery.toLowerCase());
        return matchesType && matchesCategory && matchesSearch;
    });

    // 2. Kosongkan tabel DOM
    datatableBody.innerHTML = '';

    // 3. Tangani Empty State (Tantangan tambahan jika kosong)
    if (filteredData.length === 0) {
        datatableBody.innerHTML = `
            <tr>
                <td colspan="4" class="p-8 text-center text-slate-400">
                    <p class="font-medium">Belum ada data transaksi yang cocok.</p>
                </td>
            </tr>
        `;
    } else {
        // 4. Looping data yang sudah difilter untuk dimasukkan ke datatable row
        filteredData.forEach(t => {
            const isIncome = t.type === 'income';
            const sign = isIncome ? '+' : '-';
            const textAmountColor = isIncome ? 'text-emerald-600' : 'text-rose-600';
            const badgeTypeColor = isIncome ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700';

            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50/80 transition';
            tr.innerHTML = `
                <td class="p-3">
                    <span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase ${badgeTypeColor} mb-0.5">
                        ${isIncome ? 'Pemasukan' : 'Pengeluaran'}
                    </span>
                    <p class="font-semibold text-slate-700 text-sm">${t.description}</p>
                </td>
                <td class="p-3 text-slate-600 text-xs">${t.category}</td>
                <td class="p-3 text-right font-bold ${textAmountColor}">
                    ${sign} ${formatRp(t.amount)}
                </td>
                <td class="p-3 text-center">
                    <div class="flex items-center justify-center gap-1.5">
                        <button data-id="${t.id}" class="edit-btn text-indigo-600 hover:bg-indigo-50 p-1.5 rounded text-xs font-semibold">Edit</button>
                        <button data-id="${t.id}" class="delete-btn text-rose-600 hover:bg-rose-50 p-1.5 rounded text-xs font-semibold">Hapus</button>
                    </div>
                </td>
            `;
            datatableBody.appendChild(tr);
        });
    }

    // 5. Update counter dan rekap angka dashboard
    dataCountEl.innerText = `${filteredData.length} data ditampilkan`;
    updateDashboardValues(filteredData);
};

/**
 * =================================================================
 * 7. CRUD OPERATIONS (CREATE, READ, UPDATE, DELETE)
 * =================================================================
 */
// Mode Edit: Mengisi form dari data item yang dipilih
const startEditTransaction = (id) => {
    const item = transactions.find(t => t.id === id);
    if (!item) return;

    editIdInput.value = item.id;
    typeSelect.value = item.type;
    renderFormCategories(); // Sinkronkan opsi kategori sesuai jenis
    categorySelect.value = item.category;
    descriptionInput.value = item.description;
    amountInput.value = item.amount;

    formTitleEl.innerText = 'Edit Transaksi';
    submitBtn.innerText = 'Perbarui Transaksi';
    cancelEditBtn.classList.remove('hidden');
    descriptionInput.focus();
};

// Batalkan mode edit
const cancelEditMode = () => {
    editIdInput.value = '';
    form.reset();
    renderFormCategories();
    formTitleEl.innerText = 'Tambah Transaksi Baru';
    submitBtn.innerText = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
    formErrorEl.classList.add('hidden');
};

// Hapus transaksi berdasarkan ID (memakai konfirmasi sederhana/toast)
const removeTransaction = (id) => {
    simulateAsyncOperation(() => {
        transactions = transactions.filter(t => t.id !== Number(id));
        saveToLocalStorage();
        renderApp();
        showToast('Transaksi berhasil dihapus!', 'error');
    });
};

/**
 * =================================================================
 * 8. EVENT LISTENERS
 * =================================================================
 */
// Event ganti jenis di form agar kategori ikut berubah dinamis
typeSelect.addEventListener('change', renderFormCategories);

// Event submit form (Handle Create & Update)
form.addEventListener('submit', (e) => {
    e.preventDefault();
    const desc = descriptionInput.value;
    const amount = parseFloat(amountInput.value);

    if (!validateTransactionForm(desc, amount)) return;

    simulateAsyncOperation(() => {
        const editId = editIdInput.value;

        if (editId) {
            // Update existing data
            const index = transactions.findIndex(t => t.id === Number(editId));
            if (index !== -1) {
                transactions[index] = {
                    ...transactions[index],
                    type: typeSelect.value,
                    category: categorySelect.value,
                    description: desc,
                    amount: amount
                };
            }
            showToast('Transaksi berhasil diperbarui!');
            cancelEditMode();
        } else {
            // Create new data
            const newTransaction = {
                id: Date.now(), // Generate unique ID berbasis timestamp
                type: typeSelect.value,
                category: categorySelect.value,
                description: desc,
                amount: amount
            };
            transactions.push(newTransaction);
            showToast('Transaksi berhasil ditambahkan!');
            form.reset();
            renderFormCategories();
        }

        saveToLocalStorage();
        renderApp();
    });
});

// Event batal edit
cancelEditBtn.addEventListener('click', cancelEditMode);

// Event Delegation pada tabel (klik Edit / Hapus)
datatableBody.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
        const id = e.target.dataset.id;
        removeTransaction(id);
    } else if (e.target.classList.contains('edit-btn')) {
        const id = Number(e.target.dataset.id);
        startEditTransaction(id);
    }
});

// Event Filter & Search real-time
filterTypeEl.addEventListener('change', (e) => {
    activeFilterType = e.target.value;
    renderApp();
});

filterCategoryEl.addEventListener('change', (e) => {
    activeFilterCategory = e.target.value;
    renderApp();
});

searchInput.addEventListener('input', (e) => {
    activeSearchQuery = e.target.value;
    renderApp();
});

// Event Reset seluruh data aplikasi (Tantangan Tambahan)
resetBtn.addEventListener('click', () => {
    if (confirm('Yakin ingin mereset seluruh data pencatatan?')) {
        simulateAsyncOperation(() => {
            transactions = [];
            localStorage.removeItem('transactions');
            cancelEditMode();
            renderApp();
            showToast('Semua data berhasil direset!', 'error');
        });
    }
});

/**
 * =================================================================
 * 9. INISIALISASI PERTAMA KALI (BOOTSTRAP UI)
 * =================================================================
 */
const init = () => {
    renderFormCategories();
    renderFilterCategories();
    renderApp();
};

// Jalankan aplikasi saat script dimuat
init();