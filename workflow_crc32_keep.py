import os
import zlib
import shutil

def get_crc32(file_path):
    """Fungsi untuk menghitung nilai CRC32 dari sebuah file."""
    with open(file_path, 'rb') as f:
        crc = 0
        while chunk := f.read(8192):
            crc = zlib.crc32(chunk, crc)
    return f"{crc & 0xFFFFFFFF:08X}"

def main():
    # '.' artinya script akan berjalan dari root folder dan mencari ke seluruh sub-folder
    root_dir = '.' 
    
    print("Memulai proses CLONE Modular: Mencari ke seluruh sub-folder...\n")
    print("-" * 70)
    
    # os.walk digunakan untuk menelusuri semua folder dan sub-folder secara rekursif
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Abaikan folder internal git agar tidak ikut diproses
        if '.github' in dirpath or '.git' in dirpath:
            continue
            
        for filename in filenames:
            # Cari file yang memiliki ekstensi .dff atau .txd
            if filename.lower().endswith(('.dff', '.txd')):
                # Path lengkap ke file asli
                old_path = os.path.join(dirpath, filename)
                
                # Hitung CRC32
                crc32_hash = get_crc32(old_path)
                
                # Buat nama baru CUMA 0x[CRC32] tanpa ekstensi
                new_filename = f"0x{crc32_hash}"
                # Path baru disamakan dengan dirpath (folder tempat file asli berada)
                new_path = os.path.join(dirpath, new_filename)
                
                # Lewati jika file clone sudah pernah dibuat sebelumnya di folder tersebut
                if os.path.exists(new_path):
                    print(f"[SKIP] {new_filename} sudah ada di {dirpath}. Melewati.")
                    continue
                
                # Proses Clone (Copy) ke path yang sama
                try:
                    shutil.copy2(old_path, new_path)
                    print(f"[BERHASIL] {dirpath}/{filename}  ->  {new_filename}")
                except Exception as e:
                    print(f"[ERROR] Gagal menyalin {filename} di {dirpath}: {e}")
                    
    print("-" * 70)
    print("Selesai! File CRC32 berhasil dibuat di path file aslinya masing-masing.")

if __name__ == "__main__":
    main()
