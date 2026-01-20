import os
import time
import subprocess
import platform
import re
from datetime import datetime
import pathlib

# ============================================================
# CONFIG
# ============================================================
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=818a0e6bdeb0ca49a0fbfbdfb9453cf6&type=Server"
CHECK_INTERVAL = 8          # detik
ANDROID_PACKAGE = "com.roblox.client"

# ============================================================
# LOGGING
# ============================================================
def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

# ============================================================
# DETEKSI GAME ID (SERVER)
# ============================================================
def get_roblox_log_path():
    base = pathlib.Path(os.getenv("LOCALAPPDATA", ""))
    log_dir = base / "Roblox" / "logs"

    if not log_dir.exists():
        return None

    files = list(log_dir.glob("*.log"))
    if not files:
        return None

    newest = max(files, key=lambda f: f.stat().st_mtime)
    return str(newest)


def extract_game_id():
    path = get_roblox_log_path()
    if not path:
        return None

    try:
        with open(path, "r", errors="ignore") as f:
            text = f.read()
    except:
        return None

    match = re.findall(r"GameId: ([0-9a-fA-F\-]+)", text)
    if match:
        return match[-1]  # ambil yang terbaru
    return None


# ============================================================
# ANDROID MODE (ROOT)
# ============================================================
def android_is_running():
    try:
        result = subprocess.check_output(["su", "-c", f"pidof {ANDROID_PACKAGE}"], stderr=subprocess.STDOUT)
        return True if result else False
    except:
        return False


def android_force_stop():
    log("🔴 Menutup Roblox...")
    os.system(f"su -c 'am force-stop {ANDROID_PACKAGE}'")
    time.sleep(2)


def android_open_ps():
    log("🟢 Membuka Private Server...")
    os.system(f"su -c \"am start -a android.intent.action.VIEW -d '{PRIVATE_SERVER_LINK}' -p {ANDROID_PACKAGE}\"")
    time.sleep(10)


# ============================================================
# WINDOWS MODE
# ============================================================
def windows_is_running():
    try:
        output = subprocess.check_output("tasklist", shell=True).decode().lower()
        return "robloxplayerbeta.exe" in output
    except:
        return False


def windows_force_stop():
    log("🔴 Menutup Roblox...")
    os.system("taskkill /F /IM RobloxPlayerBeta.exe >nul 2>&1")
    time.sleep(2)


def windows_open_ps():
    log("🟢 Membuka Private Server...")
    os.system(f'start "" "{PRIVATE_SERVER_LINK}"')
    time.sleep(10)


# ============================================================
# MAIN LOOP
# ============================================================
def main():
    system = platform.system().lower()

    if "windows" in system:
        mode = "windows"
        log("💻 Mode terdeteksi: WINDOWS")
    elif "linux" in system or "android" in system:
        mode = "android"
        log("📱 Mode terdeteksi: ANDROID / EMULATOR ROOT")
    else:
        log("❌ Device tidak didukung.")
        return

    log("=== AUTO REJOIN + PUBLIC SERVER DETECT (NO COOKIE) ===")
    log(f"🔗 PS Link: {PRIVATE_SERVER_LINK}\n")

    # buka PS pertama kali
    if mode == "android":
        android_open_ps()
    else:
        windows_open_ps()

    last_game_id = None

    while True:
        # cek apakah Roblox berjalan
        running = android_is_running() if mode == "android" else windows_is_running()

        # cek gameId (khusus Windows)
        game_id = extract_game_id() if mode == "windows" else None

        if running:
            log("🟢 Roblox berjalan.")
        else:
            log("🔴 Roblox tidak berjalan → rejoin...")
            if mode == "android":
                android_force_stop()
                android_open_ps()
            else:
                windows_force_stop()
                windows_open_ps()
            time.sleep(CHECK_INTERVAL)
            continue

        # DETEKSI PINDAH SERVER (HANYA WINDOWS)
        if mode == "windows":
            if game_id and last_game_id and game_id != last_game_id:
                log("⚠️ Server berubah → kemungkinan pindah ke publik!")
                windows_force_stop()
                windows_open_ps()

        if game_id:
            last_game_id = game_id

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
