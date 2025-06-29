import csv
import os
import json
from datetime import datetime

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_column_index(header, col_letter):
    col_letter = col_letter.upper()
    index = ord(col_letter) - ord('A')
    if index < 0 or index >= len(header):
        return None
    return index

def print_menu():
    print("╔══════════════════════════════════════════════╗")
    print("║         📊 CHƯƠNG TRÌNH XỬ LÝ FILE CSV       ║")
    print("╠══════════════════════════════════════════════╣")
    print("║ 1. Xóa chuỗi theo cột hoặc toàn bộ           ║")
    print("║ 2. Thống kê giá trị duy nhất trong 1 cột     ║")
    print("║ 3. Tìm và thay thế trong cột hoặc toàn bộ    ║")
    print("║ 4. Chuyển hoa/thường dữ liệu trong cột       ║")
    print("║ 5. Xóa dòng rỗng hoặc chứa chuỗi             ║")
    print("║ 6. Gộp hoặc tách cột                         ║")
    print("║ 7. Lọc dữ liệu theo điều kiện                ║")
    print("║ 8. Thống kê (tổng, trung bình...) theo cột   ║")
    print("║ 9. Sắp xếp theo cột                          ║")
    print("║ 10. Xử lý dữ liệu thời gian                  ║")
    print("║ 11. Xuất ra định dạng khác (JSON, TXT...)    ║")
    print("║ 12. Kiểm tra dữ liệu lỗi, thiếu              ║")
    print("║ 13. Xem nhanh (Preview 5 dòng đầu/cuối)      ║")
    print("║ 14. Đổi đường dẫn file CSV                   ║")
    print("║ 0. Thoát chương trình                        ║")
    print("╚══════════════════════════════════════════════╝")

def load_csv(file_path, silent=False):
    if not os.path.exists(file_path):
        if not silent:
            print("❌ File không tồn tại.")
        return None
    if not os.path.isfile(file_path):
        if not silent:
            print("❌ Đường dẫn không phải là file.")
        return None
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            lines = list(reader)
        return lines
    except Exception as e:
        if not silent:
            print(f"❌ Lỗi khi đọc file: {e}")
        return None

def save_csv(file_path, data):
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        print("✅ Đã lưu file thành công.")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file: {e}")

def doi_duong_dan_file():
    new_path = input("🔁 Nhập đường dẫn file CSV mới: ").strip()
    if os.path.exists(new_path):
        print("✅ Đã cập nhật đường dẫn.")
        return new_path
    else:
        print("❌ Đường dẫn không tồn tại.")
        return None

# Các chức năng CSV cơ bản
def chuc_nang_1_xoa_chuoi(lines):
    text = input("🔤 Nhập chuỗi cần xóa: ")
    col = input("📌 Nhập cột muốn áp dụng (A, B...) hoặc Enter để áp dụng toàn bộ: ").strip().upper()
    count = 0
    if col:
        col_idx = get_column_index(lines[0], col)
        if col_idx is None:
            print("❌ Cột không hợp lệ.")
            return lines
        for row in lines[1:]:
            if col_idx < len(row):
                count += row[col_idx].count(text)
                row[col_idx] = row[col_idx].replace(text, "")
    else:
        for row in lines[1:]:
            for i in range(len(row)):
                count += row[i].count(text)
                row[i] = row[i].replace(text, "")
    print(f"✅ Đã xóa {count} lần xuất hiện của chuỗi '{text}'.")
    return lines

def chuc_nang_2_thong_ke(lines):
    col = input("📌 Nhập cột cần thống kê (A, B, ...): ").strip().upper()
    col_idx = get_column_index(lines[0], col)
    if col_idx is None:
        print("❌ Cột không hợp lệ.")
        return
    values = {}
    for row in lines[1:]:
        if col_idx < len(row):
            val = row[col_idx]
            values[val] = values.get(val, 0) + 1
    for val, count in values.items():
        print(f"{val}: {count} lần")

