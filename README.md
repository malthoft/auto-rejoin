Auto Rejoin Roblox Private Server (Rooted Android)
This Python script monitors your gameplay status and automatically rejoins a Private Server if a switch to a public server or a disconnection is detected.

✨ Features
✅ Automatic server switch detection (Private → Public) using Game ID tracking
✅ Auto rejoin Private Server within 10-30 seconds
✅ Real-time in-game status monitoring
✅ SELinux auto-configuration for maximum compatibility
✅ Clean terminal output with timestamps
✅ New: Auto cookie extractor script included
✅ Support for Cloud Phones & PC Emulators (with root)
📋 Requirements
Rooted Android Device (Required - Magisk/KernelSU)
Physical Android phone/tablet
Cloud phone (Redfinger, NOX Cloud, etc.)
PC Emulator (BlueStacks, LDPlayer, NoxPlayer, MEmu - with root enabled)
Termux app installed (Recommended: F-Droid version)
⚠️ Important: Do not use the Google Play Store version (it is outdated).
Download from F-Droid or GitHub Releases.
Roblox app installed
Roblox Cookie (.ROBLOSECURITY) for Game ID tracking
🔧 Installation
1. Setup Termux
Open Termux and run:

pkg update && pkg upgrade
pkg install python
pip install requests python-dotenv psutil
2. Setup Storage Permission
termux-setup-storage
Allow access when prompted.

3. Download/Copy Script
Save the script in an accessible folder (e.g., /sdcard):

git clone https://github.com/Galkurta/Auto-Rejoin.git
cd Auto-Rejoin
⚙️ Configuration (.env)
1. Run Setup Script (Recommended)
The easiest way to configure the script is to run:

python setup.py
This will guide you through creating the .env file interactively.

2. Manual Configuration
Create a file named .env in the same folder as main.py and add the following:

# Private Server Link
PS_LINK=https://www.roblox.com/share?code=YOUR_CODE&type=Server

# Your Roblox User ID
USER_ID=12345678

# Monitoring Settings
CHECK_INTERVAL=30
RESTART_DELAY=15

# Roblox Cookie (Specific to the account used for checking)
ROBLOX_COOKIE=_|WARNING:-DO-NOT-SHARE-THIS...

# Discord Webhook (Optional)
DISCORD_ENABLED=true
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_NAME=Auto Rejoin Bot (Android)
DISCORD_MENTION_USER=YOUR_DISCORD_USER_ID_OR_ROLE
DISCORD_NOTIFY_ON_START=true
DISCORD_NOTIFY_ON_REJOIN=true
DISCORD_NOTIFY_ON_ERROR=true
Parameters Explanation
Variable	Description
PS_LINK	Your Private Server Link.
USER_ID	Your Roblox User ID.
CHECK_INTERVAL	How often to check status (in seconds). Default: 30.
RESTART_DELAY	Wait time for game to load (in seconds). Default: 15.
ROBLOX_COOKIE	Required for Game ID/Universe ID tracking.
DISCORD_ENABLED	Set to true to enable Discord notifications.
DISCORD_WEBHOOK_URL	Your Discord Webhook URL.
DISCORD_MENTION_USER	User/Role ID to ping (e.g., 123456...). Leave empty if none.
🚀 How to Run
Method 1: Using su (Recommended)
cd /sdcard/Auto-Rejoin
su
python main.py
Method 2: Using tsu (Alternative)
cd /sdcard/Auto-Rejoin
tsu
python main.py
Ensure you grant Root permissions when the Magisk/KernelSU popup appears!

📊 Normal Output
==================================================
  🎮 Auto Rejoin Roblox Private Server
==================================================

✓ Root access granted
📋 Configuration:
   • User ID: 12345678
   • Check Interval: 10s
   • Restart Delay: 30s
   • Game ID Tracking: Enabled ✓

🔄 Starting Roblox...
⏳ Waiting 60s for game to load...
🔍 Detecting private server...
✓ Game ID: 49073d8d-d97...

==================================================
  📊 Monitoring Status
==================================================

[14:23:15] 🟢 In-Game (Private Server)
[14:23:25] 🟢 In-Game (Private Server)
[14:23:35] 🔴 Server switched - Rejoining...
           ✓ Rejoined successfully
