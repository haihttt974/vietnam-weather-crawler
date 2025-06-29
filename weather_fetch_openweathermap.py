import requests
import csv
import os
import time
from datetime import datetime
import pytz
import sys

# =============================
# CẤU HÌNH
# =============================
API_KEY = "04ac04c6c5dfbc0ed71a2f734493c394"  # <-- Thay bằng API key của bạn
FOLDER = "City"
os.makedirs(FOLDER, exist_ok=True)

# =============================
# Đọc danh sách tỉnh/thành từ CSV
# =============================
locations = []
with open("DanhSach_63_TinhVN.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        province = row["Province"]
        city = row["City"]
        lat = float(row["Latitude"])
        lon = float(row["Longitude"])
        locations.append((province, city, lat, lon))

# =============================
# Hàm an toàn ép kiểu
# =============================
def safe(val, cast=float):
    try:
        return cast(val)
    except:
        return "N/A"

# =============================
# Tạo file CSV nếu chưa có
# =============================
def ensure_csv(province):
    file_path = os.path.join(FOLDER, province.replace(" ", "") + ".csv")
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "time", "province", "city",
                "temperature", "temp_min", "temp_max",
                "humidity", "feels_like", "visibility",
                "precipitation", "cloudcover", "wind_speed", "wind_gust",
                "wind_direction", "pressure", "is_day",
                "weather_code", "weather_main", "weather_description", "weather_icon"
            ])
    return file_path

# =============================
# Gọi API và ghi dữ liệu
# =============================
def fetch_and_write(province, city, lat, lon):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        )

        res = requests.get(url, timeout=5)
        data = res.json()

        main = data.get("main", {})
        wind = data.get("wind", {})
        rain = data.get("rain", {})
        clouds = data.get("clouds", {})
        weather = data.get("weather", [{}])[0]
        sys_data = data.get("sys", {})

        now = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
        sunrise = datetime.fromtimestamp(sys_data.get("sunrise", 0), pytz.utc).astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
        sunset = datetime.fromtimestamp(sys_data.get("sunset", 0), pytz.utc).astimezone(pytz.timezone("Asia/Ho_Chi_Minh"))
        is_day = 1 if sunrise < now < sunset else 0

        filename = ensure_csv(province)
        with open(filename, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                now.strftime("%Y-%m-%d %H:%M:%S"),
                province, city,
                safe(main.get("temp")),
                safe(main.get("temp_min")),
                safe(main.get("temp_max")),
                safe(main.get("humidity")),
                safe(main.get("feels_like")),
                safe(data.get("visibility")),
                safe(rain.get("1h", 0.0)),
                safe(clouds.get("all")),
                safe(wind.get("speed")),
                safe(wind.get("gust", 0.0)),
                safe(wind.get("deg")),
                safe(main.get("pressure")),
                is_day,
                safe(weather.get("id"), int),
                weather.get("main", ""),
                weather.get("description", ""),
                weather.get("icon", "")
            ])
    except Exception as e:
        print(f"\n❌ {city} - Lỗi: {e}")

# =============================
# Hiển thị thanh tiến trình
# =============================
def render_loop_progress_bar(current, total, start_time, bar_length=30):
    percent = int((current / total) * 100)
    filled_len = int(bar_length * current // total)
    bar = "=" * filled_len + ">" + "-" * (bar_length - filled_len - 1)
    sys.stdout.write(f"\r[{bar}] {percent:>3}% - Bắt đầu lúc: {start_time}")
    sys.stdout.flush()

# =============================
# VÒNG LẶP LIÊN TỤC
# =============================
while True:
    total = len(locations)
    start_dt = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
    start_time_str = start_dt.strftime("%H:%M:%S")

    for idx, (province, city, lat, lon) in enumerate(locations, start=1):
        fetch_and_write(province, city, lat, lon)
        render_loop_progress_bar(idx, total, start_time_str)

    print("\n✅ Hoàn thành lượt lúc:", datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M:%S"))
    print()
    print("``````````````````````````````````````````````````````````````")
    time.sleep(1)
