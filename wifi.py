import subprocess
import re

def get_wifi_profiles():
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='utf-8', errors='ignore')
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)
        return [p.strip() for p in profiles]
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return []

def get_wifi_password(profile):
    try:
        # Surround profile name with quotes to handle spaces/special characters
        output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profile', f'name="{profile}"', 'key=clear'],
            encoding='utf-8',
            errors='ignore'
        )
        password = re.search(r"Key Content\s*:\s*(.*)", output)
        return password.group(1) if password else None
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return None

if __name__ == "__main__":
    profiles = get_wifi_profiles()
    for profile in profiles:
        password = get_wifi_password(profile)
        print(f"WiFi Name: {profile}, Password: {password}")