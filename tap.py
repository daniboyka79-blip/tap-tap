#!/data/data/com.termux/files/usr/bin/env python
import os
import re
import time
import random
import subprocess

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.strip(), res.stderr.strip()

def check_adb():
    out, _ = run_cmd(["adb", "devices"])
    lines = [l for l in out.splitlines()[1:] if "\tdevice" in l]
    return len(lines) > 0

def get_screen_center():
    out, _ = run_cmd(["adb", "shell", "wm", "size"])
    m = re.search(r"(\d+)x(\d+)", out)
    if m:
        w, h = int(m.group(1)), int(m.group(2))
        return w // 2, h // 2
    return 540, 1170

def pair_and_connect():
    print(f"\n{YELLOW}--- Wireless Debugging ማገናኛ ---{RESET}")
    print("Settings > Developer options > Wireless debugging ክፈት።")
    p_port = input("1) 'Pair device with pairing code' ስትነካ የሚመጣውን Port ጻፍ (ቀድሞ Pair ካደረግክ Enter ተጫን): ").strip()
    if p_port:
        p_code = input("   ባለ 6 አሃዝ Pairing Code ጻፍ: ").strip()
        out, err = run_cmd(["adb", "pair", f"127.0.0.1:{p_port}", p_code])
        print(f"{CYAN}{out or err}{RESET}")
    c_port = input("2) ዋናው Wireless debugging ገጽ ላይ ከ : በኋላ ያለውን Port ቁጥር ጻፍ: ").strip()
    if c_port:
        out, err = run_cmd(["adb", "connect", f"127.0.0.1:{c_port}"])
        print(f"{GREEN}{out or err}{RESET}")

def start_unlimited_tap(min_delay, max_delay):
    if not check_adb():
        print(f"{RED}[!] ADB አልተገናኘም! መጀመሪያ በምርጫ [3] Wireless Debugging አገናኝ።{RESET}")
        time.sleep(2)
        return

    cx, cy = get_screen_center()
    print(f"\n{GREEN}[✔] የስክሪን መሃል ተገኝቷል: ({cx}, {cy}){RESET}")
    print(f"{YELLOW}[*] አሁን TikTok Live ክፈት! ከ 5 ሰከንድ በኋላ Unlimited Tap ይጀምራል...{RESET}")
    for i in range(5, 0, -1):
        print(f"\r⏳ {i} ሰከንድ... ", end="", flush=True)
        time.sleep(1)

    print(f"\n{GREEN}[🔥] Unlimited Tap-Tap ተጀምሯል! ለማቆም Termux ላይ CTRL + C ተጫን።{RESET}\n")
    proc = subprocess.Popen(
        ["adb", "shell"],
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )

    taps = 0
    try:
        while True:
            x = cx + random.randint(-28, 28)
            y = cy + random.randint(-35, 35)
            proc.stdin.write(f"input tap {x} {y}\n")
            proc.stdin.flush()
            taps += 1
            if taps % 10 == 0:
                print(f"\r❤️ የተላኩ Tap ብዛት (Unlimited): {taps:,}", end="", flush=True)
            time.sleep(random.uniform(min_delay, max_delay))
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] ቆሟል። በድምሩ {taps:,} ጊዜ Tap ተደርጓል።{RESET}")
    except BrokenPipeError:
        print(f"\n\n{RED}[!] ግንኙነቱ ተቋርጧል። Wireless Debugging መብራቱን አረጋግጥ።{RESET}")
    finally:
        try:
            proc.terminate()
        except Exception:
            pass
        time.sleep(1.5)

def main():
    while True:
        os.system("clear")
        status = f"{GREEN}CONNECTED ✔{RESET}" if check_adb() else f"{RED}NOT CONNECTED ✖{RESET}"
        print(f"{CYAN}=== TikTok Unlimited Tap-Tap (Termux + ADB) ==={RESET}")
        print(f"ADB Status: {status}\n")
        print("[1] 🔥 Start Unlimited Tap-Tap (Safe Mode — Like እንዲቆጠር)")
        print("[2] ⚡ Start Turbo Unlimited Tap-Tap (በጣም ፈጣን)")
        print("[3] 🔗 Wireless Debugging አገናኝ (Pair / Connect)")
        print("[q] ውጣ")
        ch = input("\nምረጥ > ").strip().lower()

        if ch == "1":
            start_unlimited_tap(0.08, 0.16)
        elif ch == "2":
            start_unlimited_tap(0.02, 0.05)
        elif ch == "3":
            pair_and_connect()
            time.sleep(1.5)
        elif ch == "q":
            break

if __name__ == "__main__":
    main()
