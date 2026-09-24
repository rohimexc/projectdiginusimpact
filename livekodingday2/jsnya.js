/**
 * =========================================================================
 * 1. MANAJEMEN STATE & PENYIMPANAN DATA
 * =========================================================================
 */

// Kumpulan daftar opsi kategori bawaan yang dipisahkan berdasarkan jenis transaksi
const categories = {
    expense: ['Makanan & Minuman', 'Transportasi', 'Belanja', 'Tagihan', 'Hiburan', 'Lainnya'],
    income: ['Gaji', 'Uang Saku', 'Bonus', 'Investasi', 'Penjualan', 'Lainnya']
};

// Mengambil data dari localStorage saat aplikasi pertama kali dimuat
// Jika tidak ada data tersimpan, buat array kosong default
let transactions = JSON.parse(localStorage.getItem('transactions_data')) || [];

// Variabel global untuk menyimpan referensi instance Chart agar bisa di-update dinamis
let categoryChartInstance = null;
let comparisonChartInstance = null;


/**
 * =========================================================================
 * 2. SELEKSI ELEMEN DOM
 * =========================================================================
 */
const balance = document.getElementById('balance');
const moneyPlus = document.getElementById('money-plus');
const moneyMinus = document.getElementById('money-minus');

const form = document.getElementById('form');
const formTitle = document.getElementById('form-title');
const editIdInput = document.getElementById('edit-id');
const typeSelect = document.getElementById('type');
const categorySelect = document.getElementById('category');
const descInput = document.getElementById('desc');
const amountInput = document.getElementById('amount');
const submitBtn = document.getElementById('submit-btn');
const cancelEditBtn = document.getElementById('cancel-edit-btn');

const searchInput = document.getElementById('search-input');
const filterType = document.getElementById('filter-type');
const filterCategory = document.getElementById('filter-category');
const transactionRows = document.getElementById('transaction-rows');
const emptyState = document.getElementById('empty-state');
const loading = document.getElementById('loading');


/**
 * =========================================================================
 * 3. PERSISTENSI KE LOCALSTORAGE
 * =========================================================================
 */
const syncLocalStorage = () => {
    try {
        localStorage.setItem('transactions_data', JSON.stringify(transactions));
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Penyimpanan Penuh',
            text: 'Gagal menyimpan transaksi ke memori browser.'
        });
    }
};


/**
 * =========================================================================
 * 4. HELPER FORMAT MATA UANG
 * =========================================================================
 */
const formatRp = (num) => {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(Math.abs(num));
};


/**
 * =========================================================================
 * 5. PENGATURAN DROPDOWN KATEGORI
 * =========================================================================
 */
const renderCategories = () => {
    categorySelect.innerHTML = '';
    const currentList = categories[typeSelect.value] || [];

    currentList.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
};

const renderFilterCategoryOptions = () => {
    filterCategory.innerHTML = '<option value="all">Semua Kategori</option>';
    const allCategories = [...new Set([...categories.expense, ...categories.income])];

    allCategories.forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        filterCategory.appendChild(opt);
    });
};


/**
 * =========================================================================
 * 6. KALKULASI RINGKASAN SALDO
 * =========================================================================
 */
const updateValues = () => {
    const income = transactions
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    const expense = transactions
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    const total = income - expense;

    balance.innerText = formatRp(total);
    moneyPlus.innerText = `+ ${formatRp(income)}`;
    moneyMinus.innerText = `- ${formatRp(expense)}`;
};


/**
 * =========================================================================
 * 7. VISUALISASI CHART.JS & UPDATE DINAMIS
 * =========================================================================
 */

// Menyiapkan data agregasi pengeluaran per kategori untuk Doughnut Chart
const getExpenseCategoryData = () => {
    // 1. Ambil seluruh transaksi yang berjenis pengeluaran
    const expenseData = transactions.filter(t => t.type === 'expense');

    // 2. Dapatkan daftar nama kategori unik dari pengeluaran yang ada
    const categoryLabels = [...new Set(expenseData.map(t => t.category))];

    // 3. Hitung total nominal untuk tiap kategori unik
    const categoryTotals = categoryLabels.map(cat => {
        return expenseData
            .filter(t => t.category === cat)
            .reduce((acc, t) => acc + t.amount, 0);
    });

    return {
        labels: categoryLabels.length > 0 ? categoryLabels : ['Belum Ada Data'],
        data: categoryTotals.length > 0 ? categoryTotals : [0]
    };
};

