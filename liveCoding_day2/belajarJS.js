/**
 * =================================================================
 * 1. STATE & STORAGE MANAGEMENT
 * =================================================================
 */
// Menyimpan daftar master kategori untuk jenis pemasukan dan pengeluaran.
const categories = {
    income: ["Gaji", "Bonus", "Freelance", "Hadiah"],
    expense: ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan"]
};

// Mengambil data transaksi dari localStorage browser agar data tidak hilang saat halaman direfresh.
// Jika data kosong, inisialisasi dengan array kosong [].
let transactions = JSON.parse(localStorage.getItem('upgrade_transactions')) || [];

// Variabel penampung state aktif untuk fitur filter dan pencarian real-time.
let activeFilterType = 'all';
let activeFilterCategory = 'all';
let activeSearchQuery = '';

// Variabel penampung instance Chart.js untuk mendeteksi grafik yang sudah ada (mencegah duplikasi canvas).
let incomeChartInstance = null;
let expenseChartInstance = null;
let incomeExpenseChartInstance = null;

/**
 * =================================================================
 * 2. DOM SELECTION (JEMBATAN HTML KE JAVASCRIPT)
 * =================================================================
 */
// Menangkap elemen-elemen HTML berdasarkan ID agar dapat dimanipulasi secara dinamis.
const balanceEl = document.getElementById('balance');
const moneyPlusEl = document.getElementById('money-plus');
const moneyMinusEl = document.getElementById('money-minus');
const datatableBody = document.getElementById('datatable-body');
const dataCountEl = document.getElementById('data-count');
const form = document.getElementById('form');
const formTitleEl = document.getElementById('form-title');
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

/**
 * =================================================================
 * 3. HELPER STORAGE
 * =================================================================
 */
// Fungsi untuk menyimpan array transactions ke localStorage 
// dengan mengubahnya menjadi format string JSON menggunakan JSON.stringify().
const saveToLocalStorage = () => {
    localStorage.setItem('upgrade_transactions', JSON.stringify(transactions));
};

/**
 * =================================================================
 * 4. RENDER FORM, VALIDASI, & FORMATTER
 * =================================================================
 */
// Fungsi untuk mengisi opsi dropdown kategori di form sesuai dengan pilihan jenis transaksi (income/expense).
const renderFormCategories = () => {
    categorySelect.innerHTML = '';
    categories[typeSelect.value].forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
};

// Fungsi untuk mengisi pilihan pada elemen filter kategori di tabel.
const renderFilterCategories = () => {
    const currentVal = filterCategoryEl.value;
    filterCategoryEl.innerHTML = '<option value="all">Semua Kategori</option>';
    [...categories.income, ...categories.expense].forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        filterCategoryEl.appendChild(option);
    });
    filterCategoryEl.value = currentVal;
};

// Fungsi validasi form menggunakan library SweetAlert2 untuk menampilkan pesan error interaktif.
const validateTransactionForm = (desc, amount) => {
    if (!desc.trim()) {
        Swal.fire({
            icon: 'error',
            title: 'Validasi Gagal',
            text: 'Keterangan transaksi wajib diisi!'
        });
        return false;
    }
    if (isNaN(amount) || amount <= 0) {
        Swal.fire({
            icon: 'error',
            title: 'Validasi Gagal',
            text: 'Nominal transaksi harus lebih dari 0!'
        });
        return false;
    }
    return true;
};

// Fungsi untuk memformat angka mentah menjadi format mata uang Rupiah (IDR).
const formatRp = (num) => {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(Math.abs(num));
};

/**
 * =================================================================
 * 5. INTEGRASI CHART.JS (BAR CHART & 2 DOUGHNUT CHART)
 * =================================================================
 */
