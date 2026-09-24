/**
 * =================================================================
 * 1. STATE & STORAGE MANAGEMENT
 * =================================================================
 */
const categories = {
    income: ["Gaji", "Bonus", "Freelance", "Hadiah"],
    expense: ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan"]
};

let transactions = JSON.parse(localStorage.getItem('upgrade_transactions')) || [];

let activeFilterType = 'all';
let activeFilterCategory = 'all';
let activeSearchQuery = '';

// Variabel instance Chart.js
let expenseChartInstance = null;
let incomeExpenseChartInstance = null;

/**
 * =================================================================
 * 2. DOM SELECTION
 * =================================================================
 */
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
const saveToLocalStorage = () => {
    localStorage.setItem('upgrade_transactions', JSON.stringify(transactions));
};

/**
 * =================================================================
 * 4. RENDER FORM & FILTER KATEGORI
 * =================================================================
 */
const renderFormCategories = () => {
    categorySelect.innerHTML = '';
    categories[typeSelect.value].forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        categorySelect.appendChild(option);
    });
};

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

// Validasi Form menggunakan SweetAlert error
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

const formatRp = (num) => {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR',
        minimumFractionDigits: 0
    }).format(Math.abs(num));
};

/**
 * =================================================================
 * 5. INTEGRASI CHART.JS (DOUGHNUT & BAR CHART DINAMIS)
 * =================================================================
 */
const initCharts = () => {
    // --- Chart 1: Doughnut Pengeluaran Berdasarkan Kategori ---
    const expenseData = transactions.filter(t => t.type === 'expense');
    
    // Mengambil unique kategori dari data expense
    const expenseCategories = [...new Set(expenseData.map(t => t.category))];
    
    // Menghitung total per kategori secara dinamis
    const categoryTotals = expenseCategories.map(cat => {
        return expenseData
            .filter(t => t.category === cat)
            .reduce((sum, t) => sum + t.amount, 0);
    });

    const ctxExpense = document.getElementById('expenseCategoryChart').getContext('2d');
    if (expenseChartInstance) expenseChartInstance.destroy(); // Hancurkan instance lama sebelum update

    expenseChartInstance = new Chart(ctxExpense, {
        type: 'doughnut',
        data: {
            labels: expenseCategories.length > 0 ? expenseCategories : ['Belum ada data'],
            datasets: [{
                data: categoryTotals.length > 0 ? categoryTotals : [1],
                backgroundColor: ['#f59e0b', '#ef4444', '#10b981', '#6366f1', '#ec4899', '#3b82f6']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // --- Chart 2: Bar Chart Pemasukan vs Pengeluaran ---
    const totalIncome = transactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
    const totalExpense = transactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);

    const ctxIncomeExpense = document.getElementById('incomeExpenseChart').getContext('2d');
    if (incomeExpenseChartInstance) incomeExpenseChartInstance.destroy();

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
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
};

/**
 * =================================================================
 * 6. KALKULASI & RENDER DATATABLE
 * =================================================================
 */
const updateDashboardValues = (filteredData) => {
    const income = filteredData.filter(t => t.type === 'income').reduce((acc, t) => acc + t.amount, 0);
    const expense = filteredData.filter(t => t.type === 'expense').reduce((acc, t) => acc + t.amount, 0);
    const balance = income - expense;

    balanceEl.innerText = formatRp(balance);
    moneyPlusEl.innerText = `+ ${formatRp(income)}`;
    moneyMinusEl.innerText = `- ${formatRp(expense)}`;
};

const renderApp = () => {
    const filteredData = transactions.filter(t => {
        const matchesType = activeFilterType === 'all' || t.type === activeFilterType;
        const matchesCategory = activeFilterCategory === 'all' || t.category === activeFilterCategory;
        const matchesSearch = t.description.toLowerCase().includes(activeSearchQuery.toLowerCase());
        return matchesType && matchesCategory && matchesSearch;
    });

    datatableBody.innerHTML = '';

    if (filteredData.length === 0) {
        datatableBody.innerHTML = `
            <tr>
                <td colspan="4" class="p-8 text-center text-slate-400">Belum ada data transaksi.</td>
            </tr>
        `;
    } else {
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
                        <button data-id="${t.id}" class="edit-btn text-amber-600 hover:bg-amber-50 p-1.5 rounded text-xs font-semibold">Edit</button>
                        <button data-id="${t.id}" class="delete-btn text-rose-600 hover:bg-rose-50 p-1.5 rounded text-xs font-semibold">Hapus</button>
                    </div>
                </td>
            `;
            datatableBody.appendChild(tr);
        });
    }

    dataCountEl.innerText = `${filteredData.length} data ditampilkan`;
    updateDashboardValues(filteredData);
    initCharts(); // Perbarui grafik setiap kali render dipanggil
};

/**
 * =================================================================
 * 7. CRUD OPERATIONS DENGAN SWEETALERT
 * =================================================================
 */
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

const cancelEditMode = () => {
    editIdInput.value = '';
    form.reset();
    renderFormCategories();
    formTitleEl.innerText = 'Tambah Transaksi Baru';
    submitBtn.innerText = 'Simpan Transaksi';
    cancelEditBtn.classList.add('hidden');
};

// Konfirmasi Hapus menggunakan SweetAlert
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
typeSelect.addEventListener('change', renderFormCategories);

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const desc = descriptionInput.value;
    const amount = parseFloat(amountInput.value);

    if (!validateTransactionForm(desc, amount)) return;

    const editId = editIdInput.value;

    if (editId) {
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
        transactions.push({
            id: Date.now(),
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

cancelEditBtn.addEventListener('click', cancelEditMode);

datatableBody.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
        removeTransaction(e.target.dataset.id);
    } else if (e.target.classList.contains('edit-btn')) {
        startEditTransaction(Number(e.target.dataset.id));
    }
});

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

resetBtn.addEventListener('click', () => {
    Swal.fire({
        title: 'Reset Seluruh Data?',
        text: "Semua catatan transaksi akan dihapus permanen!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#f59e0b',
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
 * 9. INITIALIZATION
 * =================================================================
 */
const init = () => {
    renderFormCategories();
    renderFilterCategories();
    renderApp();
};

init();