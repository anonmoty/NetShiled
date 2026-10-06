import requests
from core.config import Config
from core.blocker import Blocker
from core.banner import Banner
from core.logger import Log
from colorama import Fore, Style

log = Log()

class ThreatFeed:
    @staticmethod
    def run():
        Banner.section("Updating Threat Feeds")
        total_blocked = 0

        for i, feed_url in enumerate(Config.THREAT_FEEDS):
            Banner.progress(i + 1, len(Config.THREAT_FEEDS), "Fetching feed...")
            try:
                r = requests.get(feed_url, timeout=30)
                if r.status_code == 200:
                    lines = r.text.strip().split("\n")
                    count = 0
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        # Extract domain from hosts format
                        parts = line.split()
                        if len(parts) >= 2 and parts[0] in ["0.0.0.0", "127.0.0.1"]:
                            domain = parts[1]
                        else:
                            domain = parts[0]

                        if domain and "." in domain and domain not in ["localhost", "localhost.localdomain"]:
                            if not Blocker.is_domain_blocked(domain):
                                Blocker.block_domain(domain, "Threat Feed")
                                count += 1
                                if count % 100 == 0:
                                    log.info("Blocked " + str(count) + " domains...")

                    total_blocked += count
                    log.ok("Feed " + str(i+1) + ": " + str(count) + " new domains blocked")
            except Exception as e:
                log.warn("Feed " + str(i+1) + " failed: " + str(e)[:40])

        Banner.section_end()
        print("  " + Fore.GREEN + "  [✓] Total new blocks: " + str(total_blocked) + Style.RESET_ALL)
