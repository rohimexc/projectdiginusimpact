// Array utama tempat menyimpan daftar seluruh objek tugas di memori
let tasks = [];

// Variabel penanda status filter yang sedang aktif ('semua', 'pending', 'selesai')
let filter = 'semua';

// Variabel penampung timer untuk durasi penayangan notifikasi toast
let toastTimeout;

// Mengambil elemen HTML input teks tugas berdasarkan ID
const taskInput = document.getElementById('taskInput');

// Mengambil elemen HTML tombol tambah berdasarkan ID
const addBtn = document.getElementById('addBtn');

// Mengambil elemen HTML wadah daftar ul berdasarkan ID
const taskList = document.getElementById('taskList');

// Mengambil elemen HTML statistik angka total berdasarkan ID
const statTotal = document.getElementById('statTotal');

// Mengambil elemen HTML statistik angka selesai berdasarkan ID
const statCompleted = document.getElementById('statCompleted');

// Mengambil elemen HTML statistik angka pending berdasarkan ID
const statPending = document.getElementById('statPending');

// Mengambil seluruh elemen tombol filter berdasarkan class
const filterBtns = document.querySelectorAll('.filter-btn');

// Mengambil elemen HTML wadah toast notifikasi berdasarkan ID
const toast = document.getElementById('toast');

// Mengambil elemen HTML teks pesan toast berdasarkan ID
const toastMsg = document.getElementById('toastMsg');

// Mengambil elemen HTML ikon toast berdasarkan ID
const toastIcon = document.getElementById('toastIcon');

// Menambahkan event listener klik pada tombol tambah tugas
addBtn.addEventListener('click', addTask);

// Menambahkan event listener saat menekan tombol pada input teks
taskInput.addEventListener('keypress', (e) => {
    // Memeriksa apakah tombol yang ditekan adalah Enter
    if (e.key === 'Enter') {
        // Memanggil fungsi untuk menambah tugas baru
        addTask();
    }
});

// Memberikan event listener pada setiap tombol filter
filterBtns.forEach(btn => {
    // Menambahkan aksi ketika tombol filter diklik
    btn.addEventListener('click', () => {
        // Mengembalikan tampilan seluruh tombol filter ke style non-aktif
        filterBtns.forEach(b => b.className = 'filter-btn flex-1 py-1.5 rounded-lg transition');
        // Memberikan style aktif pada tombol filter yang sedang diklik
        btn.className = 'filter-btn flex-1 py-1.5 rounded-lg bg-white text-indigo-600 shadow-sm transition';
        // Menyimpan nilai kategori filter dari atribut data-filter
        filter = btn.dataset.filter;
        // Memperbarui tampilan daftar tugas di layar
        render();
    });
});

// Fungsi untuk menampilkan pop-up notifikasi toast
function showToast(message, iconClass = 'fa-circle-check text-emerald-400') {
    // Menghentikan timer notifikasi sebelumnya jika masih aktif
    clearTimeout(toastTimeout);
    // Memasukkan teks pesan ke elemen toast
    toastMsg.textContent = message;
    // Mengganti kelas ikon toast sesuai jenis notifikasi
    toastIcon.className = `fa-solid ${iconClass}`;
    // Menampilkan toast dengan menghapus kelas tersembunyi
    toast.classList.remove('opacity-0', 'translate-y-[-10px]', 'pointer-events-none');
    // Menambahkan kelas animasi muncul
    toast.classList.add('opacity-100', 'translate-y-0');

    // Mengatur timer untuk menyembunyikan toast setelah 2,5 detik
    toastTimeout = setTimeout(() => {
        // Menghapus kelas tampilan muncul
        toast.classList.remove('opacity-100', 'translate-y-0');
        // Menambahkan kembali kelas tersembunyi
        toast.classList.add('opacity-0', 'translate-y-[-10px]', 'pointer-events-none');
    }, 2500);
}

// Fungsi untuk menambah tugas baru ke dalam array
function addTask() {
    // Mengambil string input dan menghapus spasi di awal/akhir
    const text = taskInput.value.trim();
    // Menghentikan fungsi jika input kosong
    if (!text) return;

    // Memasukkan objek tugas baru ke dalam array 'tasks'
    tasks.push({
        // Menghasilkan ID unik berdasarkan timestamp
        id: Date.now(),
        // Teks tugas dari input
        text: text,
        // Status awal tugas belum selesai
        completed: false
    });

    // Mengosongkan kembali kolom input teks
    taskInput.value = '';
    // Menampilkan notifikasi sukses menambah tugas
    showToast('Berhasil menambahkan tugas!');
    // Memperbarui tampilan daftar di layar
    render();
}

