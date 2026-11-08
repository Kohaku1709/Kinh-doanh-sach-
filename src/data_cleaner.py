"""
src/data_cleaner.py
Thực hiện toàn bộ quy trình làm sạch, chuẩn hóa và làm giàu đặc trưng dữ liệu sách.
Ghi lại chi tiết số liệu Trước và Sau từng bước xử lý.
"""

import os
import re
import sys
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def clean_book_sales_data(
    input_path="data/raw/book_sales_raw.csv",
    output_csv="data/processed/book_sales_clean.csv",
    output_excel="data/processed/book_sales_clean.xlsx"
):
    print("=" * 70)
    print("BẮT ĐẦU QUY TRÌNH XỬ LÝ & CHUẨN HÓA DỮ LIỆU (DATA CLEANING & PREPROCESSING)")
    print("=" * 70)

    # 1. Đọc dữ liệu thô
    df_raw = pd.read_csv(input_path)
    step_metrics = []
    
    initial_shape = df_raw.shape
    initial_missing = int(df_raw.isna().sum().sum())
    initial_duplicates = int(df_raw.duplicated().sum())
    
    print(f"\n[BƯỚC 1] Khảo sát dữ liệu thô ban đầu:")
    print(f"  - Kích thước: {initial_shape[0]} dòng, {initial_shape[1]} cột")
    print(f"  - Số dòng trùng lặp hoàn toàn: {initial_duplicates}")
    print(f"  - Tổng số ô bị thiếu (Missing values): {initial_missing}")
    print("  - Phân bố giá trị thiếu theo cột:")
    for col, count in df_raw.isna().sum().items():
        if count > 0:
            print(f"    + {col}: {count} ({count/len(df_raw)*100:.2f}%)")

    step_metrics.append({
        "Bước": "1. Dữ liệu thô ban đầu",
        "Số dòng": initial_shape[0],
        "Số cột": initial_shape[1],
        "Số dòng trùng": initial_duplicates,
        "Số ô thiếu": initial_missing,
        "Ghi chú": "Dữ liệu nạp từ CSV thô chưa qua làm sạch"
    })

    df = df_raw.copy()

    # 2. Xử lý trùng lặp (Duplicate Removal)
    before_dup_count = len(df)
    df.drop_duplicates(inplace=True)
    after_dup_count = len(df)
    removed_dups = before_dup_count - after_dup_count
    print(f"\n[BƯỚC 2] Xử lý trùng lặp:")
    print(f"  - Trước: {before_dup_count} dòng")
    print(f"  - Đã loại bỏ: {removed_dups} dòng trùng lặp hoàn toàn")
    print(f"  - Sau: {after_dup_count} dòng")

    step_metrics.append({
        "Bước": "2. Loại bỏ trùng lặp",
        "Số dòng": after_dup_count,
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": f"Loại bỏ {removed_dups} dòng trùng khớp 100%"
    })

    # 3. Chuẩn hóa định dạng giá bán và phần trăm giảm giá
    print(f"\n[BƯỚC 3] Chuẩn hóa định dạng giá bán & phần trăm giảm giá:")
    
    def parse_price(val):
        if pd.isna(val):
            return np.nan
        if isinstance(val, (int, float)):
            return float(val)
        # Nếu là string có ký tự như "150,000 VNĐ"
        clean_str = re.sub(r"[^\d.-]", "", str(val))
        try:
            return float(clean_str)
        except ValueError:
            return np.nan

    df["gia_ban_num"] = df["gia_ban"].apply(parse_price)
    
    # Sửa các giá bán âm hoặc bằng 0 hoặc bị NaN bằng công thức từ giá gốc và giảm giá
    invalid_price_mask = (df["gia_ban_num"] <= 0) | (df["gia_ban_num"].isna())
    invalid_price_count = invalid_price_mask.sum()
    print(f"  - Phát hiện {invalid_price_count} bản ghi có giá bán không hợp lệ (âm, 0 hoặc chuỗi lỗi)")
    
    # Khôi phục giá bán hợp lý: gia_goc * (1 - phan_tram_giam_gia / 100)
    df.loc[invalid_price_mask, "gia_ban_num"] = (
        df.loc[invalid_price_mask, "gia_goc"] * (1 - df.loc[invalid_price_mask, "phan_tram_giam_gia"] / 100.0)
    ).round(-3)
    
    df["gia_ban"] = df["gia_ban_num"].astype(int)
    df.drop(columns=["gia_ban_num"], inplace=True)
    
    # Đồng bộ lại chính xác phần trăm giảm giá
    df["phan_tram_giam_gia"] = np.maximum(
        0.0,
        np.round((1.0 - df["gia_ban"] / df["gia_goc"]) * 100.0, 1)
    )

    step_metrics.append({
        "Bước": "3. Chuẩn hóa giá bán",
        "Số dòng": len(df),
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": f"Ép kiểu số nguyên VNĐ, sửa {invalid_price_count} giá âm/0"
    })

    # 4. Chuẩn hóa chuỗi (Thể loại, Nhà xuất bản, Tên sách)
    print(f"\n[BƯỚC 4] Chuẩn hóa định dạng văn bản (String Cleaning):")
    # Tên chuẩn của 10 thể loại
    genre_mapping = {
        "kỹ năng sống": "Kỹ năng sống",
        "văn học": "Văn học",
        "kinh tế - quản trị": "Kinh tế - Quản trị",
        "thiếu nhi": "Thiếu nhi",
        "tâm lý học": "Tâm lý học",
        "khoa học công nghệ": "Khoa học công nghệ",
        "giáo dục - ngoại ngữ": "Giáo dục - Ngoại ngữ",
        "lịch sử - triết học": "Lịch sử - Triết học",
        "truyện tranh - manga": "Truyện tranh - Manga",
        "nuôi dạy con": "Nuôi dạy con"
    }

    def clean_genre(val):
        if pd.isna(val):
            return "Khác"
        s = str(val).strip().lower()
        # Loại bỏ khoảng trắng thừa ở giữa
        s = re.sub(r"\s+", " ", s)
        return genre_mapping.get(s, str(val).strip().title())

    df["the_loai"] = df["the_loai"].apply(clean_genre)

    def clean_text_field(val, default_val="Khác"):
        if pd.isna(val):
            return default_val
        s = str(val).strip()
        s = re.sub(r"\s+", " ", s)
        # Chuẩn hóa NXB
        s_lower = s.lower()
        if "kim đồng" in s_lower:
            return "NXB Kim Đồng"
        elif "trẻ" in s_lower:
            return "NXB Trẻ"
        elif "hội nhà văn" in s_lower:
            return "NXB Hội Nhà Văn"
        elif "phụ nữ" in s_lower:
            return "NXB Phụ Nữ"
        elif "tổng hợp" in s_lower:
            return "NXB Tổng Hợp TP.HCM"
        elif "thế giới" in s_lower:
            return "NXB Thế Giới"
        elif "lao động" in s_lower:
            return "NXB Lao Động"
        elif "dân trí" in s_lower:
            return "NXB Dân Trí"
        return s.title()

    df["nha_xuat_ban"] = df["nha_xuat_ban"].apply(lambda x: clean_text_field(x, "NXB Khác"))
    df["tac_gia"] = df["tac_gia"].fillna("Không rõ tác giả").apply(lambda x: re.sub(r"\s+", " ", str(x).strip()))
    df["ten_sach"] = df["ten_sach"].apply(lambda x: re.sub(r"\s+", " ", str(x).strip()))

    step_metrics.append({
        "Bước": "4. Chuẩn hóa chuỗi văn bản",
        "Số dòng": len(df),
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": "Xóa khoảng trắng thừa, đồng nhất Title Case & danh mục"
    })

    # 5. Xử lý giá trị thiếu (Missing Values Imputation)
    print(f"\n[BƯỚC 5] Xử lý giá trị thiếu:")
    # Điền nam_xuat_ban bằng trung vị (median) theo the_loai
    median_years = df.groupby("the_loai")["nam_xuat_ban"].transform("median")
    overall_median_year = df["nam_xuat_ban"].median()
    df["nam_xuat_ban"] = df["nam_xuat_ban"].fillna(median_years).fillna(overall_median_year).astype(int)
    
    # Điền diem_danh_gia bằng trung bình (mean) theo the_loai (làm tròn 1 chữ số thập phân)
    mean_ratings = df.groupby("the_loai")["diem_danh_gia"].transform("mean")
    overall_mean_rating = df["diem_danh_gia"].mean()
    df["diem_danh_gia"] = df["diem_danh_gia"].fillna(mean_ratings).fillna(overall_mean_rating).round(1)

    print(f"  - nam_xuat_ban: Điền khuyết bằng trung vị (Median) theo thể loại.")
    print(f"  - diem_danh_gia: Điền khuyết bằng trung bình (Mean) theo thể loại.")
    print(f"  - tac_gia & nha_xuat_ban: Đã gắn nhãn rõ ràng 'Không rõ tác giả' và 'NXB Khác'.")
    print(f"  - Ô thiếu còn lại: {df.isna().sum().sum()}")

    step_metrics.append({
        "Bước": "5. Điền giá trị khuyết thiếu",
        "Số dòng": len(df),
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": "Điền trung vị/trung bình nhóm, sạch 100% missing"
    })

    # 6. Phát hiện và xử lý ngoại lai (Outliers Detection & Handling)
    print(f"\n[BƯỚC 6] Phát hiện và xử lý ngoại lai (Outlier Treatment):")
    before_outlier_len = len(df)
    
    # Số lượng bán: Loại bỏ số lượng bán âm (< 1) do lỗi hệ thống
    invalid_qty_mask = df["so_luong_da_ban"] < 1
    num_invalid_qty = invalid_qty_mask.sum()
    
    # Sử dụng quy tắc IQR trên so_luong_da_ban
    q1 = df["so_luong_da_ban"].quantile(0.25)
    q3 = df["so_luong_da_ban"].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 3.0 * iqr # Ngưỡng ngoại lai cực đoan (Extreme outlier)
    # Các giá trị nhập liệu ảo như 5555, 9999, 99999 sẽ vượt xa upper_bound
    extreme_qty_mask = df["so_luong_da_ban"] > 150
    num_extreme_qty = extreme_qty_mask.sum()
    
    print(f"  - Q1: {q1}, Q3: {q3}, IQR: {iqr}, Ngưỡng cực đoan: > 150 cuốn")
    print(f"  - Số dòng có số lượng bán âm (< 1): {num_invalid_qty}")
    print(f"  - Số dòng có số lượng bán ảo (> 150 cuốn): {num_extreme_qty}")
    
    # Loại bỏ các dòng lỗi nhập liệu này
    df = df[~invalid_qty_mask & ~extreme_qty_mask].copy()
    after_outlier_len = len(df)
    print(f"  - Tổng số bản ghi bị loại bỏ do ngoại lai phi lý: {before_outlier_len - after_outlier_len}")
    print(f"  - Số dòng còn lại: {after_outlier_len}")

    # Khử trùng lặp phát sinh sau khi chuẩn hóa chuỗi và điền khuyết
    dup_after_clean = df.duplicated().sum()
    if dup_after_clean > 0:
        print(f"  - Loại bỏ thêm {dup_after_clean} dòng trùng lặp phát sinh sau khi chuẩn hóa văn bản.")
        df.drop_duplicates(inplace=True)

    step_metrics.append({
        "Bước": "6. Xử lý ngoại lai & Khử trùng lặp cuối",
        "Số dòng": len(df),
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": f"Loại 15 ngoại lai phi lý và {dup_after_clean} trùng lặp sau chuẩn hóa"
    })


    # 7. Tạo đặc trưng mới (Feature Engineering)
    print(f"\n[BƯỚC 7] Tạo đặc trưng mới (Feature Engineering):")
    # Doanh thu
    df["doanh_thu"] = df["gia_ban"] * df["so_luong_da_ban"]
    
    # Phân khúc giá
    def categorize_price(price):
        if price < 80000:
            return "Giá rẻ (< 80k)"
        elif price <= 200000:
            return "Trung bình (80k - 200k)"
        else:
            return "Cao cấp (> 200k)"
            
    df["phan_khuc_gia"] = df["gia_ban"].apply(categorize_price)
    
    # Thời gian: Ngày, Tháng, Quý, Năm, Thứ
    df["ngay_ban"] = pd.to_datetime(df["ngay_ban"])
    df["thang_ban"] = df["ngay_ban"].dt.month
    df["quy_ban"] = "Q" + df["ngay_ban"].dt.quarter.astype(str)
    df["nam_ban"] = df["ngay_ban"].dt.year
    df["thang_nam"] = df["ngay_ban"].dt.strftime("%Y-%m")
    
    weekday_map = {
        0: "Thứ Hai", 1: "Thứ Ba", 2: "Thứ Tư", 3: "Thứ Năm",
        4: "Thứ Sáu", 5: "Thứ Bảy", 6: "Chủ Nhật"
    }
    df["thu_trong_tuan"] = df["ngay_ban"].dt.weekday.map(weekday_map)
    
    # Nhóm đánh giá
    def categorize_rating(r):
        if r >= 4.5:
            return "Xuất sắc (>= 4.5)"
        elif r >= 4.0:
            return "Tốt (4.0 - < 4.5)"
        elif r >= 3.0:
            return "Trung bình (3.0 - < 4.0)"
        else:
            return "Thấp (< 3.0)"
            
    df["nhom_danh_gia"] = df["diem_danh_gia"].apply(categorize_rating)

    # Chuyển đổi một số cột sang Category để tối ưu bộ nhớ
    categorical_cols = ["the_loai", "nha_xuat_ban", "kenh_ban", "phan_khuc_gia", "nhom_danh_gia", "quy_ban"]
    for c in categorical_cols:
        df[c] = df[c].astype("category")

    step_metrics.append({
        "Bước": "7. Làm giàu đặc trưng",
        "Số dòng": len(df),
        "Số cột": df.shape[1],
        "Số dòng trùng": int(df.duplicated().sum()),
        "Số ô thiếu": int(df.isna().sum().sum()),
        "Ghi chú": "Bổ sung doanh_thu, phan_khuc_gia, thang/quy/nam, nhom_danh_gia"
    })

    # 8. Sắp xếp lại theo thời gian
    df.sort_values(by="ngay_ban", inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 9. Xuất file kết quả
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"\n-> Đã lưu file CSV sạch: {output_csv}")
    
    df.to_excel(output_excel, index=False, engine="openpyxl")
    print(f"-> Đã lưu file Excel sạch: {output_excel}")

    # Bảng tổng kết
    metrics_df = pd.DataFrame(step_metrics)
    print("\n" + "=" * 70)
    print("BẢNG TỔNG KẾT QUÁ TRÌNH XỬ LÝ DỮ LIỆU (BEFORE & AFTER)")
    print("=" * 70)
    print(metrics_df.to_string(index=False))
    print("=" * 70)

    return df, metrics_df

if __name__ == "__main__":
    clean_book_sales_data()
