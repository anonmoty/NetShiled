import os
import socket
from datetime import datetime
from core.config import Config
from core.logger import Log
from colorama import Fore, Style

log = Log()


class Blocker:
    """Core blocking engine - blocks URLs, IPs, Domains"""

    @classmethod
    def block_domain(cls, domain, reason="Suspicious"):
        """Block domain in blocklist + /etc/hosts"""
        domain = domain.strip().lower()
        if not domain:
            return False

        Config.init()

        # 1. Add to domain blocklist
        already = cls.is_domain_blocked(domain)
        if already:
            log.warn("Already blocked: " + domain)
            return True

        with open(Config.DOMAIN_BLOCKLIST, "a") as f:
            f.write(domain + " | " + reason + " | " + datetime.now().strftime("%Y-%m-%d") + "\n")
        log.blocked("Domain added to blocklist: " + domain)

        # 2. Block in /etc/hosts
        cls._add_hosts(domain)

        # 3. Log
        Config.log_block("DOMAIN", domain, reason)
        return True

    @classmethod
    def block_ip(cls, ip, reason="Malicious"):
        """Block IP address"""
        ip = ip.strip()
        if not ip:
            return False

        Config.init()

        # Check if already blocked
        try:
            with open(Config.IP_BLOCKLIST, "r") as f:
                if ip in f.read():
                    log.warn("IP already blocked: " + ip)
                    return True
        except: pass

        with open(Config.IP_BLOCKLIST, "a") as f:
            f.write(ip + " | " + reason + " | " + datetime.now().strftime("%Y-%m-%d") + "\n")
        log.blocked("IP blocked: " + ip)

        # Add to hosts
        cls._add_hosts_ip(ip)

        Config.log_block("IP", ip, reason)
        return True

    @classmethod
    def block_url(cls, url, reason="Suspicious URL"):
        """Block specific URL"""
        url = url.strip()
        if not url:
            return False

        Config.init()

        with open(Config.URL_BLOCKLIST, "a") as f:
            f.write(url + " | " + reason + " | " + datetime.now().strftime("%Y-%m-%d") + "\n")
        log.blocked("URL blocked: " + url[:60])

        # Also block the domain
        from urllib.parse import urlparse
        try:
            domain = urlparse(url if "://" in url else "http://" + url).hostname
            if domain:
                cls.block_domain(domain, reason)
        except: pass

        Config.log_block("URL", url, reason)
        return True

    @classmethod
    def _add_hosts(cls, domain):
        """Add domain to /etc/hosts to block it"""
        entry = "127.0.0.1 " + domain + "\n"
        www_entry = "127.0.0.1 www." + domain + "\n"
        try:
            with open(Config.HOSTS_FILE, "r") as f:
                content = f.read()
            if domain not in content:
                with open(Config.HOSTS_FILE, "a") as f:
                    f.write("\n# NetShield Block\n")
                    f.write(entry)
                    f.write(www_entry)
                log.ok("Blocked in /etc/hosts: " + domain)
            else:
                log.info("Already in /etc/hosts: " + domain)
        except PermissionError:
            # No root - save to local hosts file
            local_hosts = os.path.join(Config.ROOT, "hosts_block.txt")
            with open(local_hosts, "a") as f:
                f.write(entry)
                f.write(www_entry)
            log.warn("No root access. Saved to " + local_hosts)
            log.info("Run with sudo or copy manually to /etc/hosts")
        except Exception as e:
            log.warn("Hosts file error: " + str(e)[:40])

    @classmethod
    def _add_hosts_ip(cls, ip):
        """Block IP via iptables rule (save for manual use)"""
        rule = "iptables -A OUTPUT -d " + ip + " -j DROP\n"
        rules_file = os.path.join(Config.ROOT, "firewall_rules.txt")
        with open(rules_file, "a") as f:
            f.write("# Block " + ip + "\n")
            f.write(rule + "\n")
        log.info("Firewall rule saved to firewall_rules.txt")

    @classmethod
    def is_domain_blocked(cls, domain):
        """Check if domain is in blocklist"""
        domain = domain.strip().lower()
        try:
            with open(Config.DOMAIN_BLOCKLIST, "r") as f:
                content = f.read().lower()
            if domain in content:
                return True
        except: pass

        # Also check hosts file
        try:
            with open(Config.HOSTS_FILE, "r") as f:
                content = f.read().lower()
            if domain in content:
                return True
        except: pass

        return False

    @classmethod
    def is_ip_blocked(cls, ip):
        """Check if IP is blocked"""
        try:
            with open(Config.IP_BLOCKLIST, "r") as f:
                if ip.strip() in f.read():
                    return True
        except: pass
        return False

    @classmethod
    def is_url_blocked(cls, url):
        """Check if URL is blocked"""
        try:
            with open(Config.URL_BLOCKLIST, "r") as f:
                if url.strip() in f.read():
                    return True
        except: pass
        return False

    @classmethod
    def unblock_domain(cls, domain):
        """Remove domain from blocklist"""
        domain = domain.strip().lower()
        Config.init()

        # Remove from blocklist file
        try:
            with open(Config.DOMAIN_BLOCKLIST, "r") as f:
                lines = f.readlines()
            new_lines = [l for l in lines if domain not in l.lower()]
            with open(Config.DOMAIN_BLOCKLIST, "w") as f:
                f.writelines(new_lines)
        except: pass

        # Remove from hosts
        try:
            with open(Config.HOSTS_FILE, "r") as f:
                lines = f.readlines()
            new_lines = [l for l in lines if domain not in l.lower()]
            with open(Config.HOSTS_FILE, "w") as f:
                f.writelines(new_lines)
            log.ok("Unblocked: " + domain)
        except PermissionError:
            log.warn("No root access to edit /etc/hosts")
        except Exception as e:
            log.warn("Error: " + str(e)[:40])

    @classmethod
    def show_blocklist(cls):
        """Display all blocked items"""
        Config.init()

        Banner_section = lambda t: print("\n  " + Fore.CYAN + "┌─[ " + t + " ]" + "─" * 38 + Style.RESET_ALL)
        Banner_end = lambda: print("  " + Fore.CYAN + "└" + "─" * 52 + Style.RESET_ALL)

        # Domains
        Banner_section("Blocked Domains")
        try:
            with open(Config.DOMAIN_BLOCKLIST, "r") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            if lines:
                for i, l in enumerate(lines[:20], 1):
                    print("  " + Fore.CYAN + "│ " + Fore.RED + str(i).ljust(4) + Fore.WHITE + l[:48])
                if len(lines) > 20:
                    print("  " + Fore.CYAN + "│ " + Fore.YELLOW + "... and " + str(len(lines)-20) + " more")
            else:
                print("  " + Fore.CYAN + "│ " + Fore.WHITE + "No domains blocked")
        except: pass
        Banner_end()

        # IPs
        Banner_section("Blocked IPs")
        try:
            with open(Config.IP_BLOCKLIST, "r") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            if lines:
                for i, l in enumerate(lines[:10], 1):
                    print("  " + Fore.CYAN + "│ " + Fore.RED + str(i).ljust(4) + Fore.WHITE + l[:48])
            else:
                print("  " + Fore.CYAN + "│ " + Fore.WHITE + "No IPs blocked")
        except: pass
        Banner_end()

        # URLs
        Banner_section("Blocked URLs")
        try:
            with open(Config.URL_BLOCKLIST, "r") as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            if lines:
                for i, l in enumerate(lines[:10], 1):
                    print("  " + Fore.CYAN + "│ " + Fore.RED + str(i).ljust(4) + Fore.WHITE + l[:48])
            else:
                print("  " + Fore.CYAN + "│ " + Fore.WHITE + "No URLs blocked")
        except: pass
        Banner_end()

    @classmethod
    def show_log(cls):
        """Show block log"""
        Config.init()
        print("\n  " + Fore.CYAN + "┌─[ 📊 Block Log ]" + "─" * 33 + Style.RESET_ALL)
        try:
            with open(Config.BLOCK_LOG, "r") as f:
                lines = f.readlines()
            if lines:
                for line in lines[-20:]:
                    print("  " + Fore.CYAN + "│ " + Fore.WHITE + line.strip()[:52])
                print("  " + Fore.CYAN + "│ " + Fore.YELLOW + "Total blocks: " + str(len(lines)))
            else:
                print("  " + Fore.CYAN + "│ " + Fore.WHITE + "No blocks yet")
        except: pass
        print("  " + Fore.CYAN + "└" + "─" * 52 + Style.RESET_ALL)
