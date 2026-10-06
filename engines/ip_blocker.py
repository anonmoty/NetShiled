from core.blocker import Blocker
from core.scanner import Scanner
from core.banner import Banner
from colorama import Fore, Style

class IPBlockerEngine:
    @staticmethod
    def run():
        ip = input("\n  " + Fore.CYAN + "  Enter IP to block: " + Style.RESET_ALL).strip()
        if not ip:
            return
        Scanner.check_ip(ip)
        reason = input("  " + Fore.CYAN + "  Reason (blank=Suspicious): " + Style.RESET_ALL).strip() or "Suspicious IP"
        Blocker.block_ip(ip, reason)
        Banner.blocked(ip, reason)
