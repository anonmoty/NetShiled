import sys, time, os, random
from colorama import Fore, Back, Style, init
init(autoreset=True)

class Banner:
    @classmethod
    def _glitch(cls, text, n=2):
        g = "▓▒░█▄▀■□"
        for _ in range(n):
            out = ""
            for ch in text:
                if ch != " " and random.random() < 0.12:
                    out += random.choice([Fore.CYAN, Fore.GREEN]) + random.choice(g)
                else:
                    out += Fore.LIGHTCYAN_EX + ch
            sys.stdout.write("\r" + out)
            sys.stdout.flush()
            time.sleep(0.04)
        sys.stdout.write("\r" + text + Style.RESET_ALL + "\n")

    @classmethod
    def show(cls):
        os.system("clear" if os.name == "posix" else "cls")

        for i in range(15):
            sp = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"[i % 10]
            sys.stdout.write("\r  " + Fore.CYAN + sp + Fore.WHITE +
                             " Loading NetShield [" + str(i*7) + "%]")
            sys.stdout.flush()
            time.sleep(0.05)
        print("\r  " + Fore.GREEN + "✓ Shield activated!              ")
        time.sleep(0.3)

        logo = [
            "",
            Fore.LIGHTCYAN_EX + Style.BRIGHT +
            "    ███╗   ██╗███████╗████████╗███████╗██╗  ██╗██╗███████╗██████╗",
            Fore.LIGHTCYAN_EX + Style.BRIGHT +
            "    ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██║  ██║██║██╔════╝██╔══██╗",
            Fore.CYAN + Style.BRIGHT +
            "    ██╔██╗ ██║█████╗     ██║   ███████╗███████║██║█████╗  ██║  ██║",
            Fore.CYAN + Style.BRIGHT +
            "    ██║╚██╗██║██╔══╝     ██║   ╚════██║██╔══██║██║██╔══╝  ██║  ██║",
            Fore.CYAN +
            "    ██║ ╚████║███████╗   ██║   ███████║██║  ██║██║███████╗██████╔╝",
            Fore.CYAN +
            "    ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚═════╝",
            "",
            Fore.LIGHTGREEN_EX + "    v1.0 | Personal Web Protection | Block Scam & Phishing",
            "",
        ]
        for line in logo:
            cls._glitch(line, n=2)
            time.sleep(0.01)

        shield = [
            Fore.LIGHTCYAN_EX + "        ╔═══╗",
            Fore.LIGHTCYAN_EX + "       ║ " + Fore.GREEN + "✓" + Fore.LIGHTCYAN_EX + " ║",
            Fore.LIGHTCYAN_EX + "       ║   ║",
            Fore.LIGHTCYAN_EX + "        ╚═╦═╝",
            Fore.LIGHTCYAN_EX + "          ║",
            Fore.CYAN + "      SHIELD ON",
        ]
        for line in shield:
            print("  " + line + Style.RESET_ALL)
            time.sleep(0.04)

        print()
        info = [
            Fore.CYAN + "    ╔" + "═" * 60 + "╗",
            Fore.CYAN + "    ║" + Fore.LIGHTCYAN_EX + " 🛡️ NetShield v1.0 " + Fore.LIGHTBLACK_EX + "│" +
            Fore.LIGHTGREEN_EX + " Personal Web Protection         " + Fore.CYAN + "   ║",
            Fore.CYAN + "    ╠" + "═" * 60 + "╣",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 🔗 URL Blocker  : Block scam/phishing URLs        " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 🌐 IP Blocker   : Block malicious IPs             " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 🎣 Phishing     : Detect & block fake websites    " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 📱 Link Guard   : Scan links before opening       " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 🔄 Threat Feed  : Auto-update blocklist           " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ║" + Fore.WHITE +
            " 🛡️ Status       : " + Fore.GREEN + "ACTIVE & PROTECTING" + Fore.WHITE +
            "              " + Fore.CYAN + "     ║",
            Fore.CYAN + "    ╚" + "═" * 60 + "╝",
        ]
        for line in info:
            print(line)
            time.sleep(0.03)
        print(Style.RESET_ALL + "\n")

    @classmethod
    def menu(cls):
        C = Fore.CYAN; W = Fore.WHITE; LC = Fore.LIGHTCYAN_EX
        LG = Fore.LIGHTGREEN_EX; LY = Fore.LIGHTYELLOW_EX
        LR = Fore.LIGHTRED_EX; S = Style.RESET_ALL

        lines = [
            "",
            C + "  ╔" + "═" * 56 + "╗",
            C + "  ║" + LC + Style.BRIGHT +
            "          🛡️ NETSHIELD CONTROL PANEL 🛡️             " + C + "  ║",
            C + "  ╠" + "═" * 56 + "╣",
            C + "  ║ " + LY + "  PROTECTION" + " " * 42 + C + "   ║",
            C + "  ║  " + LC + "1" + W + " 🔗 Check URL (Safe or Scam?)       " + C + "          ║",
            C + "  ║  " + LC + "2" + W + " 🌐 Block IP Address                " + C + "          ║",
            C + "  ║  " + LC + "3" + W + " 🚫 Block Domain/Website            " + C + "          ║",
            C + "  ║  " + LC + "4" + W + " 📱 Scan Link (Paste any link)      " + C + "          ║",
            C + "  ║ " + LY + "  DETECTION" + " " * 43 + C + "   ║",
            C + "  ║  " + LC + "5" + W + " 🎣 Phishing Detector               " + C + "          ║",
            C + "  ║  " + LC + "6" + W + " 🦠 Malware URL Scanner             " + C + "          ║",
            C + "  ║ " + LY + "  MANAGEMENT" + " " * 42 + C + "   ║",
            C + "  ║  " + LC + "7" + W + " 📋 View Blocklist                  " + C + "          ║",
            C + "  ║  " + LC + "8" + W + " ✅ Unblock Domain/IP               " + C + "          ║",
            C + "  ║  " + LC + "9" + W + " 🔄 Update Threat Feed              " + C + "          ║",
            C + "  ╠" + "═" * 56 + "╣",
            C + "  ║  " + LC + "0" + LG + " ⚡ Full System Scan              " + C + "          ║",
            C + "  ║  " + LC + "l" + LY + " 📊 View Block Log              " + LC + " s" + LR +
            " 🛡️ Shield Status  " + C + "   ║",
            C + "  ║  " + LC + "q" + LR + " 🚪 Exit                        " + C + "          ║",
            C + "  ╚" + "═" * 56 + "╝",
            S,
        ]
        for line in lines:
            print(line)

    @classmethod
    def blocked(cls, target, reason):
        print()
        print("  " + Fore.RED + "╔" + "═" * 52 + "╗")
        print("  " + Fore.RED + "║" + Fore.LIGHTRED_EX + Style.BRIGHT +
              "  🚫 BLOCKED!" + " " * 38 + Fore.RED + "║")
        print("  " + Fore.RED + "╠" + "═" * 52 + "╣")
        print("  " + Fore.RED + "║" + Fore.WHITE + "  Target : " + str(target)[:40].ljust(40) + Fore.RED + "║")
        print("  " + Fore.RED + "║" + Fore.WHITE + "  Reason : " + str(reason)[:40].ljust(40) + Fore.RED + "║")
        print("  " + Fore.RED + "╚" + "═" * 52 + "╝" + Style.RESET_ALL)

    @classmethod
    def safe(cls, target):
        print()
        print("  " + Fore.GREEN + "╔" + "═" * 52 + "╗")
        print("  " + Fore.GREEN + "║" + Fore.LIGHTGREEN_EX + Style.BRIGHT +
              "  ✅ SAFE!" + " " * 41 + Fore.GREEN + "║")
        print("  " + Fore.GREEN + "╠" + "═" * 52 + "╣")
        print("  " + Fore.GREEN + "║" + Fore.WHITE + "  Target : " + str(target)[:40].ljust(40) + Fore.GREEN + "║")
        print("  " + Fore.GREEN + "║" + Fore.WHITE + "  Status : No threats detected".ljust(50) + Fore.GREEN + "║")
        print("  " + Fore.GREEN + "╚" + "═" * 52 + "╝" + Style.RESET_ALL)

    @classmethod
    def result(cls, key, val, color=Fore.WHITE):
        print("  " + Fore.CYAN + "│ " + Fore.LIGHTYELLOW_EX +
              key.ljust(18) + Fore.WHITE + ": " + color + str(val)[:52] + Style.RESET_ALL)

    @classmethod
    def section(cls, title):
        print("\n  " + Fore.CYAN + "┌─[ " + title + " ]" + "─" * 38 + Style.RESET_ALL)

    @classmethod
    def section_end(cls):
        print("  " + Fore.CYAN + "└" + "─" * 52 + Style.RESET_ALL)

    @classmethod
    def progress(cls, cur, total, desc=""):
        if total == 0: return
        p = cur / total
        w = 25
        bar = "█" * int(w*p) + "░" * (w - int(w*p))
        sys.stdout.write("\r  " + Fore.CYAN + "[" + Fore.LIGHTCYAN_EX +
                         bar + Fore.CYAN + "] " + Fore.WHITE + str(int(p*100)) +
                         "% " + Fore.LIGHTBLACK_EX + desc[:28] + Style.RESET_ALL)
        sys.stdout.flush()
        if cur >= total: print()
