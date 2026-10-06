from core.scanner import Scanner
from core.banner import Banner

class URLChecker:
    @staticmethod
    def run():
        Banner.section("URL Safety Checker")
        url = input("  " + "\033[96m" + "  Paste URL to check: " + "\033[0m").strip()
        if url:
            Scanner.check_url(url)
        else:
            print("  \033[33m  [!] No URL provided\033[0m")
        Banner.section_end()
