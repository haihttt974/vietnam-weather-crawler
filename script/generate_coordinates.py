import pandas as pd
from geopy.geocoders import Nominatim
import time

# Đọc file đã có sẵn
df = pd.read_csv("vietnam_all_provinces_and_cities.csv")
geolocator = Nominatim(user_agent="vn_locator")

# Duyệt qua từng dòng
for i, row in df.iterrows():
    if pd.isna(row["Latitude"]) or pd.isna(row["Longitude"]):
        try:
            location = geolocator.geocode(f"{row['City']}, {row['Province']}, Vietnam")
            if location:
                df.at[i, "Latitude"] = location.latitude
                df.at[i, "Longitude"] = location.longitude
                print(f"Found: {row['City']}, {row['Province']} -> {location.latitude}, {location.longitude}")
            else:
                print(f"Not found: {row['City']}, {row['Province']}")
            time.sleep(1)  # Tránh bị chặn IP
        except:
            print(f"Error at: {row['City']}, {row['Province']}")

# Lưu lại file
df.to_csv("vietnam_all_provinces_and_cities.csv", index=False)