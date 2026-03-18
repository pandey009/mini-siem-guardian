import time
import random
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'test.log')

def write_log(line):
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')
    print(f"[*] Generated: {line}")

def simulate_brute_force(ip="192.168.1.100"):
    print(f"[!] Simulating Brute Force from {ip}...")
    for _ in range(5):
        timestamp = time.strftime("%b %d %H:%M:%S")
        log = f"{timestamp} server sshd[1234]: Failed password for root from {ip} port 54321 ssh2"
        write_log(log)
        time.sleep(1)

def simulate_web_errors():
    print("[!] Simulating Web Errors...")
    ips = ["10.0.0.5", "10.0.0.6", "10.0.0.7"]
    paths = ["/admin", "/config", "/login", "/api/v1/users"]
    for _ in range(5):
        ip = random.choice(ips)
        path = random.choice(paths)
        status = random.choice([404, 500, 403])
        timestamp = time.strftime("%d/%b/%Y:%H:%M:%S +0000")
        log = f'{ip} - - [{timestamp}] "GET {path} HTTP/1.1" {status} 512'
        write_log(log)
        time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.makedirs(os.path.dirname(LOG_FILE))
    
    while True:
        try:
            choice = random.choice(['brute', 'web', 'normal'])
            if choice == 'brute':
                simulate_brute_force(f"192.168.1.{random.randint(10, 254)}")
            elif choice == 'web':
                simulate_web_errors()
            else:
                timestamp = time.strftime("%b %d %H:%M:%S")
                write_log(f"{timestamp} server systemd[1]: Started Periodic Background Migration.")
            
            time.sleep(5)
        except KeyboardInterrupt:
            break
