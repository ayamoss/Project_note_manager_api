import random
from datetime import datetime, timedelta

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
IPS = [f"192.168.1.{i}" for i in range(1, 20)]


def generate_logs(filename="app.log", n=5000):
    start = datetime.now()
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(n):
            ts = start + timedelta(seconds=i)
            level = random.choice(LEVELS)
            ip = random.choice(IPS)
            f.write(f"{ts.isoformat()} {level} {ip} request_id={i}\n")


if __name__ == "__main__":
    generate_logs(n=50000)
    print("Логи сгенерированы в app.log")