# 🎓 Examind - Platform Pembelajaran Interaktif

![Examind Banner](https://img.shields.io/badge/Examind-Platform%20Belajar-orange?style=for-the-badge)
![Django](https://img.shields.io/badge/Django-4.2+-green?style=for-the-badge&logo=django)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-blue?style=for-the-badge&logo=tailwindcss)

**Examind** adalah platform pembelajaran interaktif yang dirancang untuk membantu siswa dan mahasiswa dalam proses belajar.

## 🚀 Fitur Utama

- 🔐 **Sistem Autentikasi** - Login/logout yang aman
- 📚 **Dashboard Interaktif** - Overview lengkap progress belajar
- 🎨 **UI/UX Modern** - Design responsive dengan TailwindCSS
  <!-- - 📊 **Tracking Progress** - Monitor kemajuan belajar secara real-time -->
  <!-- - 🎯 **Study Sets** - Organisasi materi pembelajaran -->
- ⚡ **Performance Optimized** - Loading cepat dan smooth

## 🎨 Color Palette

| Warna           | Hex Code  | Penggunaan                    |
| --------------- | --------- | ----------------------------- |
| 🔵 Primary Dark | `#11222c` | Background utama, teks header |
| 🌊 Teal         | `#1c5858` | Accent, hover states          |
| 🟠 Orange       | `#f69000` | Primary buttons, highlights   |
| 💧 Cyan         | `#53b1b1` | Secondary elements            |
| 🟡 Yellow       | `#f6c624` | Warning, notifications        |
| ⚪ Light        | `#eff1f5` | Background sekunder, cards    |

## 📋 Prasyarat Sistem

Pastikan sistem Anda sudah memiliki:

- **Python 3.8+**
- **pip** (Python package installer)
- **Git** (untuk version control)
- **Web Browser** modern (Chrome, Firefox, Safari, Edge)

## 🛠️ Instalasi & Setup

### 1. Clone Repository

```bash
git clone https://github.com/DinkyTrady/examind.git
cd examind
```

### 2. Setup Projek

```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
# Untuk Linux/Mac:
source venv/bin/activate
# Untuk Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Jalankan migrasi database
python manage.py makemigrations
python manage.py migrate

# Buat superuser
python manage.py createsuperuser

# Collect static files (jika diperlukan)
python manage.py collectstatic
```

## 🚀 Menjalankan Aplikasi

### 1. Aktifkan Virtual Environment

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Jalankan Development Server

```bash
python manage.py runserver
```

### 3. Akses Aplikasi

Buka browser dan kunjungi:

- **Homepage**: <http://127.0.0.1:8000/>
- **Admin Panel**: <http://127.0.0.1:8000/admin/>

## 👤 Login & Akses

### Default Login

Gunakan akun superuser yang telah dibuat saat instalasi.

### Halaman yang Tersedia

- `/` - Homepage (not available now)
- `/dashboard` - Dashboard utama (login required)
- `/login/` - Halaman login
- `/logout/` - Logout
- `/admin/` - Panel admin Django

## 🐛 Troubleshooting

### Error Umum & Solusi

#### 1. ModuleNotFoundError: No module named 'django'

```bash
# Pastikan virtual environment aktif
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Port sudah digunakan

```bash
# Gunakan port lain
python manage.py runserver 8001
```

#### 3. Database error

```bash
# Reset database
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 4. Static files tidak muncul

```bash
# Collect static files
python manage.py collectstatic --clear
```

### Debug Mode

Untuk debugging lebih detail, set `DEBUG=True` di settings.py dan jalankan:

```bash
python manage.py runserver --settings=examind.settings --verbosity=2
```

## 👨‍💻 Kontributor

<table>
  <tr>
    <th>Foto</th>
    <th>Nama</th>
    <th>GitHub</th>
  </tr>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/111265264?v=4" width="60" style="border-radius: 50%;" /></td>
    <td><strong>Randy Dinky Saputra</strong></td>
    <td><a href="https://github.com/DinkyTrady">@DinkyTrady</a></td>
  </tr>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/144525698?v=4" width="60" style="border-radius: 50%;" /></td>
    <td><strong>Ello Adrian Hariadi</strong></td>
    <td><a href="https://github.com/Driannnn">@Driannnn</a></td>
  </tr>
  <td><img src="https://avatars.githubusercontent.com/u/207975203?v=4" width="60" style="border-radius: 50%;" /></td>
    <td><strong>Pratama Dicky Novianto</strong></td>
    <td><a href="https://github.com/pratamadky">@pratamadky</a></td>
  </tr>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/152749994?v=4" width="60" style="border-radius: 50%;" /></td>
    <td><strong>Rendy Syahputra Riyadi</strong></td>
    <td><a href="https://github.com/Rendyprobe">@Rendyprobe</a></td>
  </tr>
   <tr>
    <td><img src="https://avatars.githubusercontent.com/u/207875678?v=4" width="60" style="border-radius: 50%;" /></td>
    <td><strong>Aditya Febrian</strong></td>
    <td><a href="https://github.com/AdityaFebrian23">@AdityaFebrian23</a></td>
  </tr>
</table>

### Cara Berkontribusi

- Gunakan pesan commit yang jelas dan deskriptif
- Tambahkan dokumentasi untuk fitur baru
- Pastikan code mengikuti PEP 8 style guide
- Test fitur sebelum submit PR

## 📚 Resources & Dokumentasi

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 📄 License

Project ini dilisensikan di bawah [MIT License](LICENSE).

## 🙏 Acknowledgments

- Tim Django untuk framework yang luar biasa
- TailwindCSS untuk utility-first CSS framework
- Komunitas Python Indonesia
