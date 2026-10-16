/*
  =======================================================
  MATERI 04: VARIABEL (let, var, const)
  =======================================================
*/

// 1. Variabel menggunakan 'let'
// Nilainya bisa diubah dan menggunakan aturan Block Scope
let nama = "Ucup surucup";
console.log(nama); // Menampilkan: Ucup surucup

// Mengubah nilai variabel let (tanpa perlu menuliskan kata 'let' lagi)
nama = "Otong surotong";
console.log(nama); // Menampilkan: Otong surotong


// 2. Perbedaan Scoping antara 'let' dan 'var'
// Contoh Block Scope menggunakan 'let':
let namaBelakang = "surucup";
{
    let namaBelakang = "surotong";
    console.log(namaBelakang); // Menampilkan: surotong (Hanya berlaku di dalam kurung kurawal)
}
console.log(namaBelakang); // Menampilkan: surucup (Nilai di luar kurung kurawal tetap aman)

// Contoh Global Scope menggunakan var:
var namaTengah = "Keren";
{
    var namaTengah = "Ganteng"; // Nilai di luar kurung kurawal akan ikut tertimpa/berubah
}
console.log(namaTengah); // Menampilkan: Ganteng


// 3. Kasus Khusus Tanpa Keyword (Otomatis menjadi 'var')
gorengan = "bala-bala";
gorengan = "combro";
console.log(gorengan); // Menampilkan: combro


// 4. Variabel menggunakan 'const' (Konstanta)
// Nilainya tetap dan janji tidak boleh diubah nilainya
const TTL = "10 Maret 2022";
console.log(TTL);

// TTL = "11 Maret 2054"; // Jika diaktifkan, baris ini akan menyebabkan ERROR!