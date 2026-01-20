import os
import time
import re

# ============================================
# LINK PRIVATE SERVER KAMU
# ============================================
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=818a0e6bdeb0ca49a0fbfbdfb9453cf6&type=Server"


# ============================================
# Ambil kode dari link share
# ============================================
def extract_ps_code(url):
    m = re.search(r"code=([A-Za-z0-9]+)", url)
    return m.group(1) if m else None


# ============================================
# Bangun deeplink roblox
# ============================================
def build_deeplink(code):
    return f"roblox://experiences/start?privateServerLinkCode={code}"


# ============================================
# Cek apakah Roblox berjalan
# ============================================
def roblox_running():
    out = os.popen("pidof com.roblox.client").read()
    return out.strip() != ""


# ============================================
# Matikan Roblox
# ============================================
def kill_roblox():
    os.system("am force-stop com.roblox.client")


# ============================================
# FORCE REJOIN ROBLOX PRIVATE SERVER
# ============================================
def full_force_rejoin():

    print("[ACTION] Membuka Roblox App...")
    os.system("am start -n com.roblox.client/com.roblox.client.Activity")

    time.sleep(4)  # WAJIB beri waktu untuk initializing

    print("[ACTION] Mengirim DeepLink Private Server...")
    os.system(f"am start -a android.intent.action.VIEW -d \"{DEEPLINK}\"")

    # Deep link kedua (lebih akurat)
    time.sleep(3)
    print("[ACTION] DeepLink kedua (jamin berhasil)...")
    os.system(f"am start -a android.intent.action.VIEW -d \"{DEEPLINK}\"")

    # Loop sampai Roblox benar-benar berjalan
    for i in range(10):
        if roblox_running():
            print("[INFO] Roblox berhasil launch, menunggu load...")
            break
        time.sleep(1)

    time.sleep(3)
    print("[INFO] Rejoin attempt selesai.\n")


# ============================================
# DETEKSI SERVER PUBLIC VIA LOGS
# ============================================
def is_public_server():
    logpath = "/sdcard/Android/data/com.roblox.client/files/logs/"
    try:
        files = os.listdir(logpath)
        files = sorted(files, reverse=True)
        for f in files:
            if "Player" in f:
                target = f
                break
        else:
            return False

        content = open(logpath + target, "r", errors="ignore").read()
        return PRIVATE_CODE not in content

    except:
        return False


# ============================================
# MAIN MONITOR
# ============================================
def monitor():
    print("[SYSTEM] Monitoring dimulai...\n")
    last_state = False

    while True:
        active = roblox_running()

        # Roblox baru crash / keluar
        if last_state and not active:
            print("[DETECT] Roblox crash / force exit.")
            time.sleep(2)
            full_force_rejoin()

        # Roblox hidup tapi user pindah ke server publik
        if active and is_public_server():
            print("[DETECT] Kamu dipindah ke SERVER PUBLIK!")
            print("[ACTION] Restart Roblox dan Rejoin...")
            kill_roblox()
            time.sleep(2)
            full_force_rejoin()

        last_state = active
        time.sleep(2)


# ============================================
# MAIN PROGRAM
# ============================================
if __name__ == "__main__":
    PRIVATE_CODE = extract_ps_code(PRIVATE_SERVER_LINK)
    if not PRIVATE_CODE:
        print("[ERROR] Private server code tidak ditemukan!")
        exit()

    DEEPLINK = build_deeplink(PRIVATE_CODE)
    print("[INFO] DeepLink:", DEEPLINK)

    # pertama kali langsung force-rejoin
    full_force_rejoin()

    # mulai monitoring auto rejoin
    monitor()
