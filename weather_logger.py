from flask import Flask, render_template, request
import requests
import csv
import os
from datetime import datetime
import pytz
import time
import threading

app = Flask(__name__, template_folder="UI")

# Biến toàn cục để lưu thông tin từ giao diện
location_data = {}

API_KEY = "04ac04c6c5dfbc0ed71a2f734493c394"

# ========== Giao diện ==========
@app.route("/")
def index():
    return render_template("location_picker.html")

@app.route("/location", methods=["POST"])
def receive_location():
    global location_data
    data = request.get_json()
    location_data = {
        "lat": round(data.get("lat", 0), 6),
        "lon": round(data.get("lon", 0), 6),
        "province": data.get("province", "").strip(),
        "city": data.get("city", "").strip(),
        "filename": data.get("filename", "").strip()
    }
    print(f"\n📍 Đã nhận vị trí từ web: {location_data['lat']}, {location_data['lon']}")
    print(f"🏙️ Tỉnh: {location_data['province']} | Thành phố: {location_data['city']}")
    print(f"💾 Ghi vào file: {location_data['filename']}")
    return "OK", 200

# ========== Ghi thời tiết ==========
def safe(val, cast=float):
    try:
        return cast(val)
    except:
        return "N/A"

def ensure_csv(filename):
    if not os.path.exists(filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "time", "province", "city",
                "temperature", "temp_min", "temp_max",
                "humidity", "feels_like", "visibility",
                "precipitation", "cloudcover", "wind_speed", "wind_gust",
                "wind_direction", "pressure", "is_day",
                "weather_code", "weather_main", "weather_description", "weather_icon"
            ])

def fetch_and_log():
    while not location_data:
        print("⏳ Đang đợi người dùng gửi vị trí từ trình duyệt...")
        time.sleep(2)

    filename = location_data["filename"]
    ensure_csv(filename)

    while True:
        try:
            lat = location_data["lat"]
            lon = location_data["lon"]
            province = location_data["province"]
            city = location_data["city"]

            url = (
                f"https://api.openweathermap.org/data/2.5/weather?"
                f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            )

            res = requests.get(url)
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
            precipitation = safe(rain.get("1h", 0.0))

            with open(filename, "a", newline="", encoding="utf-8") as f:
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
                    precipitation,
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

            print(f"🕒 {now.strftime('%H:%M:%S')} | {province} - {city} | {main.get('temp')} °C | {weather.get('description')} | 💾 {filename}")
            time.sleep(5)

        except Exception as e:
            print("❌ Lỗi khi lấy/ghi dữ liệu:", e)
            time.sleep(5)

# ========== Chạy Flask + Logger song song ==========
if __name__ == "__main__":
    threading.Thread(target=fetch_and_log, daemon=True).start()
    print("🌐 Truy cập giao diện tại: http://127.0.0.1:5000")
    app.run(debug=False)