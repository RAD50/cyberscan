def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

def ip_range(start_ip, end_ip):
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    ip_list = []

    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            for k in range(start[2], end[2] + 1):
                for l in range(start[3], end[3] + 1):
                    ip = f"{i}.{j}.{k}.{l}"
                    if is_valid_ip(ip):
                        ip_list.append(ip)
    return ip_list