[14:24:15] 🟢 In-Game (Private Server)
🔍 How It Works
This script uses Game ID Tracking to detect server switches:

On Start: The script opens the Private Server and records its Game ID.
Monitoring: Every X seconds (according to check_interval), the script:
Checks if Roblox is running.
Checks the current Game ID via the Roblox Presence API.
Compares it with the Private Server's Game ID.
Auto Rejoin: If the Game ID changes (moved to a public server), the script will:
Force stop Roblox.
Reopen the Private Server link.
Update the expected Game ID.
💻 Support for Cloud Phone & PC Emulator
Cloud Phone (Redfinger, NOX Cloud, etc.)
✅ Compatible - The script works on cloud phones provided:

Cloud phone has root access.
Termux can be installed.
Stable internet connection.
Setup:

Install Termux on the cloud phone.
Follow the installation instructions above.
Run the script as usual.
Benefits:

Runs 24/7 without relying on a physical device.
Does not drain your main device's battery.
Accessible from anywhere.
PC Emulator (BlueStacks, LDPlayer, NoxPlayer, MEmu)
✅ Compatible with root requirement - Choose an emulator that supports root:

Emulator	Root Support	Recommended
LDPlayer	✅ Built-in	⭐⭐⭐⭐⭐ Recommended
NoxPlayer	✅ Built-in	⭐⭐⭐⭐
MEmu	✅ Built-in	⭐⭐⭐⭐
BlueStacks 5	⚠️ Needs Magisk	⭐⭐⭐
How to Enable Root:

LDPlayer:

Open Settings → Other Settings
Enable "Root permission"
Restart emulator
NoxPlayer:

Click gear icon (Settings)
General tab
Enable "Root startup"
Restart emulator
MEmu:

Open Settings
Enable "ROOT"
Restart emulator
BlueStacks 5:

Install Magisk via recovery
Follow Magisk installation guide
More complex - not recommended for beginners
Performance & Recommendations
Physical Device:

Best for daily use.
Battery efficient with split check_interval 30s.
Most stable.
Cloud Phone:

Best for 24/7 operation.
Independent of physical device.
Requires cloud service subscription.
PC Emulator:

Best for testing/development.
Can run multiple instances.
High RAM usage.
Tip: For 24/7 operation, use a Cloud Phone or a PC that is always on with an emulator.

Cookie Extraction Failed
If getcookie.py can't find your cookie:

Check installed browsers: su -c "pm list packages | grep -E 'chrome|firefox|edge'"
Verify login: Ensure you are logged into Roblox in that browser.
Try manual extraction: Use the manual method described in Configuration.
SELinux Error
# Check status
su -c "getenforce"

# Manually set to Permissive
su -c "setenforce 0"
Game ID Not Detected
Ensure roblox_cookie is correctly set in config.json.
Cookie must be complete and valid (login to browser to verify).
Avoid spaces or extra characters when copy-pasting.
Roblox Not Opening
# Manual test
su -c "am start -a android.intent.action.VIEW -d 'YOUR_PS_LINK' -p com.roblox.client"

# Or test with monkey
su -c "monkey -p com.roblox.client 1"
Script Crash/Error
Ensure Python and requests are installed: pip install requests
Check root permission: su -c "id"
Check error logs for debugging.
⚠️ Security Notes
DO NOT SHARE your config.json file or .ROBLOSECURITY cookie!
This cookie is equivalent to a password - anyone with it can log in as you.
Change your Roblox password periodically for security.
Logging out from all devices will reset the cookie (requires re-setup).
📱 Usage Tips
Set check_interval to 10 for fast detection (more API calls).
Set check_interval to 30 to save battery (slower detection).
restart_delay should be 30-60 seconds depending on your game loading speed.
The script runs continuously until manually stopped (Ctrl+C).
🔄 Auto-Start on Boot (Optional)
To run the script automatically on device boot, use Termux:Boot or Tasker with root.

📝 License
Free to use and modify.

🤝 Support
If there are issues or questions, open an issue in this repository.

Disclaimer: This script is for educational purposes. Use wisely and follow Roblox Terms of Service.
