"""
Author: Raihan Rizqi Muhtadiin (raihanrizqi91@ui.ac.id)
Co-author: (credited)

Last update: 18 November 2019
"""

# Menyiapkan modul-modul bawaan Python untuk digunakan dalam program ini.
import csv
import os

tempat_data = {} # Bahan utama dalam program ini, yakni sebuah global dictionary yang kosong
panduan_prog = """\tPanduan daftar perintah:
\tIMPOR\t\t Mengimpor data dari file CSV. Impor dulu sebelum perintah yang lain. ex: IMPOR inifileku.csv
\tEKSPOR\t\t Mengekspor data file CSV, ex: EKSPOR itufileku.csv
\tCARINAMA\t Mencari nama budaya, ex: CARINAMA Ayam Kodok
\tCARITIPE\t Mencari tipe budaya, ex: CARITIPE Minuman
\tCARIPROV\t Mencari provinsi asal budaya, ex: CARIPROV Nusa Tenggara Barat
\tTAMBAH\t\t Menambahkan data baru ke dalam file CSV, formatnya: nama;;;tipe;;;provinsi;;;referensi
\tUPDATE\t\t Menimpa suatu baris data lama dengan baris data baru, formatnya: nama;;;tipe;;;provinsi;;;referensi
\tHAPUS\t\t Menghapus data yang ada, ex: HAPUS Ketoprak
\tSTAT\t\t Menampilkan jumlah total warisan budaya
\tSTATTIPE\t Menampilkan jumlah warisan budaya per tipe dari terbanyak ke tersedikit
\tSTATPROV\t Menampilkan jumlah warisan budaya per provinsi dari terbanyak ke tersedikit
\tBERSIHKAN\t Membersihkan CLI
\tKELUAR\t\t Keluar dari program\n"""

def header():
    # Bagian ini sekadar untuk header program.
    print("\t", "="*70)
    print("\t\t\t\tBudayaKB Lite v1.1")
    print("\t\t~Kalau bukan kita yang melestarikan budaya, siapa lagi?~")
    print("\t", "="*70)

def panduan():
    # Mencetak panduan penggunaan program.
    print(panduan_prog)

def parsing(input_perintah):
    # Menyatukan input dari user untuk selanjutnya disebut sebagai 'obj_perintah'.
    return " ".join(input_perintah[1:])

def impordata(obj_perintah):
    # Mengimpor data budaya dari file. Sebelumnya, pastikan file yang akan diakses berada dalam directory yang sama dengan program.
    baris_data = []
    with open(obj_perintah, "r") as file_saya:
        for baris in file_saya:
            baris_data = baris.strip("\n").split(",")
            temp_key = baris_data[0]
            temp_val = baris_data[:]
            tempat_data[temp_key] = temp_val
            baris_data = []
            temp_key = []
            temp_val = []
    file_saya.close()
    return tempat_data

def ekspordata(tempat_data, obj_perintah):
    # Mengekspor data budaya dalam file ke file baru. File baru dapat menggunakan ekstensi selain .csv
    with open(obj_perintah, "a", newline = "") as file_saya:
        menulis = csv.writer(file_saya)
        for baris in tempat_data.values():
            menulis.writerow(baris)

def carinama(nama, tempat_data):
    # Mencari data budaya berdasarkan nama. Untuk menampilkan semua data tersedia dalam file, gunakan CARINAMA *
    if nama == "*":
        for key in tempat_data:
            print(",".join(tempat_data[key]))
    else:
        print("{}".format(",".join(tempat_data[nama.title()])))

def caritipe(tipe, tempat_data):
    # Mencari data budaya berdasarkan tipe lalu mencetak semua baris data yang cocok.
    penghitung = 0
    for key, val in tempat_data.items():
        for i in val:
            if tipe.title() == i:
                penghitung += 1
                print("{}".format(",".join(tempat_data[key])))
            else:
                continue
    if penghitung == 0:
        return "{} tidak ditemukan.\n".format(tipe.title())
    else:
        return "*Ditemukan {} {}*\n".format(penghitung, tipe.title())

def cariprovinsi(prov, tempat_data):
    # Mencari data budaya berdasarkan provinsi lalu mencetak semua baris data yang cocok.
    penghitung = 0
    for key, val in tempat_data.items():
        for i in val:
            if prov.title() == i:
                penghitung += 1
                print("{}".format(",".join(tempat_data[key])))
            else:
                continue
    if penghitung == 0:
        return "{} tidak ditemukan.\n".format(prov.title())
    else:
        return "*Ditemukan {} warisan budaya dari {}*\n".format(penghitung, prov.title())

def tambahdata(tambahan_data, tempat_data):
    # Menambahkan baris data budaya baru ke dalam file.
    tambahan_data = tambahan_data.split(";;;")
    if len(tambahan_data) != 4:
        print("Mohon maaf, silakan sesuaikan kembali format TAMBAH data Anda dengan contoh pada panduan program.\n")
    else:
        tempat_data[tambahan_data[0].title()] = tambahan_data
        print("{} ditambahkan.\n".format(tambahan_data[0]))

def updatedata(update_data, tempat_data):
    # Meng-update baris data budaya yang sudah ada dalam file. Jika data budaya termaksud belum ada, gunakan perintah 'TAMBAH'.
    update_data = update_data.split(";;;")
    if update_data[0].title() not in tempat_data:
        print("Mohon maaf, data budaya tersebut belum tersedia pada program. Silakan gunakan perintah TAMBAH.\n")
    else:
        if len(update_data) != 4:
            print("Mohon sesuaikan kembali format penambahan data dengan contoh panduan program")
        else:
            tempat_data[update_data[0]] = update_data
            print("{} di-update.\n".format(update_data[0]))

