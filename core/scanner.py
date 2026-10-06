import re
import socket
from urllib.parse import urlparse
from core.config import Config
from core.blocker import Blocker
from core.logger import Log
from core.banner import Banner
from colorama import Fore, Style
import requests

log = Log()


class Scanner:
    """URL/IP/Domain threat scanner"""

    # Phishing keywords
    PHISH_KEYWORDS = [
        "login", "signin", "verify", "confirm", "secure", "update",
        "account", "banking", "paypal", "apple", "google", "microsoft",
        "amazon", "facebook", "instagram", "netflix", "suspended",
        "unauthorized", "credential", "password-reset",
    ]

    # Suspicious TLDs
    BAD_TLDS = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".top",
                ".buzz", ".click", ".icu", ".cam", ".loan", ".work"]

    # Known scam patterns
    SCAM_PATTERNS = [
        r"free[-_]?gift", r"you[-_]?won", r"claim[-_]?prize",
        r"lottery[-_]?winner", r"congratulations", r"urgent[-_]?action",
        r"account[-_]?suspended", r"verify[-_]?now", r"limited[-_]?time",
        r"click[-_]?here[-_]?now", r"download[-_]?now",
    ]

    @classmethod
    def check_url(cls, url):
        """Check if URL is safe or suspicious"""
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed = urlparse(url)
        domain = parsed.hostname or ""
        score = 0
        reasons = []

        Banner.section("URL Analysis: " + url[:45])

        # 1. Check blocklist
        if Blocker.is_domain_blocked(domain):
            Banner.result("Blocklist", "🚫 ALREADY BLOCKED!", Fore.RED)
            Banner.blocked(url, "In blocklist")
            return "BLOCKED"

        # 2. IP in URL
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            score += 25
            reasons.append("Raw IP in URL")
            Banner.result("⚠️ IP URL", "Raw IP address used", Fore.RED)

        # 3. Suspicious TLD
        for tld in cls.BAD_TLDS:
            if domain.endswith(tld):
                score += 20
                reasons.append("Suspicious TLD: " + tld)
                Banner.result("⚠️ TLD", "Suspicious: " + tld, Fore.YELLOW)
                break

        # 4. URL shortener
        shorteners = ["bit.ly", "tinyurl", "goo.gl", "t.co", "is.gd", "ow.ly"]
        for s in shorteners:
            if s in domain:
                score += 15
                reasons.append("URL shortener")
                Banner.result("⚠️ Shortener", s, Fore.YELLOW)
                break

        # 5. @ symbol
        if "@" in url:
            score += 25
            reasons.append("@ symbol (redirect trick)")
            Banner.result("⚠️ @ Symbol", "Redirect trick detected", Fore.RED)

        # 6. HTTPS check
        if not url.startswith("https"):
            score += 10
            reasons.append("No HTTPS")
            Banner.result("⚠️ HTTPS", "Not using HTTPS", Fore.YELLOW)

        # 7. Scam keywords
        url_lower = url.lower()
        for kw in cls.PHISH_KEYWORDS:
            if kw in url_lower:
                score += 5
        if score >= 10:
            reasons.append("Phishing keywords in URL")

        # 8. Scam patterns
        for pat in cls.SCAM_PATTERNS:
            if re.search(pat, url_lower):
                score += 15
                reasons.append("Scam pattern: " + pat[:20])
                break

        # 9. Long URL
        if len(url) > 200:
            score += 10
            reasons.append("Abnormally long URL")

        # 10. Many subdomains
        if domain.count(".") > 3:
            score += 10
            reasons.append("Too many subdomains")

        # 11. DNS check
        try:
            ip = socket.gethostbyname(domain)
            Banner.result("DNS", domain + " → " + ip, Fore.GREEN)
        except:
            score += 20
            reasons.append("DNS resolution failed")
            Banner.result("DNS", "FAILED (suspicious)", Fore.RED)

        # 12. HTTP check
        try:
            r = requests.get(url, timeout=8, verify=False, allow_redirects=True)
            Banner.result("HTTP", str(r.status_code), Fore.GREEN if r.status_code == 200 else Fore.YELLOW)
            if r.status_code == 200:
                body = r.text.lower()
                # Check for phishing content
                if "password" in body and "login" in body and "form" in body:
                    if any(kw in domain for kw in ["paypal", "apple", "google", "bank", "microsoft"]):
                        if not any(real in domain for real in ["paypal.com", "apple.com", "google.com", "microsoft.com"]):
                            score += 30
                            reasons.append("Fake login page detected!")
                            Banner.result("🎣 Phishing", "FAKE LOGIN PAGE!", Fore.RED)
        except:
            Banner.result("HTTP", "Connection failed", Fore.YELLOW)

        # Verdict
        Banner.result("Threat Score", str(score) + "/100",
                      Fore.RED if score >= 50 else Fore.YELLOW if score >= 25 else Fore.GREEN)

        if reasons:
            Banner.result("Reasons", "; ".join(reasons[:3]),
                          Fore.RED if score >= 50 else Fore.YELLOW)

        Banner.section_end()

        if score >= 50:
            Banner.blocked(url, "Threat score: " + str(score))
            ans = input("  " + Fore.RED + "  Block this URL? (y/n): " + Style.RESET_ALL).strip().lower()
            if ans == "y":
                Blocker.block_url(url, "Score: " + str(score) + " | " + "; ".join(reasons[:2]))
            return "DANGEROUS"
        elif score >= 25:
            log.warn("Suspicious URL (score: " + str(score) + ")")
            return "SUSPICIOUS"
        else:
            Banner.safe(url)
            return "SAFE"

    @classmethod
    def check_ip(cls, ip):
        """Check IP reputation"""
        ip = ip.strip()
        Banner.section("IP Analysis: " + ip)

        if Blocker.is_ip_blocked(ip):
            Banner.result("Status", "🚫 ALREADY BLOCKED", Fore.RED)
            Banner.section_end()
            return "BLOCKED"

        # GeoIP
        try:
            r = requests.get("http://ip-api.com/json/" + ip, timeout=8)
            if r.status_code == 200:
                d = r.json()
                if d.get("status") == "success":
                    Banner.result("Country", d.get("country", "") + " (" + d.get("countryCode", "") + ")")
                    Banner.result("City", d.get("city", ""))
                    Banner.result("ISP", d.get("isp", ""))
                    Banner.result("Org", d.get("org", ""))
                    if d.get("proxy"):
                        Banner.result("⚠️ Proxy", "YES - This is a proxy/VPN", Fore.RED)
                    if d.get("hosting"):
                        Banner.result("⚠️ Hosting", "Datacenter IP", Fore.YELLOW)
        except:
            Banner.result("GeoIP", "Lookup failed", Fore.YELLOW)

        # Reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)
            Banner.result("Hostname", hostname[0])
        except:
            Banner.result("Hostname", "No reverse DNS")

        Banner.section_end()
        return "CHECKED"
