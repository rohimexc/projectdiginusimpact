// 1. mempelajari tentang charAt
// ini berfungsi untuk mengambil karakter dari sebuah string berdasarkan index yang ditentukan. Index dimulai dari 0.
let huruf ="abcdf";
let huruff =huruf.charAt(0);
console.log(`Huruf 0 : ${huruff}`);
huruff =huruf.charAt(1);
console.log(`Huruf 1 : ${huruff}`);
huruff =huruf.charAt(2);
console.log(`Huruf 2 : ${huruff}`);
huruff =huruf.charAt(3);
console.log(`Huruf 3 : ${huruff}`);
huruff =huruf.charAt(4);
console.log(`Huruf 4 : ${huruff}`);

// 2. menyambung string menggunakan concat
// concat adalah method yang digunakan untuk menggabungkan dua atau lebih string menjadi satu string. Method ini tidak mengubah string asli, tetapi mengembalikan string baru yang merupakan hasil penggabungan.
let kata1 = "Belajar";
let kata2 = "JavaScript";

let kata3 = kata1.concat(" ", kata2); 
console.log(kata3);

// 3. mengambil index dari sebuah string menggunakan indexOf
// indexOf adalah method yang digunakan untuk mencari index dari sebuah karakter atau substring dalam sebuah string. Method ini mengembalikan index pertama dari karakter atau substring yang ditemukan, atau -1 jika tidak ditemukan.
console.log(`Index dari huruf a adalah : ${kata3.indexOf("t")}`); // index pertama dari huruf t

// 4. substring
// substring adalah method yang digunakan untuk mengambil sebagian dari sebuah string berdasarkan index awal dan index akhir yang ditentukan. Method ini mengembalikan string baru yang merupakan potongan dari string asli.
let kata4 = kata3.substring(0, 7);
console.log(`Substring dari kata3 adalah : ${kata4}`); // mengambil substring dari index 0 sampai 7 (tidak termasuk index 7)

// 5. slice
// slice adalah method yang digunakan untuk mengambil sebagian dari sebuah string berdasarkan index awal dan index akhir yang ditentukan. Method ini mengembalikan string baru yang merupakan potongan dari string asli.
//  Perbedaannya dengan substring adalah slice tidak bisa membalikkan index, sedangkan substring bisa. Jika index awal lebih besar dari index akhir, maka substring akan membalikkan index, sedangkan slice akan mengembalikan string kosong.
let kata5 = kata3.slice(0, 7);
console.log(`Slice dari kata3 adalah : ${kata5}`); // mengambil slice dari index 0 sampai 7 (tidak termasuk index 7)

// 6. replace
// replace adalah method yang digunakan untuk mengganti karakter atau substring dalam sebuah string dengan karakter atau substring yang baru. Method ini mengembalikan string baru yang merupakan hasil penggantian, dan tidak mengubah string asli.
let kata6 = kata3.replace("JavaScript", "JS");
console.log(`Replace dari kata3 adalah : ${kata6}`); // mengganti JavaScript dengan JS

//7. tolowerCase dan toUpperCase
// toLowerCase adalah method yang digunakan untuk mengubah semua karakter dalam sebuah string menjadi huruf kecil. Method ini mengembalikan string baru yang merupakan hasil pengubahan, dan tidak mengubah string asli.
let kata7 = kata3.toLowerCase();
console.log(`toLowerCase dari kata3 adalah : ${kata7}`); // mengubah semua karakter menjadi huruf kecil
// toUpperCase adalah method yang digunakan untuk mengubah semua karakter dalam sebuah string menjadi huruf besar. Method ini mengembalikan string baru yang merupakan hasil pengubahan, dan tidak mengubah string asli.
let kata8 = kata3.toUpperCase();
console.log(`toUpperCase dari kata3 adalah : ${kata8}`); // mengubah semua karakter menjadi huruf besar

// 8.extracting data number
// extracting data number adalah method yang digunakan untuk mengambil angka dari sebuah string. Method ini mengembalikan string baru yang merupakan hasil pengambilan angka, dan tidak mengubah string asli.
let dataString = '10';
console.log(typeof dataString); // string
let dataNumber = parseInt(dataString);
console.log(dataNumber); // 10
console.log(typeof dataNumber); // number

// data float
let dataString2 = '10.5';
console.log(typeof dataString2); // string
let dataNumber2 = parseFloat(dataString2);
console.log(dataNumber2); // 10.5
console.log(typeof dataNumber2); // number