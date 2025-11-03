import os
import pandas as pd

# Thư mục chứa script
current_dir = os.path.dirname(os.path.abspath(__file__))

# KHAI BÁO CÁC FOLDER THEO THỨ TỰ MUỐN GHÉP
folders = [
    os.path.join(current_dir, '..', '1'),
    os.path.join(current_dir, '..', '2'),
    os.path.join(current_dir, '..', '3'),
    os.path.join(current_dir, '..', '4'),
    os.path.join(current_dir, '..', '5'),
    os.path.join(current_dir, '..', '6'),
    os.path.join(current_dir, '..', '7'),
    os.path.join(current_dir, '..', '8'),
    os.path.join(current_dir, '..', '9'),
    os.path.join(current_dir, '..', '10'),
]

output_folder = os.path.join(current_dir, '..', '05-Citys')
os.makedirs(output_folder, exist_ok=True)

# Lấy TẬP HỢP tên file .csv xuất hiện ở ÍT NHẤT một trong các folder
all_csv_names = set()
for folder in folders:
    if os.path.isdir(folder):
        all_csv_names.update([f for f in os.listdir(folder) if f.endswith('.csv')])

for file_name in all_csv_names:
    dfs = []
    cols_ref = None  # dùng để chuẩn hoá cột (nếu cần)
    for idx, folder in enumerate(folders):
        file_path = os.path.join(folder, file_name)
        if not os.path.exists(file_path):
            continue

        # Trường hợp chuẩn: tất cả CSV đều có header ở dòng đầu → đọc bình thường
        df = pd.read_csv(file_path)

        # (Tuỳ chọn) Nếu bạn lo CSV sau có thể khác thứ tự cột,
        # thì khi đã có df đầu tiên, ép các df sau về cùng bộ cột:
        if cols_ref is None:
            cols_ref = list(df.columns)
        else:
            # Chỉ giữ những cột trùng, thêm cột thiếu với NaN
            for c in cols_ref:
                if c not in df.columns:
                    df[c] = pd.NA
            df = df[cols_ref]

        dfs.append(df)

    if not dfs:
        print(f"⚠️ Không tìm thấy '{file_name}' trong bất kỳ folder nào.")
        continue

    # Ghép THEO THỨ TỰ trong mảng folders (dfs đã được push theo thứ tự duyệt)
    merged_df = pd.concat(dfs, ignore_index=True)

    # Ghi ra file kết quả
    output_path = os.path.join(output_folder, file_name)
    merged_df.to_csv(output_path, index=False)
    print(f"✅ Ghép thành công (theo thứ tự folders): {file_name}")
