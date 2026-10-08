        /* ==========================================================================
           1. STATE UTAMA (ARRAY OF OBJECTS) & DATA AWAL
           ========================================================================== */
        // Menggunakan Array of Objects sebagai penyimpan data utama
        let inventoryData = [
            { id: 101, nama: "MacBook Air M2", harga: 18500000, stok: 5, kategori: "Elektronik", kondisi: "Baru", isPromo: true },
            { id: 102, nama: "Kemeja Flanel Retro", harga: 250000, stok: 20, kategori: "Pakaian", kondisi: "Baru", isPromo: false },
            { id: 103, nama: "Kopi Arabika 250g", harga: 65000, stok: 45, kategori: "Makanan", kondisi: "Baru", isPromo: true }
        ];

        // Object sementara untuk menandai produk yang sedang di-inspect
        let inspectedObject = null;

        /* ==========================================================================
           2. ELEMEN SELEKTOR DOM
           ========================================================================== */
        const formProduk = document.getElementById('form-produk');
        const inputId = document.getElementById('input-id');
        const inputNama = document.getElementById('input-nama');
        const inputHarga = document.getElementById('input-harga');
        const inputStok = document.getElementById('input-stok');
        const inputKategori = document.getElementById('input-kategori');
        const inputPromo = document.getElementById('input-promo');
        const inputCustomKey = document.getElementById('input-custom-key');
        const inputCustomVal = document.getElementById('input-custom-val');
        
        const searchInput = document.getElementById('search-input');
        const filterKategori = document.getElementById('filter-kategori');
        const tableBody = document.getElementById('table-body');
        const liveNamaPreview = document.getElementById('live-nama-preview');

        /* ==========================================================================
           3. EVENT LISTENERS (INPUT, CHANGE, SUBMIT)
           ========================================================================== */

        // Event 'DOMContentLoaded': Dijalankan saat HTML selesai dimuat
        document.addEventListener('DOMContentLoaded', () => {
            renderTable(inventoryData);
            updateStats();
        });

        // Event 'input' (Realtime Input Text): Deteksi ketikan secara langsung
        inputNama.addEventListener('input', (e) => {
            const val = e.target.value;
            if (val.trim() !== '') {
                liveNamaPreview.classList.remove('hidden');
                liveNamaPreview.querySelector('span').textContent = val;
            } else {
                liveNamaPreview.classList.add('hidden');
            }
        });

        // Event 'input' pada Search Input: Pencarian data realtime
        searchInput.addEventListener('input', (e) => {
            const keyword = e.target.value.toLowerCase();
            // MANIPULASI ARRAY: filter() untuk mencari produk sesuai keyword
            const filtered = inventoryData.filter(item => 
                item.nama.toLowerCase().includes(keyword) || 
                item.kategori.toLowerCase().includes(keyword)
            );
            renderTable(filtered);
        });

        // Event 'change' pada Select Filter: Penyaringan berdasarkan kategori
        filterKategori.addEventListener('change', (e) => {
            const selectedCat = e.target.value;
            if (selectedCat === 'ALL') {
                renderTable(inventoryData);
            } else {
                // MANIPULASI ARRAY: filter() berdasarkan kategori
                const filtered = inventoryData.filter(item => item.kategori === selectedCat);
                renderTable(filtered);
            }
        });

        // Event 'submit' pada Form: Menangani penambahan & pengubahan data
        formProduk.addEventListener('submit', (e) => {
            // Mencegah reload halaman standar browser
            e.preventDefault();

            // Membaca nilai dari Radio Button yang terpilih
            const selectedKondisi = document.querySelector('input[name="input-kondisi"]:checked').value;

            const editId = inputId.value;

            if (editId) {
                /* --- MANIPULASI ARRAY: findIndex() & MANIPULASI OBJECT: Mengubah Data --- */
                const index = inventoryData.findIndex(item => item.id == editId);
                if (index !== -1) {
                    inventoryData[index].nama = inputNama.value;
                    inventoryData[index].harga = Number(inputHarga.value);
                    inventoryData[index].stok = Number(inputStok.value);
                    inventoryData[index].kategori = inputKategori.value;
                    inventoryData[index].kondisi = selectedKondisi;
                    inventoryData[index].isPromo = inputPromo.checked;

                    // Dynamic Object Property addition jika diisi
                    if(inputCustomKey.value.trim() !== '') {
                        inventoryData[index][inputCustomKey.value.trim()] = inputCustomVal.value.trim();
                    }
                }
            } else {
                /* --- MANIPULASI OBJECT: Menambah Property Baru & MANIPULASI ARRAY: push() --- */
                let newProduk = {
                    id: Date.now(), // Generate ID unik
                    nama: inputNama.value,
                    harga: Number(inputHarga.value),
                    stok: Number(inputStok.value),
                    kategori: inputKategori.value,
                    kondisi: selectedKondisi,
                    isPromo: inputPromo.checked
                };

                // Menambah property kustom secara dinamis ke Object
                if(inputCustomKey.value.trim() !== '') {
                    newProduk[inputCustomKey.value.trim()] = inputCustomVal.value.trim();
                }

                // Menambah Object baru ke dalam Array
                inventoryData.push(newProduk);
            }

            resetForm();
            renderTable(inventoryData);
            updateStats();
        });

        /* ==========================================================================
           4. FUNGSI RENDERING DOM & OPERASI ARRAY
           ========================================================================== */

        // Fungsi Render Data Array ke Tabel HTML
        function renderTable(dataArray) {
            tableBody.innerHTML = '';

            if (dataArray.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="6" class="p-4 text-center text-slate-400 italic">Data produk tidak ditemukan.</td>
                    </tr>
                `;
                document.getElementById('badge-count').textContent = '0 Item';
                return;
            }

            document.getElementById('badge-count').textContent = `${dataArray.length} Item`;

            // MANIPULASI ARRAY: map() atau forEach() untuk membaca setiap Object
            dataArray.forEach((item) => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-50 transition-colors cursor-pointer";
                
                // Menghitung harga diskon jika isPromo true
                const finalHarga = item.isPromo ? item.harga * 0.9 : item.harga;

                tr.innerHTML = `
                    <td class="p-3 text-xs font-mono font-bold text-slate-500">#${item.id}</td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-800">${item.nama}</div>
                        ${item.isPromo ? '<span class="text-[10px] bg-amber-100 text-amber-700 px-1.5 py-0.5 rounded font-bold">PROMO 10%</span>' : ''}
                    </td>
                    <td class="p-3">
                        <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded">${item.kategori}</span>
                        <span class="text-xs ${item.kondisi === 'Baru' ? 'text-emerald-600' : 'text-amber-600'} font-medium ml-1">(${item.kondisi})</span>
                    </td>
                    <td class="p-3">
                        <div class="font-semibold text-slate-700">Rp ${finalHarga.toLocaleString('id-ID')}</div>
                        ${item.isPromo ? `<div class="text-[10px] text-slate-400 line-through">Rp ${item.harga.toLocaleString('id-ID')}</div>` : ''}
                    </td>
                    <td class="p-3">
                        <span class="font-medium ${item.stok < 10 ? 'text-rose-600 font-bold' : 'text-slate-600'}">${item.stok} pcs</span>
                    </td>
                    <td class="p-3 text-center">
                        <div class="flex justify-center gap-2" onclick="event.stopPropagation()">
                            <button onclick="editProduct(${item.id})" class="p-1.5 text-blue-600 hover:bg-blue-50 rounded" title="Edit Data">
                                <i class="fa-solid fa-pen-to-square"></i>
                            </button>
                            <button onclick="deleteProduct(${item.id})" class="p-1.5 text-rose-600 hover:bg-rose-50 rounded" title="Hapus Data">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                        </div>
                    </td>
                `;

                // Event Listener Click pada baris tabel untuk inspeksi Object
                tr.addEventListener('click', () => inspectObject(item));

                tableBody.appendChild(tr);
            });
        }

        /* --- MANIPULASI ARRAY: find() --- */
        function editProduct(id) {
            // Mencari 1 Object spesifik di dalam Array
            const item = inventoryData.find(prod => prod.id === id);
            if (!item) return;

            document.getElementById('form-title').innerHTML = `<i class="fa-solid fa-pen-to-square text-indigo-600"></i> Edit Produk #${item.id}`;
            document.getElementById('btn-cancel-edit').classList.remove('hidden');

            // Mengisi nilai form dengan data Object
            inputId.value = item.id;
            inputNama.value = item.nama;
            inputHarga.value = item.harga;
            inputStok.value = item.stok;
            inputKategori.value = item.kategori;
            inputPromo.checked = item.isPromo;

            const radioKondisi = document.querySelectorAll('input[name="input-kondisi"]');
            radioKondisi.forEach(r => r.value === item.kondisi ? r.checked = true : null);

            inspectObject(item);
        }

        /* --- MANIPULASI ARRAY: splice() --- */
        function deleteProduct(id) {
            // Mencari indeks posisi Object di dalam Array
            const index = inventoryData.findIndex(item => item.id === id);
            if (index !== -1) {
                // Hapus 1 elemen dari array berdasarkan indeksnya
                inventoryData.splice(index, 1);
                renderTable(inventoryData);
                updateStats();
                
                document.getElementById('inspector-keys').textContent = "Produk telah dihapus dari Array.";
                inspectedObject = null;
            }
        }

        /* ==========================================================================
           5. FUNGSI INSPEKSI OBJECT & OPERASI KEY
           ========================================================================== */

        // Menggunakan Object.keys() untuk mendapatkan seluruh properti Object
        function inspectObject(obj) {
            inspectedObject = obj;
            const keys = Object.keys(obj); // Meminta semua key dalam bentuk Array
            
            let htmlOutput = `<strong>ID: ${obj.id} (${obj.nama})</strong><br>`;
            htmlOutput += `Key List [${keys.length}]: <span class="text-amber-300">${keys.join(', ')}</span><br><br>`;
            htmlOutput += `JSON Data:<br>${JSON.stringify(obj, null, 2)}`;

            document.getElementById('inspector-keys').innerHTML = htmlOutput;
        }

        // Mengecek keberadaan key tertentu dengan operator 'in'
        function checkKeyInObject() {
            const keyInput = document.getElementById('check-key-input').value.trim();
            const resultEl = document.getElementById('check-key-result');

            if (!inspectedObject) {
                resultEl.className = "text-xs text-rose-500 font-semibold";
                resultEl.textContent = "Pilih/klik salah satu produk di tabel terlebih dahulu!";
                return;
            }

            if (!keyInput) {
                resultEl.className = "text-xs text-amber-600";
                resultEl.textContent = "Masukkan nama key yang ingin dicek.";
                return;
            }

            /* OPERATOR 'in': Mengecek apakah property ada pada Object */
            const isExist = keyInput in inspectedObject;

            if (isExist) {
                resultEl.className = "text-xs text-emerald-600 font-bold";
                resultEl.textContent = `Ya! Key '${keyInput}' ADA dalam Object ini. (Value: ${inspectedObject[keyInput]})`;
            } else {
                resultEl.className = "text-xs text-rose-600 font-bold";
                resultEl.textContent = `Tidak! Key '${keyInput}' TIDAK DITEMUKAN dalam Object ini.`;
            }
        }

        // Memperbarui Statistik Ringkasan Data
        function updateStats() {
            document.getElementById('stat-total').textContent = inventoryData.length;
            
            // Filter promo
            const promoCount = inventoryData.filter(i => i.isPromo).length;
            document.getElementById('stat-promo').textContent = promoCount;

            // Filter kondisi baru
            const baruCount = inventoryData.filter(i => i.kondisi === 'Baru').length;
            document.getElementById('stat-baru').textContent = baruCount;

            // Total Nilai Stok
            const totalNilai = inventoryData.reduce((acc, item) => acc + (item.harga * item.stok), 0);
            document.getElementById('stat-nilai').textContent = `Rp ${totalNilai.toLocaleString('id-ID')}`;
        }

        // Reset Formulir
        function resetForm() {
            formProduk.reset();
            inputId.value = '';
            document.getElementById('form-title').innerHTML = `<i class="fa-solid fa-plus-circle text-indigo-600"></i> Tambah Produk Baru`;
            document.getElementById('btn-cancel-edit').classList.add('hidden');
            liveNamaPreview.classList.add('hidden');
        }

        // Switch Tab Navigasi
        function switchTab(tab) {
            const secApp = document.getElementById('section-app');
            const secEdu = document.getElementById('section-edu');
            const navApp = document.getElementById('nav-app');
            const navEdu = document.getElementById('nav-edu');

            if (tab === 'app') {
                secApp.classList.remove('hidden');
                secEdu.classList.add('hidden');
                navApp.className = "px-4 py-2 text-sm font-medium rounded-lg text-white bg-indigo-600 transition-all";
                navEdu.className = "px-4 py-2 text-sm font-medium rounded-lg text-indigo-200 hover:text-white transition-all";
            } else {
                secApp.classList.add('hidden');
                secEdu.classList.remove('hidden');
                navEdu.className = "px-4 py-2 text-sm font-medium rounded-lg text-white bg-indigo-600 transition-all";
                navApp.className = "px-4 py-2 text-sm font-medium rounded-lg text-indigo-200 hover:text-white transition-all";
            }
        }
