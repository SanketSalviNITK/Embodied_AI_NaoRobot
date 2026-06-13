# -*- coding: utf-8 -*-
"""
System Connection Diagnostic Tool (check_connections.py)
--------------------------------------------------------
Tests every network port and server node in the Embodied AI pipeline
to verify system health.

Usage:
  python3 check_connections.py
"""

import os
import sys
import socket

# Try importing urllib for HTTP checking
try:
    import urllib.request as urllib_request
except ImportError:
    import urllib2 as urllib_request

# Colors for terminal output (Windows ANSI support)
os.system("") # Init Windows ANSI support
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Services to test: (Name, Host, Port, Type)
SERVICES = [
    ("React Frontend (Vite)", "127.0.0.1", 5173, "HTTP"),
    ("Python 3 Brain Backend", "127.0.0.1", 5002, "HTTP"),
    ("Python 2.7 NAOqi Bridge", "127.0.0.1", 5001, "HTTP"),
    ("Blender Addon Server", "127.0.0.1", 9876, "TCP"),
    ("NAO Robot (Physical/Sim)", "10.23.18.144", 9559, "TCP"),
]

def test_tcp_connection(host, port, timeout=1.0):
    """Checks if a TCP socket port is open."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception:
        return False

def test_http_connection(host, port, timeout=1.0):
    """Checks if an HTTP service responds."""
    url = f"http://{host}:{port}"
    try:
        req = urllib_request.Request(
            url, 
            headers={'User-Agent': 'ConnectionCheck/1.0'}
        )
        response = urllib_request.urlopen(req, timeout=timeout)
        response.read()
        return True
    except Exception as e:
        # If port is open but returns an HTTP error (like 404 or 500), the service IS online
        if "HTTP Error" in str(e) or "Code 404" in str(e) or "Code 500" in str(e) or "Unauthorized" in str(e):
            return True
        # Try raw TCP check as backup
        return test_tcp_connection(host, port, timeout)

def main():
    print(f"\n{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}{CYAN}      NAO DIGITAL TWIN PIPELINE CONNECTION CHECK    {RESET}")
    print(f"{BOLD}{CYAN}===================================================={RESET}\n")
    
    print(f"{BOLD}{'Service Name':<30} {'Host:Port':<22} {'Status':<12}{RESET}")
    print("-" * 68)
    
    all_ok = True
    active_count = 0
    
    for name, host, port, conn_type in SERVICES:
        sys.stdout.write(f"{name:<30} {f'{host}:{port}':<22} ")
        sys.stdout.flush()
        
        is_online = False
        if conn_type == "HTTP":
            is_online = test_http_connection(host, port)
        else:
            is_online = test_tcp_connection(host, port)
            
        if is_online:
            status_text = f"{GREEN}[ ONLINE ]{RESET}"
            active_count += 1
        else:
            status_text = f"{RED}[OFFLINE]{RESET}"
            all_ok = False
            
        print(status_text)
        
    print("-" * 68)
    
    if all_ok:
        print(f"\n{GREEN}{BOLD}>>> ALL CONNECTIONS ARE SUCCESSFUL AND HEALTHY! <<< {RESET}")
        print("Your digital twin, brain, and robot sync pipeline is 100% operational.\n")
    else:
        print(f"\n{YELLOW}{BOLD}>>> SYSTEM STATUS: {active_count}/{len(SERVICES)} SERVICES ACTIVE <<< {RESET}")
        print(f"To run the digital twin, ensure {BOLD}Blender Server{RESET} is active, and then start")
        print("the React dashboard and sync bridges as needed.\n")

if __name__ == "__main__":
    main()
