import os
import pandas as pd

# Đường dẫn tới thư mục chứa các file CSV
folder_path = 'City'

# Duyệt qua tất cả các file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        try:
            # Đọc toàn bộ file CSV
            df = pd.read_csv(file_path)
            
            # Nếu có ít nhất 2 dòng thì xóa 2 dòng cuối
            if len(df) >= 2:
                df = df[:-2]
                # Ghi đè lại file CSV sau khi xóa
                df.to_csv(file_path, index=False)
                print(f'Đã xử lý: {filename}')
            else:
                print(f'Bỏ qua (ít hơn 2 dòng): {filename}')
        except Exception as e:
            print(f'Lỗi khi xử lý {filename}: {e}')
