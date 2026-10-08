// ==========================================
// 1. DATA INITIAL (ARRAY & OBJECT)
// ==========================================
let dataSiswa = [
  { id: 1, nama: "Ahmad", jurusan: "RPL", gender: "Laki-laki", aktif: true },
  { id: 2, nama: "Budi", jurusan: "TKJ", gender: "Laki-laki", aktif: false }
];

// Elemen DOM
const form = document.getElementById("siswaForm");
const inputNama = document.getElementById("inputNama");
const selectJurusan = document.getElementById("selectJurusan");
const checkAktif = document.getElementById("checkAktif");
const tabelSiswa = document.getElementById("tabelSiswa");

// ==========================================
// 2. EVENT LISTENERS PADA FORM & INPUT
// ==========================================

// Event 'input' pada Input Text (Real-time preview)
inputNama.addEventListener("input", function(e) {
  document.getElementById("namaPreview").innerText = "Karakter: " + e.target.value.length;
});

// Event 'change' pada Select / Option
selectJurusan.addEventListener("change", function(e) {
  console.log("Jurusan dipilih:", e.target.value);
});

// Event 'submit' pada Form
form.addEventListener("submit", function(e) {
  e.preventDefault(); // Mencegah reload halaman

  // Mengambil nilai radio button yang terpilih
  const genderSelected = document.querySelector('input[name="gender"]:checked').value;

  // MENAMBAH DATA BARU KE OBJECT & ARRAY
  const siswaBaru = {
    id: Date.now(), // Generate ID unik berdasarkan timestamp
    nama: inputNama.value,
    jurusan: selectJurusan.value,
    gender: genderSelected,
    aktif: checkAktif.checked
  };

  // Operasi Array: Menambah data baru ke akhir array (push)
  dataSiswa.push(siswaBaru);

  // Reset Form & Render ulang tabel
  form.reset();
  document.getElementById("namaPreview").innerText = "";
  tampilkanData(dataSiswa);
});

// ==========================================
// 3. OPERASI ARRAY & OBJECT (CRUD DATA)
// ==========================================

// RENDER / MENGAKSES DATA UNTUK DITAMPILKAN DI HTML
function tampilkanData(listData) {
  tabelSiswa.innerHTML = ""; // Bersihkan tabel terlebih dahulu

  // Mengakses data array menggunakan loop forEach
  listData.forEach(function(siswa) {
    const statusBadge = siswa.aktif 
      ? `<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Aktif</span>`
      : `<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">Tidak Aktif</span>`;

    // Mengakses property object menggunakan dot notation (.)
    const row = `
      <tr class="hover:bg-gray-50">
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${siswa.id}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${siswa.nama}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${siswa.jurusan}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${siswa.gender}</td>
        <td class="px-6 py-4 whitespace-nowrap text-sm">${statusBadge}</td>
      </tr>
    `;
    tabelSiswa.innerHTML += row;
  });
}

// MENCARI DATA DI ARRAY (filter & includes)
document.getElementById("btnCari").addEventListener("click", function() {
  const kataKunci = document.getElementById("inputCari").value.toLowerCase();
  
  // Operasi Array: menyaring data sesuai pencarian
  const hasilCari = dataSiswa.filter(function(siswa) {
    return siswa.nama.toLowerCase().includes(kataKunci);
  });

  tampilkanData(hasilCari);
});

// MENGUBAH DATA DI ARRAY & OBJECT
document.getElementById("btnUbah").addEventListener("click", function() {
  if (dataSiswa.length > 0) {
    // Mengakses data index ke-0 lalu mengubah property nama pada object
    dataSiswa[0].nama = dataSiswa[0].nama + " (Updated)";
    tampilkanData(dataSiswa);
  }
});

// MENGHAPUS DATA DARI ARRAY
document.getElementById("btnHapus").addEventListener("click", function() {
  if (dataSiswa.length > 0) {
    // Operasi Array: menghapus elemen pertama (shift)
    dataSiswa.shift(); 
    tampilkanData(dataSiswa);
  }
});

// MENGECEK KEY & MENGAMBIL SELURUH KEY OBJECT
document.getElementById("btnCekKey").addEventListener("click", function() {
  if (dataSiswa.length > 0) {
    const contohObject = dataSiswa[0];

    // Mengecek apakah key tertentu ada pada Object (operator 'in')
    const adaNama = "nama" in contohObject;
    const adaAlamat = "alamat" in contohObject;

    // Mengambil seluruh key pada Object (Object.keys)
    const semuaKey = Object.keys(contohObject);

    alert(
      `Cek Key 'nama': ${adaNama}\n` +
      `Cek Key 'alamat': ${adaAlamat}\n` +
      `Semua Key dalam Object: ${semuaKey.join(", ")}`
    );
  }
});

// Tampilkan data awal saat halaman pertama kali dimuat
tampilkanData(dataSiswa);