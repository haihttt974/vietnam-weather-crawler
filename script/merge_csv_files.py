import os
import pandas as pd

# Đường dẫn chính xác đến thư mục City từ vị trí chạy script
folder_path = 'D:/PYTHON/vietnam-weather-crawler/Citys'
output_file = 'D:/PYTHON/vietnam-weather-crawler/weather-vn.csv'

dataframes = []
header_saved = None

for i, file in enumerate(sorted(os.listdir(folder_path))):
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)

        if header_saved is None:
            df = pd.read_csv(file_path, engine='python')
            header_saved = df.columns.tolist()
        else:
            df = pd.read_csv(file_path, skiprows=1, names=header_saved, engine='python')

        dataframes.append(df)

merged_df = pd.concat(dataframes, ignore_index=True)
merged_df.to_csv(output_file, index=False)

print(f"✅ Ghép thành công {len(dataframes)} file vào '{output_file}'")