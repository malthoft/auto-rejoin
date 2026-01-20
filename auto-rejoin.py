import os
import time
import re
import requests
import webbrowser

# ====================================================
# MASUKKAN LINK PRIVATE SERVER KAMU DI SINI
# ====================================================
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=818a0e6bdeb0ca49a0fbfbdfb9453cf6&type=Server"

# ====================================================
# FUNGSI: Ambil kode Private Server dari URL
# ====================================================
def extract_private_server_code(url):
    m = re.search(r'code=([A-Za-z0-9]+)', url)
    return m.group(1) if m else None

# ====================================================
# Buat deep link roblox://
# ====================================================
def build_roblox_deeplink(code):
    return f"roblox://experiences/start?privateServerLinkCode={code}"

# ====================================================
# Buka Roblox dengan private server
# ====================================================
def join_private_server():
    print("[INFO] Membuka Private Server...")
    os.system(f"am start -a android.intent.action.VIEW -d \"{ROBLOX_DEEPLINK}\"")

# ====================================================
# DETEKSI: Apakah user sedang di server publik?
# Menggunakan pengecekan log Roblox localstorage.json
# ====================================================
def is_in_public_server():
    roblox_path = "/sdcard/Android/data/com.roblox.client/files/logs/"

    try:
        files = os.listdir(roblox_path)
        target = None

        # ambil file log terbaru
        for f in sorted(files, reverse=True):
            if "Player" in f:
                target = f
                break

        if not target:
            return False

        with open(roblox_path + target, "r", errors="ignore") as f:
            content = f.read()

        # Jika PrivateServerLinkCode tidak ada, berarti user di public server
        if PRIVATE_SERVER_CODE not in content:
            return True

        return False

    except Exception:
        return False

# ====================================================
# DETEKSI: Roblox ditutup / crash
# Termux method: cek proses com.roblox.client di android
# ====================================================
def is_roblox_running():
    out = os.popen("pidof com.roblox.client").read()
    return out.strip() != ""

# ====================================================
# Matikan Roblox
# ====================================================
def kill_roblox():
    os.system("am force-stop com.roblox.client")

# ====================================================
# MODE PANTAU
# ====================================================
def monitor():
    print("[SYSTEM] Auto Rejoin dimulai...")
    last_running = False

    while True:
        running = is_roblox_running()

        # Roblox sebelumnya berjalan → sekarang tidak → reconnect
        if last_running and not running:
            print("[DETECT] Roblox crash/disconnect!")
            time.sleep(2)
            join_private_server()

        # Roblox hidup tapi user pindah ke server publik
        if running:
            if is_in_public_server():
                print("[DETECT] Kamu dipindah ke SERVER PUBLIK!")
                print("[ACTION] Restart & Rejoin ke Private Server")

                kill_roblox()
                time.sleep(2)
                join_private_server()

        last_running = running
        time.sleep(2)

# ====================================================
# MAIN
# ====================================================
if __name__ == "__main__":
    print("[INFO] Mengambil Private Server Link Code...")
    PRIVATE_SERVER_CODE = extract_private_server_code(PRIVATE_SERVER_LINK)

    if not PRIVATE_SERVER_CODE:
        print("[ERROR] Kode Private Server gagal dibaca!")
        exit()

    ROBLOX_DEEPLINK = build_roblox_deeplink(PRIVATE_SERVER_CODE)
    print(f"[INFO] DeepLink Roblox OK: {ROBLOX_DEEPLINK}")

    # Pertama kali langsung masuk
    join_private_server()

    # Mulai monitoring
    monitor()
