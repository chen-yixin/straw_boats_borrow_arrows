import os
import re
import csv
from pathlib import Path
from IP2Location import IP2Location


# 配置数据库路径
DB_PATH = "IP2LOCATION-LITE-DB11.BIN"
ip2location_obj = IP2Location(DB_PATH)

BASE_DIR = Path(__file__).resolve().parent


def parse_log_file(log_file_path):
    data = []
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 根据实际日志格式调整正则表达式
            match = re.match(r'^([\d/]+\s[\d:.]+)\s([\d.]+):(\d+)\s?(.*?)\s?(\S*)\s?(\S*)$', line)
            if match:
                timestamp = match.group(1)
                ip = match.group(2)
                port = match.group(3)
                client = match.group(4)
                username = match.group(5)
                password = match.group(6)

                # 获取地理位置信息
                try:
                    record = ip2location_obj.get_all(ip)
                    country_code = record.country_short
                    country_name = record.country_long
                    region = record.region
                    city = record.city
                except Exception as e:
                    # 处理查询失败的情况
                    country_code = 'N/A'
                    country_name = 'N/A'
                    region = 'N/A'
                    city = 'N/A'

                entry = {
                    'timestamp': timestamp,
                    'ip': ip,
                    'port': port,
                    'client': client,
                    'username': username,
                    'password': password,
                    'country_code': country_code,
                    'country_name': country_name,
                    'region': region,
                    'city': city
                }
                data.append(entry)
    return data


def process_log_directory(log_directory: Path):
    all_data = []
    for filename in os.listdir(log_directory):
        if filename.endswith('.log'):
            log_file_path = os.path.join(log_directory, filename)
            log_data = parse_log_file(log_file_path)
            all_data.extend(log_data)
    return all_data


def write_to_csv(data, csv_file_path):
    fieldnames = [
        'timestamp', 'ip', 'port', 'country_code', 'country_name', 'region', 'city',
        'client', 'username', 'password',
    ]
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)


def main():
    log_directory = BASE_DIR / "logs"
    csv_output = BASE_DIR / "outputs" / "fakessh.csv"

    all_data = process_log_directory(log_directory)
    write_to_csv(all_data, csv_output)

    print(f"处理完成，结果已保存至 {csv_output}")


if __name__ == "__main__":
    main()
