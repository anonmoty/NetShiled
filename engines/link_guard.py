from core.scanner import Scanner
from core.blocker import Blocker
from core.banner import Banner
from colorama import Fore, Style

class LinkGuard:
    @staticmethod
    def run():
        print("\n  " + Fore.CYAN + "  Paste links one by one (empty line to stop):" + Style.RESET_ALL)
        count = 0
        blocked = 0
        while True:
            link = input("  " + Fore.LIGHTCYAN_EX + "  🔗 > " + Style.RESET_ALL).strip()
            if not link:
                break
            count += 1
            result = Scanner.check_url(link)
            if result in ["DANGEROUS", "BLOCKED"]:
                blocked += 1
        print("\n  " + Fore.GREEN + "  Scanned: " + str(count) + " | Blocked: " + str(blocked) + Style.RESET_ALL)
