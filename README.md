# vietnam-weather-crawler

Công cụ Python thu thập dữ liệu thời tiết cho 63 tỉnh/thành của Việt Nam sử dụng OpenWeatherMap API. Mỗi tỉnh được lưu thành một file CSV riêng trong thư mục `City/`.

## Cài đặt

```bash
pip install -r requirements.txt
```

Sau khi cài thư viện, mở file `weather_fetch_openweathermap.py` và thay `API_KEY` bằng khóa của bạn.

## Chạy chương trình

```bash
python weather_fetch_openweathermap.py
```

Có thể chạy bằng Docker nếu muốn:

```bash
docker build -t vn-weather .
docker run vn-weather
```

## Giải thích chi tiết các cột dữ liệu thời tiết

Dưới đây là giải thích cụ thể và chi tiết cho từng cột trong file CSV thu thập dữ liệu thời tiết từ OpenWeatherMap:

| Tên cột                 | Ý nghĩa chi tiết                                                                          |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| **time**                | Thời gian ghi nhận dữ liệu (theo giờ Việt Nam), định dạng `YYYY-MM-DD HH:mm:ss`.          |
| **province**            | Tên tỉnh/thành phố cấp tỉnh (ví dụ: TP Hồ Chí Minh, Hà Nội,...).                          |
| **city**                | Tên thành phố cụ thể (ví dụ: Ho Chi Minh, Hue, Da Nang,...).                              |
| **temperature**         | Nhiệt độ hiện tại tại điểm đo (°C).                                                       |
| **temp_min**            | Nhiệt độ thấp nhất trong khu vực tại thời điểm đó (°C).                                   |
| **temp_max**            | Nhiệt độ cao nhất trong khu vực tại thời điểm đó (°C).                                    |
| **humidity**            | Độ ẩm không khí hiện tại (%).                                                             |
| **feels_like**          | Nhiệt độ cảm nhận được (°C), có thể khác nhiệt độ thực tế do gió, độ ẩm,...               |
| **visibility**          | Tầm nhìn xa (mét), thường tối đa là 10.000 mét.                                           |
| **precipitation**       | Lượng mưa trong 1 giờ gần nhất (mm), nếu không có sẽ là 0.                                |
| **cloudcover**          | Mức độ mây che phủ bầu trời (%), 100 là mây hoàn toàn.                                    |
| **wind_speed**          | Tốc độ gió hiện tại (mét/giây).                                                           |
| **wind_gust**           | Cơn gió giật mạnh nhất được ghi nhận (mét/giây), có thể vắng mặt.                         |
| **wind_direction**      | Hướng gió (°), tính theo la bàn: 0 là Bắc, 90 là Đông, 180 là Nam, 270 là Tây.            |
| **pressure**            | Áp suất khí quyển tại mặt đất (hPa – hectopascal).                                        |
| **is_day**              | Trạng thái ngày/đêm: `1` nếu đang là ban ngày, `0` nếu là ban đêm.                        |
| **weather_code**        | Mã thời tiết (ví dụ: `804` cho “overcast clouds”). Có thể tra bảng mã của OpenWeatherMap. |
| **weather_main**        | Trạng thái tổng quát của thời tiết (ví dụ: "Clouds", "Rain", "Clear",...).                |
| **weather_description** | Mô tả chi tiết hơn về thời tiết (ví dụ: "overcast clouds", "light rain",...).             |
| **weather_icon**        | Mã icon biểu diễn thời tiết, có thể dùng để tải ảnh thời tiết tương ứng từ OpenWeather.   |

---

## Ghi chú thêm

- Dữ liệu được lấy từ API `https://api.openweathermap.org/data/2.5/weather`.
- Các giá trị được cập nhật mỗi vòng quét (mặc định mỗi giây, có thể thay đổi).
- Mỗi tỉnh/thành có file riêng lưu trữ dữ liệu trong thư mục `City/`.
