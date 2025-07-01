import os
import pandas as pd

# Lấy đường dẫn thư mục chứa script này
current_dir = os.path.dirname(os.path.abspath(__file__))

# Đường dẫn đến các thư mục chứa file csv
folder1 = os.path.join(current_dir, '..', 'FirstCity')
folder2 = os.path.join(current_dir, '..', 'LastCity')
output_folder = os.path.join(current_dir, '..', '_Citys')

# Tạo thư mục kết quả nếu chưa tồn tại
os.makedirs(output_folder, exist_ok=True)

# Lấy danh sách file .csv từ folder1
file_names = [f for f in os.listdir(folder1) if f.endswith('.csv')]

for file_name in file_names:
    file1_path = os.path.join(folder1, file_name)
    file2_path = os.path.join(folder2, file_name)
    if os.path.exists(file2_path):
        # Đọc file City1 bình thường
        df1 = pd.read_csv(file1_path)
        # Đọc file City2 và bỏ dòng đầu tiên (tên cột)
        df2 = pd.read_csv(file2_path).iloc[1:]
        # Ghép dữ liệu
        merged_df = pd.concat([df1, df2], ignore_index=True)
        # Ghi vào file mới
        output_path = os.path.join(output_folder, file_name)
        merged_df.to_csv(output_path, index=False)
        print(f"✅ Ghép thành công: {file_name}")
    else:
        print(f"❌ Không tìm thấy {file_name} trong {folder2}")
