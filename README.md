Langkah-langkah untuk menjalankan Aplikasi: 
- pastikan git sudah terinstall di komputer
- buka terminal di folder project
- Download code dari repository ini dengan jalankan 
    perintah: git clone https://github.com/app-generator/django-adminlte.git
- Install dependency aplikasi
dengan jalankan perintah: pip install -r requirements.txt
- jalankan aplikasi dengan perintah: python manage.py runserver
- buka http://127.0.0.1:8000 di browser

Langkah-langkah Deploy Aplikasi dengan Docker:
- buka terminal di folder project
- jalankan perintah: docker-compose up --build
- buka http://localhost:5085 di browser