// Fungsi utama untuk membuat dan memperbarui ketiga grafik secara dinamis.
const initCharts = () => {
    // --- Chart 1: Bar Chart Pemasukan vs Pengeluaran ---
    // Menghitung total keseluruhan uang masuk dan keluar dari data transaksi.
    const totalIncome = transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
    const totalExpense = transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);

    const ctxIncomeExpense = document.getElementById('incomeExpenseChart').getContext('2d');
    if (incomeExpenseChartInstance) incomeExpenseChartInstance.destroy(); // Hancurkan instance lama agar tidak konflik

    incomeExpenseChartInstance = new Chart(ctxIncomeExpense, {
        type: 'bar',
        data: {
            labels: ['Pemasukan', 'Pengeluaran'],
            datasets: [{
                label: 'Total (Rp)',
                data: [totalIncome, totalExpense],
                backgroundColor: ['#10b981', '#ef4444']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });

    // --- Chart 2: Doughnut Chart Kategori Pemasukan ---
    // Menyaring data pemasukan, mengambil kategori unik menggunakan Set, lalu menjumlahkan nominalnya per kategori.
    const incomeData = transactions.filter(t => t.type === 'income');
    const incomeCategories = [...new Set(incomeData.map(t => t.category))];
    const incomeCategoryTotals = incomeCategories.map(cat => {
        return incomeData
            .filter(t => t.category === cat)
            .reduce((sum, t) => sum + t.amount, 0);
    });

    const ctxIncome = document.getElementById('incomeCategoryChart').getContext('2d');
    if (incomeChartInstance) incomeChartInstance.destroy();

    incomeChartInstance = new Chart(ctxIncome, {
        type: 'doughnut',
        data: {
            labels: incomeCategories.length > 0 ? incomeCategories : ['Belum ada data'],
            datasets: [{
                data: incomeCategoryTotals.length > 0 ? incomeCategoryTotals : [1],
                backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#6366f1']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    // --- Chart 3: Doughnut Chart Kategori Pengeluaran ---
    // Menyaring data pengeluaran, mengambil kategori unik, dan menghitung total nominalnya.
    const expenseData = transactions.filter(t => t.type === 'expense');
    const expenseCategories = [...new Set(expenseData.map(t => t.category))];
    const expenseCategoryTotals = expenseCategories.map(cat => {
        return expenseData
            .filter(t => t.category === cat)
            .reduce((sum, t) => sum + t.amount, 0);
    });

    const ctxExpense = document.getElementById('expenseCategoryChart').getContext('2d');
    if (expenseChartInstance) expenseChartInstance.destroy();

    expenseChartInstance = new Chart(ctxExpense, {
        type: 'doughnut',
        data: {
            labels: expenseCategories.length > 0 ? expenseCategories : ['Belum ada data'],
            datasets: [{
                data: expenseCategoryTotals.length > 0 ? expenseCategoryTotals : [1],
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#ec4899', '#6366f1']
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });
};

/**
 * =================================================================
 * 6. KALKULASI SALDO & RENDER DATATABLE
 * =================================================================
 */
// Menghitung total pemasukan, pengeluaran, dan sisa saldo bersih menggunakan .reduce().
const updateDashboardValues = (filteredData) => {
    const income = filteredData.filter(t => t.type === 'income').reduce((acc, t) => acc + t.amount, 0);
    const expense = filteredData.filter(t => t.type === 'expense').reduce((acc, t) => acc + t.amount, 0);
    const balance = income - expense;

    balanceEl.innerText = formatRp(balance);
    moneyPlusEl.innerText = `+ ${formatRp(income)}`;
    moneyMinusEl.innerText = `- ${formatRp(expense)}`;
};

// Fungsi utama untuk memfilter data, merender ulang isi tabel, memperbarui kartu saldo, dan merefresh grafik.
const renderApp = () => {
    const filteredData = transactions.filter(t => {
        const matchesType = activeFilterType === 'all' || t.type === activeFilterType;
        const matchesCategory = activeFilterCategory === 'all' || t.category === activeFilterCategory;
        const matchesSearch = t.description.toLowerCase().includes(activeSearchQuery.toLowerCase());
        return matchesType && matchesCategory && matchesSearch;
    });

    datatableBody.innerHTML = '';

    // Menangani tampilan jika data kosong (Empty State).
    if (filteredData.length === 0) {
        datatableBody.innerHTML = `
            <tr>
                <td colspan="4" class="p-8 text-center text-slate-400">Belum ada data transaksi.</td>
            </tr>
        `;
    } else {
        // Melakukan perulangan (looping) pada data yang lolos filter untuk dimasukkan ke baris tabel HTML.
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
                <td class="p-3 text-right font-bold ${textAmountColor}">${sign} ${formatRp(t.amount)}</td>
                <td class="p-3 text-center">
                    <div class="flex items-center justify-center gap-1.5">
                        <button data-id="${t.id}" class="edit-btn text-blue-600 hover:bg-blue-50 p-1.5 rounded text-xs font-semibold">Edit</button>
                        <button data-id="${t.id}" class="delete-btn text-rose-600 hover:bg-rose-50 p-1.5 rounded text-xs font-semibold">Hapus</button>
                    </div>
                </td>
            `;
            datatableBody.appendChild(tr);
        });
    }

    dataCountEl.innerText = `${filteredData.length} data ditampilkan`;
    updateDashboardValues(filteredData);
    initCharts(); // Memperbarui grafik secara otomatis setiap kali aplikasi melakukan render ulang.
};

/**
 * =================================================================
 * 7. CRUD OPERATIONS DENGAN SWEETALERT
 * =================================================================
 */
// Fungsi untuk memuat data lama ke dalam form saat tombol Edit diklik.
const startEditTransaction = (id) => {
    const item = transactions.find(t => t.id === id);
    if (!item) return;

    editIdInput.value = item.id;
    typeSelect.value = item.type;
    renderFormCategories();
    categorySelect.value = item.category;
    descriptionInput.value = item.description;
    amountInput.value = item.amount;

    formTitleEl.innerText = 'Edit Transaksi';
    submitBtn.innerText = 'Perbarui Transaksi';
    cancelEditBtn.classList.remove('hidden');
    descriptionInput.focus();
};

// Fungsi untuk membatalkan mode edit dan mereset form kembali seperti semula.
const cancelEditMode = () => {
    editIdInput.value = '';
    form.reset();
    renderFormCategories();
    formTitleEl.innerText = 'Tambah Transaksi Baru';
    submitBtn.innerText = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
};

// Fungsi untuk menghapus transaksi menggunakan dialog konfirmasi SweetAlert2.
const removeTransaction = (id) => {
    Swal.fire({
        title: 'Apakah kamu yakin?',
        text: "Ingin menghapus transaksi ini?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#64748b',
        confirmButtonText: 'Ya, Hapus!',
        cancelButtonText: 'Batal'
    }).then((result) => {
        if (result.isConfirmed) {
            transactions = transactions.filter(t => t.id !== Number(id));
            saveToLocalStorage();
            renderApp();
            Swal.fire('Terhapus!', 'Transaksi berhasil dihapus.', 'success');
        }
    });
};

/**
 * =================================================================
 * 8. EVENT LISTENERS
 * =================================================================
 */
// Event listener untuk mengubah opsi kategori di form secara otomatis saat jenis transaksi diganti.
typeSelect.addEventListener('change', renderFormCategories);

// Event listener saat form disubmit (menangani proses Tambah Data baru atau Perbarui Data lama).
form.addEventListener('submit', (e) => {
    e.preventDefault(); // Mencegah browser melakukan reload halaman secara bawaan.
    const desc = descriptionInput.value;
    const amount = parseFloat(amountInput.value);

    // Memeriksa validasi input menggunakan SweetAlert.
    if (!validateTransactionForm(desc, amount)) return;

    const editId = editIdInput.value;

    if (editId) {
        // Logika untuk memperbarui data yang sudah ada (Update).
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
        Swal.fire({
            icon: 'success',
            title: 'Berhasil!',
            text: 'Transaksi berhasil diperbarui!',
            timer: 1500,
            showConfirmButton: false
        });
        cancelEditMode();
    } else {
        // Logika untuk menambahkan data transaksi baru (Create).
        transactions.push({
            id: Date.now(), // Membuat ID unik berdasarkan waktu milidetik saat ini.
            type: typeSelect.value,
            category: categorySelect.value,
            description: desc,
            amount: amount
        });
        Swal.fire({
            icon: 'success',
            title: 'Berhasil!',
            text: 'Transaksi berhasil ditambahkan!',
            timer: 1500,
            showConfirmButton: false
        });
        form.reset();
        renderFormCategories();
    }

    saveToLocalStorage();
    renderApp();
});

// Event listener untuk tombol batal edit.
cancelEditBtn.addEventListener('click', cancelEditMode);

// Event delegation pada bodi tabel untuk mendeteksi klik tombol Edit atau Hapus.
datatableBody.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
        removeTransaction(e.target.dataset.id);
    } else if (e.target.classList.contains('edit-btn')) {
        startEditTransaction(Number(e.target.dataset.id));
    }
});

// Event listener untuk filter jenis transaksi secara real-time.
filterTypeEl.addEventListener('change', (e) => {
    activeFilterType = e.target.value;
    renderApp();
});

// Event listener untuk filter kategori transaksi secara real-time.
filterCategoryEl.addEventListener('change', (e) => {
    activeFilterCategory = e.target.value;
    renderApp();
});

// Event listener untuk kotak pencarian teks secara real-time.
searchInput.addEventListener('input', (e) => {
    activeSearchQuery = e.target.value;
    renderApp();
});

// Event listener untuk tombol reset seluruh data dengan konfirmasi SweetAlert.
resetBtn.addEventListener('click', () => {
    Swal.fire({
        title: 'Reset Seluruh Data?',
        text: "Semua catatan transaksi akan dihapus permanen!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3b82f6',
        cancelButtonColor: '#64748b',
        confirmButtonText: 'Ya, Reset!',
        cancelButtonText: 'Batal'
    }).then((result) => {
        if (result.isConfirmed) {
            transactions = [];
            localStorage.removeItem('upgrade_transactions');
            cancelEditMode();
            renderApp();
            Swal.fire('Terreset!', 'Semua data berhasil dibersihkan.', 'success');
        }
    });
});

/**
 * =================================================================
 * 9. INITIALIZATION (INISIALISASI PERTAMA KALI)
 * =================================================================
 */
// Fungsi untuk menjalankan seluruh setup awal aplikasi saat pertama kali dimuat ke browser.
const init = () => {
    renderFormCategories();
    renderFilterCategories();
    renderApp();
};

init();