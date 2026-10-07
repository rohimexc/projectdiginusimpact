# Mengimpor fungsi render dari Django untuk menggabungkan data Python ke file HTML
from django.shortcuts import render

# Fungsi view utama untuk menangani request halaman beranda/landing page
def home(request):
    # Menyimpan seluruh data konten prodi dalam bentuk dictionary (context)
    context = {
        # Data teks ringkas prodi
        'nama_prodi': 'Ilmu Administrasi Publik',
        'akreditasi': 'Unggul',
        'visi': 'Menjadi program studi unggul dalam menghasilkan lulusan yang kompeten di bidang tata kelola publik digital dan kebijakan publik strategis.',
        
        # Data berupa list untuk ditampilkan pakai perulangan (looping) di HTML
        'keunggulan': [
            'Kurikulum Berbasis Kebijakan Publik Digital & E-Government',
            'Kerja Sama Magang di Instansi Pemerintah & Lembaga Riset',
            'Fasilitas Laboratorium Kebijakan & Tata Kelola Publik',
        ],
        
        # Daftar peluang karir lulusan prodi
        'prospek_karir': [
            'Analis Kebijakan Publik',
            'Aparatur Sipil Negara (ASN / Birokrat)',
            'Manajer Organisasi Non-Profit / NGO',
            'Konsultan Tata Kelola Pemerintahan',
        ]
    }
    
    # Mengirimkan file index.html ke browser beserta seluruh isi data context
    return render(request, 'core/index.html' , context)