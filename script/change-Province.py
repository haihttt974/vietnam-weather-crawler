import pandas as pd
from unidecode import unidecode

# Đọc file CSV
df = pd.read_csv('DanhSach_63_TinhVN.csv')

# Bỏ dấu tiếng Việt trong cột 'Province'
df['Province'] = df['Province'].apply(lambda x: unidecode(str(x)))

# Ghi kết quả ra file mới
df.to_csv('output.csv', index=False)

print("✅ Đã chuyển đổi toàn bộ cột 'Province' sang không dấu và lưu vào 'output.csv'")