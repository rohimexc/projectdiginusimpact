/**
 * =========================================================================
 * 1. MANAJEMEN STATE (Penyimpanan Data di Memori Aplikasi)
 * =========================================================================
 */

// Kumpulan daftar kategori yang dipisah berdasarkan tipe transaksi
// Struktur objek ini memudahkan pemanggilan kategori secara dinamis sesuai pilihan select type
const categories = {
    expense: ['Makanan & Minuman', 'Transportasi', 'Belanja', 'Tagihan', 'Hiburan', 'Lainnya'],
    income: ['Gaji', 'Uang Saku', 'Bonus', 'Investasi', 'Penjualan', 'Lainnya']
};

// Mengambil data dari localStorage saat browser dibuka pertama kali
// JSON.parse mengubah teks string berformat JSON kembali menjadi Array of Objects JS
// Menggunakan operator || [] agar jika penyimpanan masih kosong (null), variabel tetap berupa array kosong
let transactions = JSON.parse(localStorage.getItem('transactions_data')) || [];


/**
 * =========================================================================
 * 2. SELEKSI ELEMEN DOM
 * =========================================================================
 * Mengambil referensi elemen HTML menggunakan getElementById untuk efisiensi performa seleksi
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
const errorMessage = document.getElementById('error-message');

const searchInput = document.getElementById('search-input');
const filterType = document.getElementById('filter-type');
const filterCategory = document.getElementById('filter-category');
const transactionRows = document.getElementById('transaction-rows');
const emptyState = document.getElementById('empty-state');
const loading = document.getElementById('loading');


/**
 * =========================================================================
 * 3. LOGIKA PERSISTENSI DATA (localStorage & Error Handling)
 * =========================================================================
 */

// Menyimpan seluruh array transaksi ke localStorage
// Menggunakan try...catch untuk mengantisipasi storage browser penuh (quota exceeded)
const syncLocalStorage = () => {
    try {
        localStorage.setItem('transactions_data', JSON.stringify(transactions));
    } catch (err) {
        showError('Gagal menyimpan data ke penyimpanan lokal browser.');
    }
};


/**
 * =========================================================================
 * 4. FUNGSI FORMAT MATA UANG
 * =========================================================================
 */
const formatRp = (num) => {
    // Math.abs memastikan angka input selalu positif sebelum diformat
    const absoluteNum = Math.abs(num);
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(absoluteNum);
};


/**
 * =========================================================================
 * 5. MERENDER OPSI KATEGORI PADA FORM & FILTER
 * =========================================================================
 */

// Memperbarui isi dropdown kategori pada form input berdasarkan jenis yang aktif (income/expense)
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

// Menggabungkan seluruh kategori unik (gabungan expense dan income) ke dropdown filter
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
    // Array.reduce mengakumulasikan nilai amount dari array transaksi bertipe 'income'
    const income = transactions
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    // Array.reduce mengakumulasikan nilai amount dari transaksi bertipe 'expense'
    const expense = transactions
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    const total = income - expense;

    // Memperbarui UI tampilan saldo dengan format mata uang rupiah
    balance.innerText = formatRp(total);
    moneyPlus.innerText = `+ ${formatRp(income)}`;
    moneyMinus.innerText = `- ${formatRp(expense)}`;
};


/**
 * =========================================================================
 * 7. MEMBUAT BARIS TABEL TRANSAKSI (Manipulasi DOM)
 * =========================================================================
 */
