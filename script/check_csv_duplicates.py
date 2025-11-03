# === CẤU HÌNH ===
URL_PART = "D://PYTHON//vietnam-weather-crawler//03-Citys//AnGiang-LongXuyen.csv" 
CSV_SEP = ","                        # ký tự phân tách cột
CSV_ENCODING = "utf-8"               # encoding
SHOW_MAX = 20                        # in tối đa N dòng trùng ra màn hình
# =================

import sys
import pandas as pd
from pathlib import Path

def main():
    csv_path = sys.argv[1] if len(sys.argv) > 1 else URL_PART

    if not csv_path:
        print("⚠️ Chưa cấu hình URL_PART và cũng không truyền đường dẫn qua CLI.", file=sys.stderr)
        sys.exit(2)

    p = Path(csv_path)
    if not p.exists():
        print(f"⚠️ Không tìm thấy file: {p}", file=sys.stderr)
        sys.exit(2)

    try:
        df = pd.read_csv(p, sep=CSV_SEP, encoding=CSV_ENCODING, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"⚠️ Lỗi khi đọc CSV: {e}", file=sys.stderr)
        sys.exit(2)

    total_rows = len(df)

    dup_mask = df.duplicated(keep=False)
    dup_rows = df[dup_mask]

    if dup_rows.empty:
        print(f"✅ Không phát hiện dòng trùng. Tổng số dòng: {total_rows} (so sánh toàn bộ dòng).")
        sys.exit(0)

    counts = (dup_rows.groupby(list(df.columns), dropna=False)
                        .size()
                        .reset_index(name="count")
                        .sort_values("count", ascending=False))

    num_groups = len(counts)

    print("⚠️ PHÁT HIỆN DÒNG TRÙNG")
    print(f"- File: {p}")
    print(f"- Tổng số dòng: {total_rows}")
    print(f"- Số nhóm dòng trùng: {num_groups}")
    print(f"- Tổng số bản ghi thuộc các nhóm trùng: {len(dup_rows)}")
    print("\nTop các dòng bị lặp nhiều nhất (đếm theo số lần xuất hiện):")
    print(counts.head(10).to_string(index=False))

    print(f"\nVí dụ các dòng trùng (tối đa {SHOW_MAX} dòng):")
    print(dup_rows.head(SHOW_MAX).to_string(index=False))

    # Trả mã thoát 1 nếu có trùng
    sys.exit(1)

if __name__ == "__main__":
    main()
