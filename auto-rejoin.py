import subprocess
import time
import psutil
import re
import webbrowser

# ==========================================
# MASUKKAN LINK PRIVATE SERVER KAMU DI SINI
# ==========================================
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=818a0e6bdeb0ca49a0fbfbdfb9453cf6&type=Server"

# ==========================================
# FUNGSI: Ambil kode Private Server dari URL
# ==========================================
def extract_private_server_code(url):
    m = re.search(r'code=([A-Za-z0-9]+)', url)
    return m.group(1) if m else None

# ==========================================
# KONVERSI LINK SHARE MENJADI roblox://
# ==========================================
def build_roblox_deeplink(code):
    # Link resmi format baru Roblox
    return f"roblox://experiences/start?privateServerLinkCode={code}"

# ==========================================
# FUNGSI: Buka Private Server
# ==========================================
def join_private_server():
    print("[INFO] Membuka Private Server...")
    webbrowser.open(ROBLOX_DEEPLINK)

# ==========================================
# CEK apakah Roblox sedang berjalan
# ==========================================
def is_roblox_running():
    for p in psutil.process_iter(attrs=['name']):
        try:
            if "RobloxPlayer" in p.info['name'] or "RobloxPlayerBeta" in p.info['name']:
                return True
        except:
            pass
    return False

# ==========================================
# CEK apakah user masuk Server Publik
# (mendeteksi "RobloxCrashHandler" atau "RobloxPlayerBeta" restart)
# ==========================================
def detect_public_server():
    # Metode sederhana: Roblox restart dalam <10 detik = biasanya pindah server
    # Kamu bisa tambah metode lain jika ingin lebih akurat.
    return False  # placeholder bila tidak ingin deteksi tambahan

# ==========================================
# FUNGSI: Pantau Roblox
# ==========================================
def monitor():
    print("[SYSTEM] Auto Rejoin dimulai.")
    roblox_was_running = False

    while True:
        running = is_roblox_running()

        # Roblox sebelumnya aktif → sekarang tidak → otomatis reconnect
        if roblox_was_running and not running:
            print("[DETECT] Roblox disconnect / crash / pindah server.")
            time.sleep(2)
            join_private_server()

        # Roblox sedang jalan tapi kamu pindah ke server publik → auto rejoin
        if running and detect_public_server():
            print("[DETECT] Pindah ke server publik. Memaksa rejoin...")
            kill_roblox()
            time.sleep(2)
            join_private_server()

        roblox_was_running = running
        time.sleep(1)

# ==========================================
# MATIKAN ROBLOX
# ==========================================
def kill_roblox():
    for p in psutil.process_iter():
        try:
            if "RobloxPlayer" in p.name() or "RobloxPlayerBeta" in p.name():
                p.kill()
        except:
            pass

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("[INFO] Mengambil Private Server Link Code...")
    code = extract_private_server_code(PRIVATE_SERVER_LINK)

    if not code:
        print("[ERROR] Kode Private Server gagal ditemukan!")
        exit()

    ROBLOX_DEEPLINK = build_roblox_deeplink(code)
    print(f"[INFO] DeepLink Roblox: {ROBLOX_DEEPLINK}")

    # pertama kali langsung join
    join_private_server()

    # mulai mode pantau
    monitor()