// Fungsi untuk mengubah status centang selesai/belum pada tugas
function toggleTask(id) {
    // Mencari objek tugas berdasarkan ID di dalam array
    const task = tasks.find(t => t.id === id);
    // Memeriksa apakah tugas ditemukan
    if (task) {
        // Membalik status boolean completed
        task.completed = !task.completed;
        // Memeriksa status terbaru untuk menentukan pesan toast
        if (task.completed) {
            // Tampilkan notifikasi jika tugas selesai
            showToast('Tugas telah selesai!', 'fa-circle-check text-emerald-400');
        } else {
            // Tampilkan notifikasi jika tugas dikembalikan ke pending
            showToast('Tugas dikembalikan ke pending', 'fa-circle-info text-amber-400');
        }
    }
    // Memperbarui tampilan daftar di layar
    render();
}

// Fungsi untuk menghapus tugas dari array berdasarkan ID
function deleteTask(id) {
    // Menyaring array untuk membuang elemen dengan ID yang sesuai
    tasks = tasks.filter(t => t.id !== id);
    // Menampilkan notifikasi sukses menghapus tugas
    showToast('Tugas berhasil dihapus!', 'fa-trash-can text-rose-400');
    // Memperbarui tampilan daftar di layar
    render();
}

// Fungsi untuk menghitung dan memperbarui indikator statistik
function updateStats() {
    // Menghitung jumlah total seluruh tugas di array
    const total = tasks.length;
    // Menghitung jumlah tugas yang statusnya selesai
    const completed = tasks.filter(t => t.completed).length;
    // Menghitung jumlah tugas yang masih pending
    const pending = total - completed;

    // Memperbarui teks total di HTML
    statTotal.textContent = total;
    // Memperbarui teks selesai di HTML
    statCompleted.textContent = completed;
    // Memperbarui teks pending di HTML
    statPending.textContent = pending;
}

// Fungsi utama untuk merender elemen daftar tugas ke layar
function render() {
    // Mengosongkan elemen ul sebelum memasukkan data baru
    taskList.innerHTML = '';
    
    // Menyaring array tasks berdasarkan filter yang sedang aktif
    const filtered = tasks.filter(t => {
        // Jika filter 'completed', tampilkan yang selesai saja
        if (filter === 'completed') return t.completed;
        // Jika filter 'pending', tampilkan yang belum selesai saja
        if (filter === 'pending') return !t.completed;
        // Jika filter 'all', tampilkan semua tugas
        return true;
    });

    // Memeriksa jika daftar tugas yang difilter kosong
    if (!filtered.length) {
        // Menampilkan pesan kosong di dalam list
        taskList.innerHTML = `<li class="text-center text-xs text-slate-400 py-4">Tidak ada tugas</li>`;
    } else {
        // Melakukan iterasi untuk setiap objek tugas yang lolos filter
        filtered.forEach(t => {
            // Membuat elemen li baru
            const li = document.createElement('li');
            // Menentukan kelas Tailwind pada li berdasarkan status completed
            li.className = `flex items-center justify-between p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm transition ${t.completed ? 'opacity-50' : ''}`;
            // Memasukkan struktur HTML ke dalam baris li
            li.innerHTML = `
                <div class="flex items-center gap-2.5 cursor-pointer overflow-hidden flex-1" onclick="toggleTask(${t.id})">
                    <div class="w-4 h-4 rounded-full border border-slate-400 flex items-center justify-center shrink-0 ${t.completed ? 'bg-indigo-600 border-indigo-600 text-white' : ''}">
                        ${t.completed ? '<i class="fa-solid fa-check text-[9px]"></i>' : ''}
                    </div>
                    <span class="truncate ${t.completed ? 'line-through text-slate-400' : ''}">${escapeHTML(t.text)}</span>
                </div>
                <button onclick="deleteTask(${t.id})" class="text-slate-400 hover:text-rose-500 p-1 transition" title="Hapus">
                    <i class="fa-solid fa-trash-can text-xs"></i>
                </button>
            `;
            // Memasukkan elemen li ke dalam wadah taskList
            taskList.appendChild(li);
        });
    }

    // Memperbarui indikator angka statistik
    updateStats();
}

// Fungsi helper untuk mencegah potensi celah keamanan XSS (Cross-Site Scripting)
function escapeHTML(str) {
    // Membuat elemen div temporer di memori
    const div = document.createElement('div');
    // Memasukkan string ke textContent agar aman dari injeksi script
    div.textContent = str;
    // Mengembalikan string yang sudah ter-encode dengan aman
    return div.innerHTML;
}

// Memanggil render pertama kali saat file script selesai dimuat
render();