import os
import math
import pandas as pd

# --- Cấu hình ---
folder_path = 'D:/PYTHON/vietnam-weather-crawler/05-Citys'
output_base = 'D:/PYTHON/vietnam-weather-crawler/Data/weather-vn-5'
max_size_mb = 70  # Giới hạn mỗi file

# --- Tính dung lượng file ---
files = [f for f in sorted(os.listdir(folder_path)) if f.endswith('.csv')]
file_sizes = [os.path.getsize(os.path.join(folder_path, f)) for f in files]  # bytes
total_size = sum(file_sizes)
max_size_bytes = max_size_mb * 1024 * 1024

# --- Tính số nhóm cần chia ---
num_parts = math.ceil(total_size / max_size_bytes)
print(f"📦 Tổng dung lượng: {total_size/1024/1024:.2f} MB -> chia thành {num_parts} file nhỏ hơn {max_size_mb}MB")

# --- Phân nhóm file dựa trên dung lượng ---
groups = [[] for _ in range(num_parts)]
group_sizes = [0] * num_parts

for file, size in zip(files, file_sizes):
    # Tìm nhóm có dung lượng hiện tại nhỏ nhất để thêm vào
    idx = group_sizes.index(min(group_sizes))
    groups[idx].append(file)
    group_sizes[idx] += size

# --- Ghép từng nhóm ---
header_saved = None
for i, group in enumerate(groups, start=1):
    dataframes = []
    for file in group:
        file_path = os.path.join(folder_path, file)
        if header_saved is None:
            df = pd.read_csv(file_path, engine='python')
            header_saved = df.columns.tolist()
        else:
            df = pd.read_csv(file_path, skiprows=1, names=header_saved, engine='python')
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    output_file = f"{output_base}_{i}.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"✅ Đã tạo {output_file} ({len(group)} file)")

print("🎉 Hoàn tất chia nhỏ và ghép file!")
