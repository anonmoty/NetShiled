from core.scanner import Scanner
from core.blocker import Blocker
from core.banner import Banner
from colorama import Fore, Style

class PhishingDetector:
    @staticmethod
    def run():
        url = input("\n  " + Fore.CYAN + "  Paste suspicious link: " + Style.RESET_ALL).strip()
        if not url:
            return
        result = Scanner.check_url(url)
        if result in ["DANGEROUS", "BLOCKED"]:
            print("  " + Fore.RED + "  ⚠️ This is likely a PHISHING/SCAM website!" + Style.RESET_ALL)
            print("  " + Fore.RED + "  Do NOT open this link on any device!" + Style.RESET_ALL)
