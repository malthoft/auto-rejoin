import os
import time
import subprocess
import platform
from datetime import datetime

# ============================
# CONFIG
# ============================
PRIVATE_SERVER_LINK = "https://www.roblox.com/share?code=818a0e6bdeb0ca49a0fbfbdfb9453cf6&type=Server"
CHECK_INTERVAL = 10          # detik
ANDROID_PACKAGE = "com.roblox.client"

# ============================
# LOGGING
# ============================
def log(msg):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

# ============================
# ANDROID MODE (ROOT)
# ============================
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


# ============================
# WINDOWS MODE
# ============================
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


# ============================
# MAIN LOOP
# ============================
def main():
    system = platform.system().lower()

    if "android" in system or "linux" in system:
        mode = "android"
        log("📱 Mode: ANDROID/EMULATOR")
    elif "windows" in system:
        mode = "windows"
        log("💻 Mode: WINDOWS")
    else:
        log("❌ Device tidak didukung.")
        return

    log("=== AUTO REJOIN PRIVATE SERVER ===")
    log(f"🔗 PS Link: {PRIVATE_SERVER_LINK}\n")

    # buka PS pertama kali
    if mode == "android":
        android_open_ps()
    else:
        windows_open_ps()

    while True:
        if mode == "android":
            running = android_is_running()
        else:
            running = windows_is_running()

        if running:
            log("🟢 Roblox berjalan.")
        else:
            log("🔴 Roblox tidak berjalan → Rejoin...")
            if mode == "android":
                android_force_stop()
                android_open_ps()
            else:
                windows_force_stop()
                windows_open_ps()

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
