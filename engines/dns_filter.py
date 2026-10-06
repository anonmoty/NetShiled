from core.blocker import Blocker
from core.banner import Banner
from colorama import Fore, Style

class DNSFilter:
    @staticmethod
    def run():
        domain = input("\n  " + Fore.CYAN + "  Enter domain to block: " + Style.RESET_ALL).strip()
        if not domain:
            return
        domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
        reason = input("  " + Fore.CYAN + "  Reason (blank=Scam): " + Style.RESET_ALL).strip() or "Scam/Phishing"
        Blocker.block_domain(domain, reason)
        Banner.blocked(domain, reason)
