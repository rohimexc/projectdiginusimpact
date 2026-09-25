// Mendapatkan elemen input teks tugas dari DOM berdasarkan ID-nya
const taskInput = document.getElementById('taskInput');
// Mendapatkan elemen tombol tambah tugas dari DOM berdasarkan ID-nya
const addTaskBtn = document.getElementById('addTaskBtn');
// Mendapatkan elemen kontainer tubuh tabel (tbody) daftar tugas dari DOM
const taskList = document.getElementById('taskList');
// Mendapatkan elemen untuk menampilkan statistik total tugas
const totalTasksEl = document.getElementById('totalTasks');
// Mendapatkan elemen untuk menampilkan statistik tugas selesai
const completedTasksEl = document.getElementById('completedTasks');
// Mendapatkan semua elemen tombol filter berdasarkan kelasnya
const filterBtns = document.querySelectorAll('.filter-btn');

// Mendefinisikan array utama untuk menyimpan seluruh data objek tugas
let tasks = [];
// Mendefinisikan variabel untuk melacak status filter yang sedang aktif
let currentFilter = 'all';

// Membuat fungsi utama untuk memperbarui tampilan antarmuka (UI) di layar
function renderTasks() {
    // Mengosongkan isi kontainer tabel tugas sebelum merender ulang
    taskList.innerHTML = '';
    // Menyaring array tasks berdasarkan status filter yang sedang aktif
    const filteredTasks = tasks.filter(function(task) {
        // Jika filter 'completed', ambil tugas yang status completed-nya true
        if (currentFilter === 'completed') return task.completed;
        // Jika filter 'active', ambil tugas yang status completed-nya false
        if (currentFilter === 'active') return !task.completed;
        // Jika filter 'all', ambil seluruh tugas tanpa terkecuali
        return true;
    });
    // Melakukan perulangan untuk setiap tugas yang sudah disaring
    filteredTasks.forEach(function(task) {
        // Membuat elemen baris tabel baru berupa tr
        const tr = document.createElement('tr');
        // Menambahkan kelas Tailwind CSS agar baris tabel terlihat rapi saat kursor mendekat
        tr.className = 'hover:bg-gray-50 transition';
        // Mengatur isi kolom HTML di dalam baris tabel menggunakan template literal
        tr.innerHTML = `
            <td class="p-3 text-center">
                <input type="checkbox" ${task.completed ? 'checked' : ''} onclick="confirmToggle(${task.id}, event)" class="w-4 h-4 text-indigo-600 rounded cursor-pointer">
            </td>
            <td class="p-3 ${task.completed ? 'line-through text-gray-400' : 'text-gray-700'} font-medium">
                ${task.text}
            </td>
            <td class="p-3 text-right">
                <button onclick="confirmDelete(${task.id})" class="px-2.5 py-1 text-xs text-red-600 bg-red-50 rounded hover:bg-red-100 transition font-medium">Hapus</button>
            </td>
        `;
        // Memasukkan baris tabel tugas ke dalam elemen tbody di DOM
        taskList.appendChild(tr);
    });
    // Memanggil fungsi untuk memperbarui angka statistik di layar
    updateStats();
}

// Membuat fungsi untuk menambahkan tugas baru ke dalam array
function addTask() {
    // Mengambil teks dari input dan membuang spasi kosong di awal/akhir
    const text = taskInput.value.trim();
    // Memeriksa apakah input kosong atau tidak, jika kosong hentikan fungsi
    if (text === '') return;
    // Membuat objek tugas baru dengan ID unik berdasarkan waktu, teks, dan status awal false
    const newTask = { id: Date.now(), text: text, completed: false };
    // Memasukkan objek tugas baru ke dalam array tasks
    tasks.push(newTask);
    // Mengosongkan kembali kolom input teks tugas di layar
    taskInput.value = '';
    // Memunculkan pop-up alert sederhana saat tugas berhasil ditambahkan
    alert('Berhasil: Tugas baru telah ditambahkan ke daftar!');
    // Memanggil fungsi renderTasks untuk memperbarui tampilan daftar tugas
    renderTasks();
}

// Membuat fungsi konfirmasi sebelum mencentang/mengubah status tugas
function confirmToggle(id, event) {
    // Mencegah perubahan checkbox secara langsung sebelum user menekan OK pada konfirmasi
    event.preventDefault();
    // Memunculkan kotak dialog konfirmasi pilihan OK / Tidak
    const userConfirmed = confirm('Apakah Anda yakin ingin mengubah status selesai tugas ini?');
    // Memeriksa apakah user menekan tombol OK
    if (userConfirmed) {
        // Mencari tugas di dalam array berdasarkan ID yang cocok
        const task = tasks.find(function(t) { return t.id === id; });
        // Memeriksa apakah tugas ditemukan di dalam array
        if (task) {
            // Membalik status nilai boolean completed
            task.completed = !task.completed;
            // Memperbarui tampilan layar setelah status berubah
            renderTasks();
        }
    } else {
        // Jika user memilih Batal, kembalikan posisi centang ke kondisi semula
        renderTasks();
    }
}

// Membuat fungsi konfirmasi sebelum menghapus tugas
function confirmDelete(id) {
    // Memunculkan kotak dialog konfirmasi pilihan OK / Tidak
    const userConfirmed = confirm('Apakah Anda yakin ingin menghapus tugas ini?');
    // Memeriksa apakah user menekan tombol OK
    if (userConfirmed) {
        // Menyaring array tasks untuk membuang tugas yang memiliki ID yang cocok
        tasks = tasks.filter(function(t) { return t.id !== id; });
        // Memperbarui tampilan layar setelah tugas berhasil dihapus
        renderTasks();
    }
}

// Membuat fungsi untuk menghitung dan memperbarui statistik tugas
function updateStats() {
    // Menghitung jumlah total tugas yang ada di dalam array
    const total = tasks.length;
    // Menghitung jumlah tugas yang status completed-nya bernilai true
    const completed = tasks.filter(function(t) { return t.completed; }).length;
    // Menampilkan angka total tugas ke elemen HTML terkait
    totalTasksEl.textContent = total;
    // Menampilkan angka tugas selesai ke elemen HTML terkait
    completedTasksEl.textContent = completed;
}

// Menambahkan event listener ke tombol tambah tugas saat diklik
addTaskBtn.addEventListener('click', addTask);
// Menambahkan event listener ke input teks untuk mendeteksi tombol Enter
taskInput.addEventListener('keypress', function(e) {
    // Memeriksa apakah tombol yang ditekan pada keyboard adalah 'Enter'
    if (e.key === 'Enter') {
        // Menjalankan fungsi tambah tugas jika tombol Enter ditekan
        addTask();
    }
});

// Melakukan perulangan untuk setiap tombol filter yang ada
filterBtns.forEach(function(btn) {
    // Menambahkan event listener klik pada masing-masing tombol filter
    btn.addEventListener('click', function(e) {
        // Menghapus kelas latar belakang aktif dari semua tombol filter
        filterBtns.forEach(function(b) { b.classList.remove('bg-indigo-600', 'text-white'); });
        // Menambahkan kelas latar belakang aktif ke tombol filter yang sedang diklik
        e.target.classList.add('bg-indigo-600', 'text-white');
        // Mengubah nilai variabel currentFilter sesuai atribut data-filter tombol
        currentFilter = e.target.getAttribute('data-filter');
        // Memperbarui tampilan tugas berdasarkan filter yang baru dipilih
        renderTasks();
    });
});