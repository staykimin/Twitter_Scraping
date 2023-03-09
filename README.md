
# Twitter Scaping

   Program Ini Menggunakan Sistem Web Automation Untuk Men Scaping Data dan Flask Untuk Membuat API dan Juga Menampilkan Data.






## Installation

Cara Install Server

```bash
  pip install -r modul.min
  playwright install
```
    
## Usage/Examples

```python
-> python twitter.py
```

## Features

- Searcing Semua Tweet Yang Mengandung Kata Mulai Dari Tanggal xx Sampai Tanggal xx
- Penyesuain Waktu Timeout
- Speed Testing
- Ambil Semua Data Dari Popular / Populer Tweet
- Ambil Semua Data Dari Latest / Terbaru Tweet
- Ambil Semua Data Dari Orang / People Tweet
- Ambil Semua Data Dari Foto Tweet
- Ambil Semua Data Dari Vidio Tweet


## Documentation

[Documentation]

- `/Api`  -> Digunakan Untuk Melihat Data Hasil Scraping Dalam Bentuk API
- `/Data`     -> Digunakan Untuk Melihat Data Hasil Scraping


## API Reference

#### Kirim Pesan

```http
  POST /
```

| Parameter | Required | Type     | Description                       |
| :-------- | :------- | :------- | :-------------------------------- |
| `query`| `True` | `string` | Untuk Mencari Keyword |
| `mulai` | `True` |`string` | Untuk Menentukan Tanggal Awal Pencarian Dengan Format (Bulan/Hari/Tahun)
| `sampai` | `True` | `string` | Untuk Menentukan Tanggal Akhir Pencarian Dengan Format (Bulan/Hari/Tahun)