def chuc_nang_3_tim_thay(lines):
    target = input("🔍 Chuỗi cần tìm: ")
    replace = input("✏️ Chuỗi thay thế: ")
    col = input("📌 Nhập cột áp dụng hoặc Enter để toàn bộ: ").strip().upper()
    count = 0
    if col:
        col_idx = get_column_index(lines[0], col)
        if col_idx is None:
            print("❌ Cột không hợp lệ.")
            return lines
        for row in lines[1:]:
            if col_idx < len(row):
                count += row[col_idx].count(target)
                row[col_idx] = row[col_idx].replace(target, replace)
    else:
        for row in lines[1:]:
            for i in range(len(row)):
                count += row[i].count(target)
                row[i] = row[i].replace(target, replace)
    print(f"✅ Đã thay thế {count} lần.")
    return lines

def chuc_nang_4_chuyen_hoa_thuong(lines):
    mode = input("🔁 Chọn chế độ (upper/lower): ").strip().lower()
    col = input("📌 Nhập cột áp dụng (A, B,...): ").strip().upper()
    col_idx = get_column_index(lines[0], col)
    if col_idx is None:
        print("❌ Cột không hợp lệ.")
        return lines
    for row in lines[1:]:
        if col_idx < len(row):
            row[col_idx] = row[col_idx].upper() if mode == 'upper' else row[col_idx].lower()
    print("✅ Đã chuyển đổi.")
    return lines

def chuc_nang_5_xoa_dong_rong(lines):
    key = input("🔤 Nhập chuỗi (Enter nếu muốn xóa dòng rỗng): ").strip()
    new_lines = [lines[0]]
    for row in lines[1:]:
        if key:
            if not any(key in cell for cell in row):
                new_lines.append(row)
        else:
            if any(cell.strip() for cell in row):
                new_lines.append(row)
    print(f"✅ Đã xóa {len(lines) - len(new_lines)} dòng.")
    return new_lines

def chuc_nang_6_gop_tach(lines):
    action = input("🛠️ Gõ 'gop' để gộp hoặc 'tach' để tách cột: ").strip().lower()
    if action == 'gop':
        cols = input("📌 Nhập các cột muốn gộp (VD: A,B,C): ").strip().split(',')
        sep = input("🔗 Nhập ký tự phân tách: ")
        indices = [get_column_index(lines[0], c.strip()) for c in cols]
        for row in lines[1:]:
            values = [row[i] if i < len(row) else "" for i in indices]
            row.append(sep.join(values))
        lines[0].append("GopCot")
        print("✅ Đã gộp cột.")
    elif action == 'tach':
        col = input("📌 Cột muốn tách (A, B...): ").strip().upper()
        sep = input("🔗 Ký tự phân tách: ")
        idx = get_column_index(lines[0], col)
        new_col_names = input("📌 Nhập tên các cột mới (cách nhau dấu phẩy): ").split(",")
        lines[0].extend(new_col_names)
        for row in lines[1:]:
            if idx < len(row):
                parts = row[idx].split(sep)
                row.extend(parts)
        print("✅ Đã tách cột.")
    return lines

def chuc_nang_7_loc(lines):
    col = input("📌 Nhập cột cần lọc (A, B...): ").strip().upper()
    value = input("🔎 Giá trị cần lọc: ")
    col_idx = get_column_index(lines[0], col)
    if col_idx is None:
        print("❌ Cột không hợp lệ.")
        return lines
    result = [lines[0]]
    for row in lines[1:]:
        if col_idx < len(row) and row[col_idx] == value:
            result.append(row)
    print(f"✅ Lọc được {len(result)-1} dòng.")
    return result

def chuc_nang_8_thong_ke_so(lines):
    col = input("📌 Nhập cột số (A, B...): ").strip().upper()
    col_idx = get_column_index(lines[0], col)
    values = []
    for row in lines[1:]:
        try:
            values.append(float(row[col_idx]))
        except:
            continue
    if not values:
        print("❌ Không có giá trị số.")
        return
    print(f"🔢 Tổng: {sum(values)}, Trung bình: {sum(values)/len(values):.2f}, Min: {min(values)}, Max: {max(values)}")