def hapusdata(data, tempat_data):
    # Menghapus baris data budaya
    try:
        tempat_data.pop(data.title())
        print("{} dihapus.\n".format(data.title()))
    except KeyError:
        print("Mohon maaf, data budaya yang hendak Anda hapus memang sudah tidak ada di file sejak awal.\n")

def statbudaya(tempat_data):
    # Menampilkan statistik data budaya secara keseluruhan.
    return "Terdapat {} warisan budaya dalam data file ini.\n".format(len(tempat_data))

def stattipebudaya(tempat_data):
    # Menampilkan statistik data budaya per tipe, diurutkan dari tipe terbanyak.
    list_tipe = []
    dict_tipe = {}
    for value in tempat_data.values():
        list_tipe.append(value[1])
    for elemen in list_tipe:
        dict_tipe[elemen] = list_tipe.count(elemen)
    dict_tipe_sorted = sorted(dict_tipe.items(), key = lambda kv: kv[1], reverse=True)
    print(dict_tipe_sorted)

def statprovbudaya(tempat_data):
    # Menampilkan statistik data budaya per provinsi, diurutkan dari provinsi terbanyak.
    list_tipe = []
    dict_tipe = {}
    for value in tempat_data.values():
        list_tipe.append(value[2])
    for elemen in list_tipe:
        dict_tipe[elemen] = list_tipe.count(elemen)
    dict_tipe_sorted = sorted(dict_tipe.items(), key = lambda kv: kv[1], reverse=True)
    print(dict_tipe_sorted)

def pembersihan():
    # Membersihkan CLI
    os.system('cls')

def mainprog():
    # Fungsi yang menghubungkan setiap input perintah dari user ke fungsi-fungsi yang sesuai.
    pembersihan()
    header()
    panduan()
    while True:
        try:
            input_perintah = input("> Masukkan perintah: ").split()
            if len(input_perintah) > 1:
                obj_perintah = parsing(input_perintah)
            else:
                obj_perintah = ""
            if input_perintah[0].upper() == "IMPOR":
                try:
                    tempat_data = impordata(obj_perintah)
                    try:
                        print("Terimpor {} baris.\n".format(len(tempat_data)))
                    except UnboundLocalError:
                        print("Mohon maaf, program tidak mendukung ekstensi file yang akan Anda buka.")
                except FileNotFoundError:
                    print("Mohon maaf, file tidak ditemukan.\n")
            elif input_perintah[0].upper() == "EKSPOR":
                try:
                    ekspordata(tempat_data, obj_perintah)
                    with open(obj_perintah, "r") as bukaan_file:
                        penghitung = 0
                        for barisdata in bukaan_file:
                            print(barisdata)
                            penghitung += 1
                    print("Terekspor {} baris.\n".format(penghitung))
                except UnboundLocalError:
                    print("Mohon maaf, tidak ada data untuk diekspor.\n")
            elif input_perintah[0].upper() == "CARINAMA":
                if len(tempat_data) != 0:
                    try:
                        carinama(obj_perintah, tempat_data)
                    except KeyError:
                        print("Mohon maaf, {} tidak terdapat dalam data program.\n".format(obj_perintah).title())
                else:
                    print("Mohon maaf, file kosong tidak dapat diproses. Harap impor file lain yang tidak kosong.\n")
            elif input_perintah[0].upper() == "CARITIPE":
                print(caritipe(obj_perintah, tempat_data))
            elif input_perintah[0].upper() == "CARIPROV":
                print(cariprovinsi(obj_perintah, tempat_data))
            elif input_perintah[0].upper() == "TAMBAH":
                tambahdata(obj_perintah, tempat_data)
            elif input_perintah[0].upper() == "UPDATE":
                updatedata(obj_perintah, tempat_data)
            elif input_perintah[0].upper() == "HAPUS":
                hapusdata(obj_perintah, tempat_data)
            elif input_perintah[0].upper() == "STAT":
                print(statbudaya(tempat_data))
            elif input_perintah[0].upper() == "STATTIPE":
                stattipebudaya(tempat_data)
            elif input_perintah[0].upper() == "STATPROV":
                statprovbudaya(tempat_data)
            elif input_perintah[0].upper() == "BERSIHKAN":
                pembersihan()
                header()
                panduan()
            elif input_perintah[0].upper() == "KELUAR":
                print("\tSpecial thanks to:")
                print("\tGani Ilham Irsyadi")
                print("\tDennis Al Baihaqi Walangadi")
                print("\tFrancis Wibisono")
                print("\tAdam Syauqi Medise\n")
                print("\t~Sampai jumpa, jangan lupa mencintai warisan budaya Indonesia!~")
                break
            else:
                print("Mohon maaf, perintah yang Anda input tidak valid.\n")
        except IndexError:
            print("Mohon maaf, Anda belum menginput perintah apapun. Untuk keluar program, ketik KELUAR.\n")
        except UnboundLocalError:
            print("Mohon maaf, Anda harus impor file data terlebih dahulu sebelum menggunakan perintah yang lain.\n")

# Program yang telah termodularisasi menjadi main program lalu dijalankan melalui special variable berikut:
if __name__ == "__main__":
    mainprog()
