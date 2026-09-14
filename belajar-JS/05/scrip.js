/*
  =======================================================
  MATERI 05: TIPE DATA (String, Number, Boolean, Undefined, NaN)
  =======================================================
*/

// 1. Tipe Data String (Teks)
let dataString = "Ucup";
console.log(dataString);
console.log(typeof dataString); // Output: string

// 2. Tipe Data Number (Angka Bulat / Desimal)
let dataNumber = 16.324;
console.log(dataNumber);
console.log(typeof dataNumber); // Output

// 3. Tipe Data Boolean (true / false)
let dataBoolean = false;
console.log(dataBoolean);
console.log(typeof dataBoolean); 
// 4. Dynamic Typing (Tipe data variabel bisa berubah)
dataString = 2; // Mengubah isi dari String menjadi Number
console.log(dataString);
console.log(typeof dataString); 

// 5. Tipe Data Undefined (Variabel belum diisi nilai)
let dataKosong;
console.log(dataKosong); 
console.log(typeof dataKosong); 

// Mengisi nilai ke variabel yang sebelumnya undefined
dataKosong = "Otong";
console.log(dataKosong);
console.log(typeof dataKosong); 

// 6. Kasus Khusus: NaN (Not a Number)
let hasil = Math.sqrt(-1); // Akar dari -1 menghasilkan bilangan imajiner
console.log(hasil); // Output: NaN
console.log(typeof hasil); // Output: number