/**
 * =========================================================================
 * 1. MANAJEMEN STATE & PENYIMPANAN DATA
 * =========================================================================
 */

// Objek master berisi daftar kategori default untuk pemasukan dan pengeluaran.
// Digunakan untuk mengisi opsi dropdown form dan filter secara dinamis.
const categories = {
    expense: ['Makanan & Minuman', 'Transportasi', 'Belanja', 'Tagihan', 'Hiburan', 'Lainnya'],
    income: ['Gaji', 'Uang Saku', 'Bonus', 'Investasi', 'Penjualan', 'Lainnya']
};

// menyimpan data transaksi ke dalam localstorage
let transactions = JSON.parse(localStorage.getItem('transactions_data')) || [];


// variable ini berguna untuk chart.js agar kita bisa memanggil update dan saat data berubah 
// kita tidak perlu menghapus dan membuat carth dari awal
let comparisonChartInstance = null;
let incomeChartInstance = null;
let expenseChartInstance = null;


/**
 * =========================================================================
 * 2. SELEKSI ELEMEN DOM
 * =========================================================================
 * Menghubungkan elemen HTML ke variabel JavaScript menggunakan getElementById
 * agar nilainya bisa dibaca, diubah teksnya, atau diberi event listener.
 */

// Elemen penampil total ringkasan saldo, pemasukan, dan pengeluaran
const balance = document.getElementById('balance');
const moneyPlus = document.getElementById('money-plus');
const moneyMinus = document.getElementById('money-minus');

// Elemen formulir transaksi ,kolom input dan tombol aksinya
const form = document.getElementById('form');
const formTitle = document.getElementById('form-title');
const editIdInput = document.getElementById('edit-id');
const typeSelect = document.getElementById('type');
const categorySelect = document.getElementById('category');
const descInput = document.getElementById('desc');
const amountInput = document.getElementById('amount');
const submitBtn = document.getElementById('submit-btn');
const cancelEditBtn = document.getElementById('cancel-edit-btn');

// Elemen fitur filter, pencarian, dan kontainer tabel data
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
 * Fungsi untuk menyimpan data ke localstorge jika di ripres data masih
 */
const syncLocalStorage = () => {
    try {
        // Mengubah array objek JavaScript menjadi format teks JSON agar bisa disimpan di localStorage
        localStorage.setItem('transactions_data', JSON.stringify(transactions));
    } catch (error) {
        // Blok pengaman jika memori browser penuh atau akses ditolak oleh browser
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
 * Fungsi pembantu (utility) untuk mengubah angka biasa menjadi format Rupiah.
 */
const formatRp = (num) => {
    // Intl.NumberFormat bawaan JS untuk memformat angka sesuai standar mata uang Indonesia (IDR)
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0 // Menghilangkan angka desimal koma nol di belakang
    }).format(Math.abs(num)); // Math.abs memastikan angka selalu positif sebelum diberi simbol +/-
};


/**
 * =========================================================================
 * 5. PENGATURAN DROPDOWN KATEGORI
 * =========================================================================
 * Mengatur isi pilihan kategori agar berubah otomatis tergantung tipe transaksi.
 */

// Mengisi dropdown kategori pada FORMULIR berdasarkan jenis yang dipilih (income/expense)
const renderCategories = () => {
    categorySelect.innerHTML = ''; // Mengosongkan opsi lama
    const currentList = categories[typeSelect.value] || []; // Ambil array kategori yang cocok

    // Membuat elemen <option> satu per satu lalu menempelkannya ke dalam <select>
    currentList.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
};

