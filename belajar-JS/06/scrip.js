/*
  =======================================================
  MATERI 06: STRING (ESCAPING & TEMPLATE LITERAL)
  =======================================================
*/

// --- 1. ESCAPING STRING ---

// Masalah: Menggunakan tanda kutip ganda di dalam kutip ganda akan menyebabkan SyntaxError
// Solusi A: Menggunakan kombinasi single quote dan double quote
let data1 = 'Ucup berkata "Apa kabar dunia?"';
console.log(data1);

// Solusi B: Menggunakan backslash (\) sebagai Escaping Character
let data2 = "Otong berkata \"Tetap Asik\"";
console.log(data2);

// Karakter khusus Escaping Character lainnya:
// \n : Newline / Baris Baru (Enter)
// \t : Tabulasi (Tab)
let data3 = "Ucup berjalan-jalan di tepi pantai.\n\tKeren banget!";
console.log(data3);


// --- 2. CONCATENATION (CARA LAMA) ---
let namaDepan = "Otong";
let namaBelakang = "Surotong";
let umur = 7;

// Menggabungkan string dengan operator (+)
let namaLengkap = namaDepan + " " + namaBelakang + " berumur " + umur + " tahun";
console.log(namaLengkap);


// --- 3. TEMPLATE LITERAL / LITERAL STRING (CARA MODERN) ---
// Menggunakan simbol backtick (``) di bawah tombol Esc
// Menggunakan sintaks ${variabel} untuk menyisipkan nilai variabel
let biodata = `${namaDepan} ${namaBelakang} berumur ${umur} tahun`;
console.log(biodata);

// Mengubah nilai variabel umur secara dinamis
umur = 10;
biodata = `Perubahan: ${namaDepan} ${namaBelakang} sekarang berumur ${umur} tahun`;
console.log(biodata);