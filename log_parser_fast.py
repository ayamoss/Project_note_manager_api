from collections import Counter, defaultdict
import time


def parse_logs_fast(filename="app.log"):
    ip_counts = Counter()
    level_counts = Counter()
    ip_levels = defaultdict(list)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            timestamp, level, ip = parts[0], parts[1], parts[2]
            ip_counts[ip] += 1
            level_counts[level] += 1
            ip_levels[ip].append(level)

    return ip_counts, level_counts, ip_levels


if __name__ == "__main__":
    start = time.time()
    ip_counts, level_counts, ip_levels = parse_logs_fast()

    print(f"Уникальных IP: {len(ip_counts)}")
    print(f"Топ-5 активных IP: {ip_counts.most_common(5)}")
    print(f"Статистика по уровням: {dict(level_counts)}")
    print(f"Время выполнения: {time.time() - start:.4f} сек")