// Mengisi dropdown kategori pada FILTER TABEL dengan menggabungkan semua kategori unik
const renderFilterCategoryOptions = () => {
    filterCategory.innerHTML = '<option value="all">Semua Kategori</option>';
    // Menggunakan new Set() untuk memastikan tidak ada nama kategori yang duplikat
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
 * Menghitung akumulasi pemasukan, pengeluaran, dan saldo bersih secara real-time.
 */
const updateValues = () => {
    // Menghitung total semua pemasukan menggunakan metode .filter() lalu .reduce()
    const income = transactions
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    // Menghitung total semua pengeluaran
    const expense = transactions
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    // Saldo bersih adalah selisih total pemasukan dikurangi pengeluaran
    const total = income - expense;

    // Memperbarui tampilan angka di card statistik dashboard
    balance.innerText = formatRp(total);
    moneyPlus.innerText = `+ ${formatRp(income)}`;
    moneyMinus.innerText = `- ${formatRp(expense)}`;
};


/**
 * =========================================================================
 * 7. VISUALISASI CHART.JS (BAR & DUA PIE CHART)
 * =========================================================================
 * Mengagregasi data transaksi dan menampilkannya dalam bentuk grafik visual.
 */

// Helper: Menghitung total uang per kategori untuk Pie Chart (berdasarkan 'income' / 'expense')
const getCategoryDataByType = (type) => {
    // 1. Saring transaksi sesuai tipenya saja
    const filteredData = transactions.filter(t => t.type === type);
    // 2. Ambil daftar kategori yang benar-benar ada transaksinya (tanpa duplikat)
    const categoryLabels = [...new Set(filteredData.map(t => t.category))];

    // 3. Jumlahkan total nominal uang untuk tiap-tiap kategori tersebut
    const categoryTotals = categoryLabels.map(cat => {
        return filteredData
            .filter(t => t.category === cat)
            .reduce((acc, t) => acc + t.amount, 0);
    });

    // Kembalikan label & data. Jika belum ada data, beri label fallback default
    return {
        labels: categoryLabels.length > 0 ? categoryLabels : ['Belum Ada Data'],
        data: categoryTotals.length > 0 ? categoryTotals : [0]
    };
};

// Helper: Menghitung total pemasukan vs total pengeluaran untuk Bar Chart
const getIncomeVsExpenseData = () => {
    const totalIncome = transactions
        .filter(t => t.type === 'income')
        .reduce((acc, t) => acc + t.amount, 0);

    const totalExpense = transactions
        .filter(t => t.type === 'expense')
        .reduce((acc, t) => acc + t.amount, 0);

    return [totalIncome, totalExpense];
};

// Palet warna untuk Pie Chart pemasukan (nuansa hijau) dan pengeluaran (nuansa cerah/rose)
const incomeColors = ['#10b981', '#34d399', '#059669', '#6ee7b7', '#047857', '#a7f3d0'];
const expenseColors = ['#f43f5e', '#fb923c', '#facc15', '#a855f7', '#06b6d4', '#64748b'];

// Fungsi inisialisasi awal pembuatan ketiga chart saat aplikasi dimuat
const initCharts = () => {
    // 1. Bar Chart: Perbandingan Arus Kas (Pemasukan vs Pengeluaran)
    const ctxComparison = document.getElementById('comparisonChart').getContext('2d');
    comparisonChartInstance = new Chart(ctxComparison, {
        type: 'bar',
        data: {
            labels: ['Pemasukan', 'Pengeluaran'],
            datasets: [{
                label: 'Total Nominal (Rp)',
                data: getIncomeVsExpenseData(),
                backgroundColor: ['#10b981', '#f43f5e'],
                borderRadius: 8 // Membuat ujung batang grafik melengkung halus
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false } // Legend disembunyikan karena label sumbu X sudah jelas
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        // Mengubah angka sumbu Y menjadi format mata uang Rupiah
                        callback: (value) => 'Rp ' + value.toLocaleString('id-ID')
                    }
                }
            }
        }
    });

    // 2. Pie Chart: Rincian Kategori Pemasukan
    const ctxIncome = document.getElementById('incomeCategoryChart').getContext('2d');
    const incomeData = getCategoryDataByType('income');
    incomeChartInstance = new Chart(ctxIncome, {
        type: 'pie',
        data: {
            labels: incomeData.labels,
            datasets: [{
                data: incomeData.data,
                backgroundColor: incomeColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' } // Posisi label kategori di bawah grafik
            }
        }
    });

    // 3. Pie Chart: Rincian Kategori Pengeluaran
    const ctxExpense = document.getElementById('expenseCategoryChart').getContext('2d');
    const expenseData = getCategoryDataByType('expense');
    expenseChartInstance = new Chart(ctxExpense, {
        type: 'pie',
        data: {
            labels: expenseData.labels,
            datasets: [{
                data: expenseData.data,
                backgroundColor: expenseColors,
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
};

// Fungsi krusial: Memperbarui visual chart setiap kali ada data yang ditambah, diedit, atau dihapus
const updateCharts = () => {
    // Pengaman: Jika chart belum siap, jangan lakukan apa-apa
    if (!comparisonChartInstance || !incomeChartInstance || !expenseChartInstance) return;

    // Perbarui data Bar Chart lalu jalankan animasi update
    comparisonChartInstance.data.datasets[0].data = getIncomeVsExpenseData();
    comparisonChartInstance.update();

    // Perbarui data Pie Chart Pemasukan
    const incData = getCategoryDataByType('income');
    incomeChartInstance.data.labels = incData.labels;
    incomeChartInstance.data.datasets[0].data = incData.data;
    incomeChartInstance.update();

    // Perbarui data Pie Chart Pengeluaran
    const expData = getCategoryDataByType('expense');
    expenseChartInstance.data.labels = expData.labels;
    expenseChartInstance.data.datasets[0].data = expData.data;
    expenseChartInstance.update();
};


/**
 * =========================================================================
 * 8. MANIPULASI DOM TABEL & ASYNC LOADING
 * =========================================================================
 * Mengelola pembuatan baris data tabel, efek animasi loading, dan filter data.
 */

// Helper membuat elemen <tr> tabel untuk tiap satu data transaksi
const createRowDOM = (item) => {
    const isIncome = item.type === 'income';
    const sign = isIncome ? '+' : '-';
    // Memberi warna badge dan teks (hijau jika income, merah jika expense)
    const badgeColor = isIncome ? 'text-emerald-700 bg-emerald-50' : 'text-rose-700 bg-rose-50';

    const tr = document.createElement('tr');
    tr.className = 'hover:bg-slate-50/80 transition-colors';
    tr.dataset.id = item.id; // Menyimpan ID transaksi pada atribut HTML untuk kemudahan edit/hapus

    tr.innerHTML = `
        <td class="p-4">
            <span class="inline-block px-2.5 py-1 text-xs font-semibold rounded-md ${badgeColor}">
                ${item.category}
            </span>
        </td>
        <td class="p-4 font-medium text-slate-700">
            ${item.desc || '-'}
        </td>
        <td class="p-4 text-right font-bold ${isIncome ? 'text-emerald-600' : 'text-rose-600'}">
            ${sign} ${formatRp(item.amount)}
        </td>
        <td class="p-4 text-center space-x-1">
            <button class="edit-btn text-xs bg-amber-50 hover:bg-amber-100 text-amber-700 font-semibold px-2.5 py-1 rounded transition">
                Edit
            </button>
            <button class="delete-btn text-xs bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold px-2.5 py-1 rounded transition">
                Hapus
            </button>
        </td>
    `;
    return tr;
};

// Fungsi render tabel dengan filter pencarian dan efek loading simulasi
const renderTable = async () => {
    loading.classList.remove('hidden'); // Munculkan indikator loading
    transactionRows.innerHTML = '';      // Bersihkan isi tabel lama
    emptyState.classList.add('hidden');  // Sembunyikan state kosong

    // Jeda simulasi 80 milidetik agar transisi update data terasa interaktif dan halus
    await new Promise(resolve => setTimeout(resolve, 80));

    // Ambil nilai kata kunci pencarian dan dropdown filter
    const searchTerm = searchInput.value.toLowerCase().trim();
    const selectedType = filterType.value;
    const selectedCat = filterCategory.value;

    // Logika penyaringan transaksi berdasarkan 3 parameter: tipe, kategori, dan kata kunci teks
    const filtered = transactions.filter(t => {
        const matchesType = (selectedType === 'all') || (t.type === selectedType);
        const matchesCat = (selectedCat === 'all') || (t.category === selectedCat);
        const matchesSearch = (t.desc || '').toLowerCase().includes(searchTerm) || 
                              t.category.toLowerCase().includes(searchTerm);

        return matchesType && matchesCat && matchesSearch;
    });

    loading.classList.add('hidden'); // Sembunyikan loading setelah data siap

    // Jika tidak ada data yang cocok dengan pencarian, tampilkan kotak Empty State
    if (filtered.length === 0) {
        emptyState.classList.remove('hidden');
        return;
    }

    // Jika data ada, render baris demi baris ke dalam tabel
    filtered.forEach(item => {
        transactionRows.appendChild(createRowDOM(item));
    });
};


/**
 * =========================================================================
 * 9. STATE & LOGIKA CRUD (CREATE, READ, UPDATE, DELETE)
 * =========================================================================
 * Mengatur alur penambahan, perubahan, pembatalan, dan penghapusan data transaksi.
 */

// (mode Tambah Baru)
const resetFormState = () => {
    form.reset();
    editIdInput.value = '';
    formTitle.textContent = 'Tambah Transaksi Baru';
    submitBtn.textContent = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
    renderCategories();
};

// Memulai mode edit:
const startEditTransaction = (id) => {
    const item = transactions.find(t => t.id === id);
    if (!item) return;

    // Isi formulir dengan data transaksi yang dipilih
    editIdInput.value = item.id;
    typeSelect.value = item.type;
    renderCategories(); // Perbarui opsi dropdown sesuai tipenya
    categorySelect.value = item.category;
    descInput.value = item.desc || '';
    amountInput.value = item.amount;

    // Ubah teks form dan munculkan tombol 'Batal'
    formTitle.textContent = 'Edit Transaksi';
    submitBtn.textContent = 'Perbarui Transaksi';
    cancelEditBtn.classList.remove('hidden');

    // Geser scroll layar dengan halus menuju ke formulir
    window.scrollTo({ top: form.offsetTop - 20, behavior: 'smooth' });
};

// Menghapus data transaksi dengan dialog konfirmasi SweetAlert2
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
        // Cek jika pengguna mengklik tombol 'Ya, Hapus!'
        if (result.isConfirmed) {
            // Saring array: buang transaksi yang memiliki ID tersebut
            transactions = transactions.filter(t => t.id !== id);

            // Sinkronkan ke database browser, hitung ulang saldo, update grafik, dan render tabel
            syncLocalStorage();
            updateValues();
            updateCharts();
            renderTable();

            // Notifikasi berhasil terhapus
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
 * Menangkap setiap interaksi pengguna seperti klik, input ketikan, dan submit.
 */

// Perbarui opsi kategori otomatis saat dropdown Jenis (Pemasukan/Pengeluaran) diubah
typeSelect.addEventListener('change', renderCategories);

// Tangani submit formulir (bisa berupa Simpan Baru atau Simpan Pembaruan)
form.addEventListener('submit', (e) => {
    e.preventDefault(); // Mencegah reload halaman bawaan form HTML

    const amountVal = parseFloat(amountInput.value);
    const descVal = descInput.value.trim();

    // 1. Validasi Kolom Keterangan: Wajib diisi (tidak boleh kosong)
    if (descVal === '') {
        Swal.fire({
            icon: 'error',
            title: 'Validasi Gagal',
            text: 'Keterangan transaksi wajib diisi!'
        });
        descInput.focus();
        return;
    }

    // 2. Validasi Kolom Nominal: Harus berupa angka dan harus lebih besar dari nol
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
        // --- MODE UPDATE (EDIT DATA YANG SUDAH ADA) ---
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
        // --- MODE CREATE (TAMBAH DATA TRANSAKSI BARU) ---
        const newTransaction = {
            id: Date.now(), // Menggunakan timestamp milidetik saat ini sebagai ID unik
            type: typeSelect.value,
            category: categorySelect.value,
            desc: descVal,
            amount: amountVal
        };
        // unshift() memasukkan data baru ke urutan paling pertama (paling atas)
        transactions.unshift(newTransaction);

        Swal.fire({
            icon: 'success',
            title: 'Berhasil',
            text: 'Transaksi berhasil ditambahkan!',
            timer: 1500,
            showConfirmButton: false
        });
    }

    // setiap ripres data akan tersimpan dikodigan 4 di bawah
    syncLocalStorage();
    updateValues();
    updateCharts();
    renderTable();
    resetFormState(); // Kembalikan form ke status bersih
});

// Event klik tombol 'Batal' saat sedang mengedit
cancelEditBtn.addEventListener('click', resetFormState);

// Event Delegation pada tabel: Mendeteksi apakah yang diklik tombol Hapus atau Edit
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

// Event listener pencarian dan filter tabel secara otomatis/instan
searchInput.addEventListener('input', renderTable);
filterType.addEventListener('change', renderTable);
filterCategory.addEventListener('change', renderTable);


/**
 * =========================================================================
 * 11. BOOTSTRAP INISIALISASI APLIKASI
 * =========================================================================
 * Pintu masuk utama: Dijalankan otomatis saat file JS pertama kali terbaca.
 */
const initApp = () => {
    renderCategories();             // 1. Siapkan opsi kategori formulir
    renderFilterCategoryOptions();   // 2. Siapkan opsi kategori filter
    updateValues();                  // 3. Hitung saldo awal dari localStorage
    initCharts();                    // 4. Bangun ketiga canvas Chart.js
    renderTable();                   // 5. Gambar isi baris tabel transaksi
};

initApp();