const createRowDOM = (transaction) => {
    const isIncome = transaction.type === 'income';
    const sign = isIncome ? '+' : '-';
    const textBadgeColor = isIncome ? 'text-emerald-700 bg-emerald-50' : 'text-rose-700 bg-rose-50';

    const tr = document.createElement('tr');
    tr.className = 'hover:bg-slate-50/80 transition-colors';
    tr.dataset.id = transaction.id;

    tr.innerHTML = `
        <td class="p-3">
            <span class="inline-block px-2.5 py-1 text-xs font-semibold rounded-md ${textBadgeColor}">
                ${transaction.category}
            </span>
        </td>
        <td class="p-3 font-medium text-slate-700">
            ${transaction.desc || '-'}
        </td>
        <td class="p-3 text-right font-bold ${isIncome ? 'text-emerald-600' : 'text-rose-600'}">
            ${sign} ${formatRp(transaction.amount)}
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


/**
 * =========================================================================
 * 8. MENAMPILKAN DATA DENGAN ASYNC LOADING STATE & FILTER
 * =========================================================================
 */
const renderTable = async () => {
    // Menampilkan indikator loading untuk memberikan feedback visual pada proses komputasi
    loading.classList.remove('hidden');
    transactionRows.innerHTML = '';
    emptyState.classList.add('hidden');

    // Menggunakan Promise simulasi delay (100ms) untuk demonstrasi async processing
    await new Promise(resolve => setTimeout(resolve, 100));

    // Ekstraksi nilai filter pencarian
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedType = filterType.value;
    const selectedCat = filterCategory.value;

    // Filter multi-kriteria: mencari kecocokan tipe, kategori, dan deskripsi teks
    const filtered = transactions.filter(t => {
        const matchesType = (selectedType === 'all') || (t.type === selectedType);
        const matchesCat = (selectedCat === 'all') || (t.category === selectedCat);
        const matchesSearch = (t.desc || '').toLowerCase().includes(searchTerm) || 
                              t.category.toLowerCase().includes(searchTerm);

        return matchesType && matchesCat && matchesSearch;
    });

    loading.classList.add('hidden');

    // Menampilkan empty state bila tidak ada data transaksi yang cocok
    if (filtered.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }

    // Memasukkan setiap baris data hasil filter ke tabel DOM
    filtered.forEach(item => {
        transactionRows.appendChild(createRowDOM(item));
    });
};


/**
 * =========================================================================
 * 9. VALIDASI FORM & ERROR HANDLING
 * =========================================================================
 */
const showError = (msg) => {
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
};

const hideError = () => {
    errorMessage.textContent = '';
    errorMessage.classList.add('hidden');
};

const resetFormState = () => {
    form.reset();
    editIdInput.value = '';
    formTitle.textContent = 'Tambah Transaksi Baru';
    submitBtn.textContent = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
    hideError();
    renderCategories();
};


/**
 * =========================================================================
 * 10. CRUD: UPDATE & DELETE
 * =========================================================================
 */

// Memasukkan data transaksi yang dipilih kembali ke form untuk diedit
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
    hideError();
};

// Menghapus data transaksi berdasarkan id unik
const deleteTransaction = (id) => {
    transactions = transactions.filter(t => t.id !== id);
    syncLocalStorage();
    updateValues();
    renderTable();
};


/**
 * =========================================================================
 * 11. EVENT LISTENERS
 * =========================================================================
 */

// 1. Dropdown Type: Render ulang dropdown kategori saat jenis pengeluaran/pemasukan diganti
typeSelect.addEventListener('change', renderCategories);

// 2. Form Submit: Menangani penambahan data baru atau pembaruan data yang sudah ada
form.addEventListener('submit', (e) => {
    e.preventDefault();
    hideError();

    const amountVal = parseFloat(amountInput.value);
    const descVal = descInput.value.trim();

    // Validasi nilai nominal agar tidak bernilai negatif, nol, atau kosong
    if (isNaN(amountVal) || amountVal <= 0) {
        showError('Nominal transaksi harus berupa angka lebih besar dari 0!');
        return;
    }

    const editId = editIdInput.value;

    if (editId) {
        // Mode Edit: Mencari transaksi lama lalu memperbarui nilainya
        const index = transactions.findIndex(t => t.id === Number(editId));
        if (index !== -1) {
            transactions[index] = {
                ...transactions[index],
                type: typeSelect.value,
                category: categorySelect.value,
                desc: descVal,
                amount: amountVal
            };
        }
    } else {
        // Mode Tambah Baru: Buat objek transaksi dengan identifier ID unik berbasis timestamp
        const newTransaction = {
            id: Date.now(),
            type: typeSelect.value,
            category: categorySelect.value,
            desc: descVal,
            amount: amountVal
        };
        // Menambahkan transaksi baru ke urutan pertama array (unshift)
        transactions.unshift(newTransaction);
    }

    syncLocalStorage();
    updateValues();
    renderTable();
    resetFormState();
});

// 3. Tombol Batal Edit: Mengembalikan form ke mode tambah baru
cancelEditBtn.addEventListener('click', resetFormState);

// 4. Event Delegation pada Tabel untuk Tombol Edit dan Hapus
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

// 5. Input Filter dan Search: Merender ulang tabel saat filter berubah
searchInput.addEventListener('input', renderTable);
filterType.addEventListener('change', renderTable);
filterCategory.addEventListener('change', renderTable);


/**
 * =========================================================================
 * 12. INISIALISASI AWAL
 * =========================================================================
 */
const initApp = () => {
    renderCategories();
    renderFilterCategoryOptions();
    updateValues();
    renderTable();
};

initApp();