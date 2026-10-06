import os
from datetime import datetime

class Config:
    APP = "NetShield"
    VERSION = "1.0.0"
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BLOCKLIST_DIR = os.path.join(ROOT, "blocklist")
    LOGS_DIR = os.path.join(ROOT, "logs")
    URL_BLOCKLIST = os.path.join(BLOCKLIST_DIR, "urls.txt")
    IP_BLOCKLIST = os.path.join(BLOCKLIST_DIR, "ips.txt")
    DOMAIN_BLOCKLIST = os.path.join(BLOCKLIST_DIR, "domains.txt")
    BLOCK_LOG = os.path.join(LOGS_DIR, "blocked.log")
    HOSTS_FILE = "/etc/hosts"
    TIMEOUT = 10

    # Known threat feed URLs (free)
    THREAT_FEEDS = [
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
        "https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt",
    ]

    @classmethod
    def init(cls):
        for d in [cls.BLOCKLIST_DIR, cls.LOGS_DIR]:
            os.makedirs(d, exist_ok=True)
        for f in [cls.URL_BLOCKLIST, cls.IP_BLOCKLIST, cls.DOMAIN_BLOCKLIST, cls.BLOCK_LOG]:
            if not os.path.exists(f):
                with open(f, "w") as fh:
                    fh.write("# NetShield Blocklist\n")

    @classmethod
    def log_block(cls, target_type, target, reason):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = "[" + ts + "] BLOCKED [" + target_type + "] " + target + " | Reason: " + reason + "\n"
        try:
            with open(cls.BLOCK_LOG, "a") as f:
                f.write(entry)
        except:
            pass