def chuc_nang_9_sap_xep(lines):
    col = input("📌 Cột cần sắp xếp (A, B...): ").strip().upper()
    rev = input("🔽 Sắp giảm? (y/n): ").strip().lower() == 'y'
    col_idx = get_column_index(lines[0], col)
    try:
        lines[1:] = sorted(lines[1:], key=lambda x: x[col_idx], reverse=rev)
        print("✅ Đã sắp xếp.")
    except:
        print("❌ Lỗi sắp xếp.")
    return lines

def chuc_nang_10_thoi_gian(lines):
    col = input("📅 Cột thời gian (A, B...): ").strip().upper()
    fmt = input("🕒 Định dạng thời gian (VD: %Y-%m-%d %H:%M:%S): ")
    col_idx = get_column_index(lines[0], col)
    for row in lines[1:]:
        try:
            row[col_idx] = str(datetime.strptime(row[col_idx], fmt))
        except:
            continue
    print("✅ Đã chuyển đổi thời gian.")
    return lines

def chuc_nang_11_xuat(lines):
    fmt = input("💾 Định dạng xuất (json/txt): ").strip().lower()
    name = input("📄 Tên file xuất (không cần đuôi): ").strip()
    if fmt == "json":
        with open(name + ".json", "w", encoding="utf-8") as f:
            keys = lines[0]
            json.dump([dict(zip(keys, row)) for row in lines[1:]], f, ensure_ascii=False, indent=2)
        print("✅ Đã lưu file JSON.")
    elif fmt == "txt":
        with open(name + ".txt", "w", encoding="utf-8") as f:
            for row in lines:
                f.write(" | ".join(row) + "\n")
        print("✅ Đã lưu file TXT.")

def chuc_nang_12_kiem_tra_loi(lines):
    for i, row in enumerate(lines[1:], start=2):
        if len(row) != len(lines[0]):
            print(f"⚠️ Dòng {i} thiếu/thừa cột: {row}")
        elif not any(cell.strip() for cell in row):
            print(f"⚠️ Dòng {i} rỗng")

def chuc_nang_13_preview(lines):
    print("🔍 5 dòng đầu:")
    for row in lines[:6]:
        print(row)
    print("🔍 5 dòng cuối:")
    for row in lines[-5:]:
        print(row)

def main():
    file_path = input("📁 Nhập đường dẫn tới file CSV: ").strip()
    if not os.path.exists(file_path):
        print("❌ File không tồn tại.")
        return
    lines = load_csv(file_path)
    while True:
        clear()
        print(f"📂 File đang làm việc: {file_path}")
        print_menu()
        choice = input("👉 Chọn chức năng (0-14): ").strip()
        if choice == "0":
            break
        elif choice == "1":
            lines = chuc_nang_1_xoa_chuoi(lines)
        elif choice == "2":
            chuc_nang_2_thong_ke(lines)
        elif choice == "3":
            lines = chuc_nang_3_tim_thay(lines)
        elif choice == "4":
            lines = chuc_nang_4_chuyen_hoa_thuong(lines)
        elif choice == "5":
            lines = chuc_nang_5_xoa_dong_rong(lines)
        elif choice == "6":
            lines = chuc_nang_6_gop_tach(lines)
        elif choice == "7":
            lines = chuc_nang_7_loc(lines)
        elif choice == "8":
            chuc_nang_8_thong_ke_so(lines)
        elif choice == "9":
            lines = chuc_nang_9_sap_xep(lines)
        elif choice == "10":
            lines = chuc_nang_10_thoi_gian(lines)
        elif choice == "11":
            chuc_nang_11_xuat(lines)
        elif choice == "12":
            chuc_nang_12_kiem_tra_loi(lines)
        elif choice == "13":
            chuc_nang_13_preview(lines)
        elif choice == '14':
            new_path = input("🔁 Nhập đường dẫn file CSV mới: ").strip()
            temp_data = load_csv(new_path, silent=True)
            if temp_data:
                data = temp_data
                file_path = new_path
                print("✅ Đã cập nhật đường dẫn.")
            else:
                print("❌ Không thể đọc file. Vui lòng kiểm tra lại đường dẫn.")
                
        input("\nNhấn Enter để quay lại menu...")

if __name__ == "__main__":
    main()
