def parse_logs_slow(filename="app.log"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    unique_ips = []
    ip_counts = {}

    # Неэффективно: для каждой строки проверяем весь список unique_ips (O(n^2))
    for line in lines:
        parts = line.split()
        ip = parts[2]

        found = False
        for existing_ip in unique_ips:
            if existing_ip == ip:
                found = True
                break
        if not found:
            unique_ips.append(ip)

        # Также неэффективный подсчёт вхождений
        count = 0
        for l in lines:
            if ip in l:
                count += 1
        ip_counts[ip] = count

    return unique_ips, ip_counts


if __name__ == "__main__":
    import time
    start = time.time()
    ips, counts = parse_logs_slow()
    print(f"Уникальных IP: {len(ips)}")
    print(f"Время выполнения: {time.time() - start:.2f} сек")