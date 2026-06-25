import csv
import os

# 1. STRUKTUR DATA 1: Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah_di_akhir(self, data):
        node_baru = Node(data)
        if not self.head:
            self.head = node_baru
            return
        saat_ini = self.head
        while saat_ini.next:
            saat_ini = saat_ini.next
        saat_ini.next = node_baru

    def tampilkan_semua(self):
        hasil = []
        saat_ini = self.head
        while saat_ini:
            hasil.append(saat_ini.data)
            saat_ini = saat_ini.next
        return hasil

# 2. STRUKTUR DATA 2: Stack (Untuk Riwayat Aktivitas)
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if not self.is_empty() else None
    def is_empty(self): return len(self.items) == 0

riwayat = Stack()

# FUNGSI SORTING (Bubble Sort) - Tambahan agar sesuai syarat
def urutkan_buku_berdasarkan_tahun(data_list):
    n = len(data_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if int(data_list[j]['tahun']) > int(data_list[j+1]['tahun']):
                data_list[j], data_list[j+1] = data_list[j+1], data_list[j]
    return data_list

# FUNGSI SEARCHING (Linear Search) - Tambahan agar sesuai syarat
def cari_buku_berdasarkan_id(data_list, id_cari):
    for buku in data_list:
        if buku['id'] == id_cari:
            return buku
    return None

# Fungsi simpan & baca CSV
def simpan_ke_csv(daftar_buku, nama_file="perpustakaan.csv"):
    with open(nama_file, mode="w", newline="", encoding="utf-8") as f:
        penulis = csv.writer(f)
        penulis.writerow(["ID", "Judul", "Penulis", "Tahun"])
        for buku in daftar_buku:
            penulis.writerow([buku["id"], buku["judul"], buku["penulis"], buku["tahun"]])

def baca_dari_csv(nama_file="perpustakaan.csv"):
    daftar = LinkedList()
    if not os.path.exists(nama_file): return daftar
    with open(nama_file, mode="r", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        for baris in pembaca:
            daftar.tambah_di_akhir({"id": baris["ID"], "judul": baris["Judul"], "penulis": baris["Penulis"], "tahun": baris["Tahun"]})
    return daftar

def menu():
    while True:
        daftar_buku = baca_dari_csv()
        semua_data = daftar_buku.tampilkan_semua()
        
        print("\n=== SISTEM PERPUSTAKAAN ===")
        print("1. Tambah Buku (Create)")
        print("2. Lihat Semua Buku (Read)")
        print("3. Ubah Data Buku (Update)")
        print("4. Hapus Buku (Delete)")
        print("5. Cari Buku (Searching)")
        print("6. Urutkan Buku Berdasarkan Tahun (Sorting)")
        print("7. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            id_buku = input("ID Buku: ")
            judul = input("Judul: ")
            penulis = input("Penulis: ")
            tahun = input("Tahun Terbit: ")
            daftar_buku.tambah_di_akhir({"id": id_buku, "judul": judul, "penulis": penulis, "tahun": tahun})
            simpan_ke_csv(daftar_buku.tampilkan_semua())
            riwayat.push(f"Menambah buku ID {id_buku}")
            print("✅ Buku berhasil ditambahkan!")

        elif pilihan == "2":
            if not semua_data: print("⚠️ Belum ada data.")
            else:
                for b in semua_data:
                    print(f"ID: {b['id']} | Judul: {b['judul']} | Penulis: {b['penulis']} | Tahun: {b['tahun']}")

        elif pilihan == "3":
            id_cari = input("ID yang diubah: ")
            buku = cari_buku_berdasarkan_id(semua_data, id_cari)
            if buku:
                buku["judul"] = input(f"Judul ({buku['judul']}): ") or buku["judul"]
                buku["penulis"] = input(f"Penulis ({buku['penulis']}): ") or buku["penulis"]
                buku["tahun"] = input(f"Tahun ({buku['tahun']}): ") or buku["tahun"]
                simpan_ke_csv(semua_data)
                print("✅ Berhasil diubah!")
            else: print("❌ ID tidak ditemukan.")

        elif pilihan == "4":
            id_hapus = input("ID yang dihapus: ")
            data_baru = [b for b in semua_data if b["id"] != id_hapus]
            if len(data_baru) < len(semua_data):
                simpan_ke_csv(data_baru)
                print("✅ Berhasil dihapus!")
            else: print("❌ ID tidak ditemukan.")

        elif pilihan == "5": # Fitur Searching
            id_cari = input("Cari ID Buku: ")
            hasil = cari_buku_berdasarkan_id(semua_data, id_cari)
            if hasil: print(f"Ditemukan: {hasil['judul']} oleh {hasil['penulis']}")
            else: print("❌ Tidak ditemukan.")

        elif pilihan == "6": # Fitur Sorting
            data_urut = urutkan_buku_berdasarkan_tahun(semua_data)
            print("--- Buku Diurutkan Berdasarkan Tahun ---")
            for b in data_urut:
                print(f"{b['tahun']} - {b['judul']}")

        elif pilihan == "7":
            print("👋 Keluar...")
            break

if __name__ == "__main__":
    menu()