// Menyiapkan data komparasi pemasukan vs pengeluaran untuk Bar Chart
const getIncomeVsExpenseData = () => {
    const totalIncome = transactions
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    const totalExpense = transactions
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    return [totalIncome, totalExpense];
};

// Inisialisasi awal kedua objek Chart.js
const initCharts = () => {
    // Chart 1: Doughnut Chart
    const ctxCategory = document.getElementById('categoryChart').getContext('2d');
    const catData = getExpenseCategoryData();

    categoryChartInstance = new Chart(ctxCategory, {
        type: 'doughnut',
        data: {
            labels: catData.labels,
            datasets: [{
                data: catData.data,
                backgroundColor: [
                    '#f43f5e', '#fb923c', '#facc15', 
                    '#a855f7', '#06b6d4', '#64748b'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    // Chart 2: Bar Chart
    const ctxComparison = document.getElementById('comparisonChart').getContext('2d');
    comparisonChartInstance = new Chart(ctxComparison, {
        type: 'bar',
        data: {
            labels: ['Pemasukan', 'Pengeluaran'],
            datasets: [{
                label: 'Total Nominal (Rp)',
                data: getIncomeVsExpenseData(),
                backgroundColor: ['#10b981', '#f43f5e'],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => 'Rp ' + value.toLocaleString('id-ID')
                    }
                }
            }
        }
    });
};

// Fungsi krusial: Memperbarui isi chart setiap ada penambahan, pengubahan, atau penghapusan transaksi
const updateCharts = () => {
    if (!categoryChartInstance || !comparisonChartInstance) return;

    // Perbarui Doughnut Chart
    const catData = getExpenseCategoryData();
    categoryChartInstance.data.labels = catData.labels;
    categoryChartInstance.data.datasets[0].data = catData.data;
    categoryChartInstance.update();

    // Perbarui Bar Chart
    comparisonChartInstance.data.datasets[0].data = getIncomeVsExpenseData();
    comparisonChartInstance.update();
};


/**
 * =========================================================================
 * 8. MANIPULASI DOM TABEL & ASYNC LOADING
 * =========================================================================
 */
const createRowDOM = (item) => {
    const isIncome = item.type === 'income';
    const sign = isIncome ? '+' : '-';
    const badgeColor = isIncome ? 'text-emerald-700 bg-emerald-50' : 'text-rose-700 bg-rose-50';

    const tr = document.createElement('tr');
    tr.className = 'hover:bg-slate-50/80 transition-colors';
    tr.dataset.id = item.id;

    tr.innerHTML = `
        <td class="p-3">
            <span class="inline-block px-2.5 py-1 text-xs font-semibold rounded-md ${badgeColor}">
                ${item.category}
            </span>
        </td>
        <td class="p-3 font-medium text-slate-700">
            ${item.desc || '-'}
        </td>
        <td class="p-3 text-right font-bold ${isIncome ? 'text-emerald-600' : 'text-rose-600'}">
            ${sign} ${formatRp(item.amount)}
        </td>
        <td class="p-3 text-center space-x-1">
            <button class="edit-btn text-xs bg-amber-50 hover:bg-amber-100 text-amber-700 font-semibold px-2 py-1 rounded transition">
                Edit
            </button>
            <button class="delete-btn text-xs bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold px-2 py-1 rounded transition">
                Hapus
            </button>
        </td>
    `;
    return tr;
};

const renderTable = async () => {
    loading.classList.remove('hidden');
    transactionRows.innerHTML = '';
    emptyState.classList.add('hidden');

    // Jeda simulasi pemrosesan asinkron
    await new Promise(resolve => setTimeout(resolve, 80));

    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedType = filterType.value;
    const selectedCat = filterCategory.value;

    const filtered = transactions.filter(t => {
        const matchesType = (selectedType === 'all') || (t.type === selectedType);
        const matchesCat = (selectedCat === 'all') || (t.category === selectedCat);
        const matchesSearch = (t.desc || '').toLowerCase().includes(searchTerm) || 
                              t.category.toLowerCase().includes(searchTerm);

        return matchesType && matchesCat && matchesSearch;
    });

    loading.classList.add('hidden');

    if (filtered.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }

    filtered.forEach(item => {
        transactionRows.appendChild(createRowDOM(item));
    });
};


/**
 * =========================================================================
 * 9. STATE & LOGIKA CRUD
 * =========================================================================
 */
const resetFormState = () => {
    form.reset();
    editIdInput.value = '';
    formTitle.textContent = 'Tambah Transaksi Baru';
    submitBtn.textContent = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
    renderCategories();
};

const startEditTransaction = (id) => {
    const item = transactions.find(t => t.id === id);
    if (!item) return;

    editIdInput.value = item.id;
    typeSelect.value = item.type;
    renderCategories();
    categorySelect.value = item.category;
    descInput.value = item.desc || '';
    amountInput.value = item.amount;

    formTitle.textContent = 'Edit Transaksi';
    submitBtn.textContent = 'Perbarui Transaksi';
    cancelEditBtn.classList.remove('hidden');

    window.scrollTo({ top: form.offsetTop - 20, behavior: 'smooth' });
};

// Implementasi SweetAlert Confirmation Dialog sebelum menghapus
const deleteTransaction = (id) => {
    Swal.fire({
        title: 'Konfirmasi Hapus',
        text: 'Apakah kamu yakin ingin menghapus transaksi ini?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4f46e5',
        cancelButtonColor: '#e11d48',
        confirmButtonText: 'Ya, Hapus!',
        cancelButtonText: 'Batal'
    }).then((result) => {
        // Logika percabangan SweetAlert: Cek jika tombol konfirmasi ditekan
        if (result.isConfirmed) {
            transactions = transactions.filter(t => t.id !== id);

            syncLocalStorage();
            updateValues();
            updateCharts();
            renderTable();

            Swal.fire({
                icon: 'success',
                title: 'Terhapus!',
                text: 'Transaksi berhasil dihapus.',
                timer: 1500,
                showConfirmButton: false
            });
        }
    });
};


/**
 * =========================================================================
 * 10. EVENT LISTENERS
 * =========================================================================
 */

// Render kategori saat dropdown tipe diubah
typeSelect.addEventListener('change', renderCategories);

// Submit form (Tambah atau Edit transaksi)
form.addEventListener('submit', (e) => {
    e.preventDefault();

    const amountVal = parseFloat(amountInput.value);
    const descVal = descInput.value.trim(); // .trim() menghapus spasi kosong

    // 1. Validasi Kolom Keterangan: Wajib diisi (tidak boleh kosong)
    if (descVal === '') {
        Swal.fire({
            icon: 'error',
            title: 'Validasi Gagal',
            text: 'Keterangan transaksi wajib diisi!'
        });
        descInput.focus(); // Mengarahkan kursor langsung ke input keterangan
        return;
    }

    // 2. Validasi Kolom Nominal: Harus angka lebih besar dari 0
    if (isNaN(amountVal) || amountVal <= 0) {
        Swal.fire({
            icon: 'error',
            title: 'Validasi Gagal',
            text: 'Nominal transaksi harus berupa angka lebih besar dari 0!'
        });
        amountInput.focus();
        return;
    }

    const editId = editIdInput.value;

    if (editId) {
        // Mode Update
        const index = transactions.findIndex(t => t.id === Number(editId));
        if (index !== -1) {
            transactions[index] = {
                ...transactions[index],
                type: typeSelect.value,
                category: categorySelect.value,
                desc: descVal,
                amount: amountVal
            };

            Swal.fire({
                icon: 'success',
                title: 'Berhasil',
                text: 'Transaksi berhasil diperbarui!',
                timer: 1500,
                showConfirmButton: false
            });
        }
    } else {
        // Mode Tambah Baru
        const newTransaction = {
            id: Date.now(),
            type: typeSelect.value,
            category: categorySelect.value,
            desc: descVal,
            amount: amountVal
        };
        transactions.unshift(newTransaction);

        Swal.fire({
            icon: 'success',
            title: 'Berhasil',
            text: 'Transaksi berhasil ditambahkan!',
            timer: 1500,
            showConfirmButton: false
        });
    }

    syncLocalStorage();
    updateValues();
    updateCharts();
    renderTable();
    resetFormState();
});

cancelEditBtn.addEventListener('click', resetFormState);

// Event delegation pada baris tabel transaksi
transactionRows.addEventListener('click', (e) => {
    const tr = e.target.closest('tr');
    if (!tr) return;
    const id = Number(tr.dataset.id);

    if (e.target.classList.contains('delete-btn')) {
        deleteTransaction(id);
    } else if (e.target.classList.contains('edit-btn')) {
        startEditTransaction(id);
    }
});

// Event listener filter dan pencarian
searchInput.addEventListener('input', renderTable);
filterType.addEventListener('change', renderTable);
filterCategory.addEventListener('change', renderTable);


/**
 * =========================================================================
 * 11. BOOTSTRAP INISIALISASI APLIKASI
 * =========================================================================
 */
const initApp = () => {
    renderCategories();
    renderFilterCategoryOptions();
    updateValues();
    initCharts();
    renderTable();
};

initApp();