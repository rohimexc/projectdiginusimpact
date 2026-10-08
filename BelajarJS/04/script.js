// 1. variable dengan let
let nama = "Apri";
let umur = 20;
let tinggi = 170;

//tampilan variable
console.log("Nama saya " + nama);
console.log("Umur saya " + umur + " tahun");
console.log("Tinggi saya " + tinggi + " cm");

//ubah nilai variable
nama = "Apri Setiawan";
umur = 21;
tinggi = 171;
console.log("Nama saya " + nama);
console.log("Umur saya " + umur + " tahun");
console.log("Tinggi saya " + tinggi + " cm");


// 2. variable dengan var
var nama2 = "Apri";
var umur2 = 20;
var tinggi2 = 170;

console.log("Nama saya " + nama2);
console.log("Umur saya " + umur2 + " tahun");
console.log("Tinggi saya " + tinggi2 + " cm");

//ubah nilai variable
nama2 = "Apri Setiawan";
umur2 = 21;
tinggi2 = 171;
console.log("Nama saya " + nama2);
console.log("Umur saya " + umur2 + " tahun");
console.log("Tinggi saya " + tinggi2 + " cm");


//kelakuan variable dengan let
let namabelakang = "Apri";
// tanda kurung kurawal hanya untuk memanggil variable namabelakang di dalam kurung kurawal saja, 
// dan bisa di tambah if, while, for, dll
{
    let namabelakang = "Setiawan";
    console.log(namabelakang);
}
console.log(namabelakang);

//kelakuan variable dengan var
//bedanya var adalah ketika ada var di dalam kurung kurawal, maka var tersebut akan menimpa var di luar kurung kurawal
var namaTengah = "Apri";
{
    var namaTengah = "Setiawan";
    console.log(namaTengah);
}
console.log(namaTengah);

//contoh kasus
//jika membuat variable tanpa keyword akan otomatis menjadi var, sehingga bisa menimpa variable di luar
buah = "Mangga";
{
    buah = "Apel";
}
console.log(buah); // output: Apel


//3 . variable dengan const
// const adalah variable yang nilainya tidak bisa diubah
const TTl = "20 Juni 2003"; 
console.log(TTl);