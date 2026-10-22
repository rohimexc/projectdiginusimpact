let dataString = "apri";
console.log(dataString);

// 1.escaping string
// jika kita ingin menampilkan tanda kutip di dalam string, maka kita harus menggunakan tanda backslash (\) sebelum tanda kutip tersebut
// atau kita bisa menggunakan tanda kutip yang berbeda, misalnya jika kita menggunakan tanda kutip ganda ("), maka kita bisa menggunakan tanda kutip tunggal (') di dalam string, dan sebaliknya
let dataString2 = "apri \"Apa kabar dunia?\"";
console.log(dataString2);
let dataString3 = 'apri "Hidup jokowi"';
console.log(dataString3);

// escaping string menggunakan \n berguna untuk membuat baris baru di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada baris baru di antara kata-kata yang ada di dalam string
let dataString4 = "apri\nApa kabar dunia?";
console.log(dataString4); 

// escaping string menggunakan \t berguna untuk membuat tab di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada tab di antara kata-kata yang ada di dalam string
let dataString5 = "apri\tApa kabar dunia?";
console.log(dataString5);

//escaping string menggunakan \\ berguna untuk menampilkan tanda backslash (\) di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada tanda backslash di antara kata-kata yang ada di dalam string
let dataString6 = "apri\\Apa kabar dunia?";
console.log(dataString6);

//escaping string menggunakan \r berguna untuk membuat carriage return di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada carriage return di antara kata-kata yang ada di dalam string
let dataString7 = "apri \rApa kabar dunia?";
console.log(dataString7);

//escaping string menggunakan \b berguna untuk membuat backspace di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada backspace di antara kata-kata yang ada di dalam string
let dataString8 = "apri \bApa kabar dunia?";
console.log(dataString8);

//escaping string menggunakan \f berguna untuk membuat form feed di dalam string, sehingga ketika kita menampilkan string tersebut, maka akan ada form feed di antara kata-kata yang ada di dalam string
let dataString9 = "apri \fApa kabar dunia?";
console.log(dataString9);


// 2. literal string (template string)
// literal string (template string) adalah string yang bisa mengandung ekspresi di dalamnya, sehingga kita bisa menampilkan nilai dari variable di dalam string tersebut
let namadepan = "apri";
let namabelakang = "setiawan";
// misalnya kita tambahkan umur, otomatis umur akan berubah menjadi string, sehingga kita bisa menampilkan umur di dalam string tersebut
let umur = 20;
let namalengkap = namadepan + " " + namabelakang + " umur saya " + umur + " tahun";
console.log(namalengkap);

// literal string (template string) menggunakan backtick (`) dan ekspresi di dalamnya menggunakan ${}
// menggunakan backtick (`) agar kita bisa melihat bahwa variable umur akan berubah menjadi string dengan menggunakan template string ${umur} di dalam string tersebut
let namalengkap2 = `${namadepan} ${namabelakang} umur saya ${umur} tahun`;
console.log(namalengkap2);