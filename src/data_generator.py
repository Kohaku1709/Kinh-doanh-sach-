"""
src/data_generator.py
Tạo bộ dữ liệu mô phỏng kinh doanh sách bán lẻ tại Việt Nam.
Tuân thủ tính tái lập (Fixed Seed) và phản ánh sát thực tế thị trường.
"""

import os
import sys
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

RANDOM_SEED = 42

def generate_book_sales_data(output_path="data/raw/book_sales_raw.csv", num_records=6500, seed=RANDOM_SEED):
    np.random.seed(seed)
    random.seed(seed)
    
    # 1. Danh mục thể loại và phân bổ xác suất thị trường
    genres = [
        "Kỹ năng sống", "Văn học", "Kinh tế - Quản trị", "Thiếu nhi",
        "Tâm lý học", "Khoa học công nghệ", "Giáo dục - Ngoại ngữ",
        "Lịch sử - Triết học", "Truyện tranh - Manga", "Nuôi dạy con"
    ]
    genre_weights = [0.20, 0.18, 0.15, 0.13, 0.09, 0.06, 0.07, 0.04, 0.05, 0.03]
    
    # 2. Danh mục tác giả tiêu biểu theo thể loại
    authors_by_genre = {
        "Kỹ năng sống": ["James Clear", "Dale Carnegie", "Stephen R. Covey", "Nguyễn Hiến Lê", "Rosie Nguyễn", "Thiền sư Thích Nhất Hạnh", "Robin Sharma", "Mark Manson"],
        "Văn học": ["Nguyễn Nhật Ánh", "Nguyễn Ngọc Tư", "Haruki Murakami", "Paulo Coelho", "George Orwell", "Nguyễn Du", "Nam Cao", "Gabriel Garcia Marquez", "Franz Kafka"],
        "Kinh tế - Quản trị": ["Morgan Housel", "Philip Kotler", "Robert Kiyosaki", "Peter Drucker", "Michael Porter", "Jim Collins", "Trần Sĩ Chương", "Daniel Kahneman"],
        "Thiếu nhi": ["Tô Hoài", "J.K. Rowling", "Astrid Lindgren", "Antoine de Saint-Exupéry", "Nguyễn Nhật Ánh", "Vũ Hùng", "Trần Đăng Khoa"],
        "Tâm lý học": ["Daniel Kahneman", "Carl Jung", "Sigmund Freud", "Haemin", "Viktor Frankl", "Carol Dweck", "Robert Cialdini"],
        "Khoa học công nghệ": ["Yuval Noah Harari", "Stephen Hawking", "Walter Isaacson", "Carl Sagan", "Michio Kaku", "Andrew Ng"],
        "Giáo dục - Ngoại ngữ": ["Mai Lan Hương", "Raymond Murphy", "Nguyễn Thu Lệ", "Vĩnh Bá", "Lê Đình Lực"],
        "Lịch sử - Triết học": ["Trần Trọng Kim", "Đào Duy Anh", "Will Durant", "Marcus Aurelius", "Khổng Tử", "Sun Tzu"],
        "Truyện tranh - Manga": ["Fujiko F. Fujio", "Eiichiro Oda", "Gosho Aoyama", "Masashi Kishimoto", "Akira Toriyama"],
        "Nuôi dạy con": ["Adele Faber", "Maria Montessori", "Trần Thị Ái Liên", "Nguyễn Thị Thu", "John Gray"]
    }
    
    # 3. Nhà xuất bản
    publishers = [
        "NXB Trẻ", "NXB Kim Đồng", "NXB Hội Nhà Văn", "NXB Phụ Nữ",
        "NXB Tổng Hợp TP.HCM", "NXB Thế Giới", "NXB Lao Động", "NXB Dân Trí"
    ]
    
    # 4. Tạo kho đầu sách (1,200 cuốn)
    book_catalog = []
    book_id_counter = 1
    
    sample_titles = {
        "Kỹ năng sống": ["Thay Đổi Tí Hon Hiệu Quả Bất Ngờ", "Đắc Nhân Tâm", "7 Thói Quen Của Người Thành Đạt", "Tuổi Trẻ Đáng Giá Bao Nhiêu", "Nghệ Thuật Tinh Tế Của Việc Đếch Quan Tâm", "Hiểu Về Trái Tim", "Đời Ngắn Đừng Ngủ Dài", "Khéo Ăn Nói Sẽ Có Được Thiên Hạ"],
        "Văn học": ["Mắt Biếc", "Cánh Đồng Bất Tận", "Rừng Na Uy", "Nhà Giả Kim", "1984", "Truyện Kiều", "Số Đỏ", "Trăm Năm Cô Đơn", "Hoàng Tử Bé", "Tôi Thấy Hoa Vàng Trên Cỏ Xanh"],
        "Kinh tế - Quản trị": ["Tâm Lý Học Về Tiền", "Dạy Con Làm Giàu", "Quản Trị Chiến Lược", "Từ Tốt Đến Vĩ Đại", "Tiếp Thị 5.0", "Blink: Điểm Bùng Phát", "Chiến Lược Đại Dương Xanh", "Khởi Nghiệp Tinh Gọn"],
        "Thiếu nhi": ["Dế Mèn Phiêu Lưu Ký", "Harry Potter và Hòn Đá Phù Thủy", "Pippi Tất Dài", "Chuyện Con Mèo Dạy Hải Âu Bay", "Búp Sen Xanh", "Vừa Nhắm Mắt Vừa Mở Cửa Sổ", "Đất Rừng Phương Nam"],
        "Tâm lý học": ["Tư Duy Nhanh Và Chậm", "Bước Chậm Lại Giữa Thế Gian Vội Vã", "Đi Tìm Lẽ Sống", "Tâm Lý Học Đám Đông", "Tâm Lý Học Hành Vi", "Nghịch Lý Của Sự Lựa Chọn"],
        "Khoa học công nghệ": ["Sapiens: Lược Sử Loài Người", "Lược Sử Thời Gian", "Steve Jobs - Tiểu Sử", "Vũ Trụ Trong Vỏ Hạt Dẻ", "Gen: Lịch Sử Vô Hình", "Trí Tuệ Nhân Tạo 2041"],
        "Giáo dục - Ngoại ngữ": ["Giải Thích Ngữ Pháp Tiếng Anh", "English Grammar in Use", "Tự Học 2000 Từ Vựng Tiếng Anh", "IELTS Reading Strategies", "Luyện Siêu Trí Nhớ Từ Vựng"],
        "Lịch sử - Triết học": ["Việt Nam Sử Lược", "Đại Việt Sử Ký Toàn Thư", "Sử Việt - 12 Khúc Tráng Ca", "Suy Tưởng", "Lược Sử Triết Học Tây Phương", "Binh Pháp Tôn Tử"],
        "Truyện tranh - Manga": ["Doraemon Toàn Tập", "One Piece - Đảo Hải Tặc", "Thám Tử Lừng Danh Conan", "Naruto Truyền Kỳ", "Dragon Ball - 7 Viên Ngọc Rồng"],
        "Nuôi dạy con": ["Cha Mẹ Vô Điều Kiện", "Phương Pháp Giáo Dục Montessori", "Kỷ Luật Không Nước Mắt", "Nuôi Con Không Phải Là Cuộc Chiến", "Làm Mẹ Không Áp Lực"]
    }
    
    for g in genres:
        titles_pool = sample_titles.get(g, ["Sách Hay " + g])
        authors_pool = authors_by_genre[g]
        for i in range(120): # 120 cuốn mỗi thể loại = 1,200 cuốn
            base_title = titles_pool[i % len(titles_pool)]
            title = f"{base_title} (Tập {i//len(titles_pool) + 1})" if i >= len(titles_pool) else base_title
            author = random.choice(authors_pool)
            pub = random.choice(publishers)
            pub_year = random.randint(2015, 2024)
            base_price = int(np.random.choice([
                np.random.randint(45, 95) * 1000,
                np.random.randint(95, 180) * 1000,
                np.random.randint(180, 350) * 1000
            ], p=[0.4, 0.45, 0.15]))
            
            book_catalog.append({
                "ma_sach": f"BK{book_id_counter:05d}",
                "ten_sach": title,
                "tac_gia": author,
                "the_loai": g,
                "nha_xuat_ban": pub,
                "nam_xuat_ban": pub_year,
                "gia_goc": base_price
            })
            book_id_counter += 1

    # 5. Sinh dữ liệu giao dịch 24 tháng (2024-01-01 đến 2025-12-31)
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31)
    total_days = (end_date - start_date).days
    
    channels = ["Shopee Mall", "TikTok Shop", "Tiki Trading", "Cửa hàng Offline", "Website Nhà sách"]
    channel_weights = [0.35, 0.22, 0.18, 0.15, 0.10]
    
    records = []
    
    for i in range(num_records):
        # Chọn sách theo xác suất thể loại
        chosen_genre = np.random.choice(genres, p=genre_weights)
        matching_books = [b for b in book_catalog if b["the_loai"] == chosen_genre]
        book = random.choice(matching_books)
        
        # Chọn ngày
        day_offset = random.randint(0, total_days)
        trans_date = start_date + timedelta(days=day_offset)
        month = trans_date.month
        
        # Hệ số mùa vụ (Seasonality)
        seasonal_mult = 1.0
        if month in [1, 2]: # Tết
            seasonal_mult = 1.3
        elif month in [8, 9]: # Tựu trường
            seasonal_mult = 1.5 if book["the_loai"] in ["Giáo dục - Ngoại ngữ", "Thiếu nhi", "Kỹ năng sống"] else 1.2
        elif month in [11, 12]: # Mega Sale 11/11, 12/12, Black Friday
            seasonal_mult = 1.7
        elif month in [6, 7]: # Nghỉ hè thiếu nhi
            seasonal_mult = 1.3 if book["the_loai"] in ["Thiếu nhi", "Truyện tranh - Manga"] else 1.05
            
        # Kênh bán
        channel = np.random.choice(channels, p=channel_weights)
        
        # Mức giảm giá (%)
        if channel in ["Shopee Mall", "TikTok Shop", "Tiki Trading"]:
            discount_pct = float(np.random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40], p=[0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.08, 0.05, 0.02]))
        else:
            discount_pct = float(np.random.choice([0, 5, 10, 15, 20], p=[0.35, 0.3, 0.2, 0.1, 0.05]))
            
        gia_goc = book["gia_goc"]
        gia_ban = int(round(gia_goc * (1 - discount_pct / 100.0) / 1000.0) * 1000)
        
        # Số lượng bán (Tương quan nghịch với giá bán, tương quan thuận với giảm giá và mùa vụ)
        price_factor = max(0.5, 1.8 - (gia_ban / 200000.0))
        discount_factor = 1.0 + (discount_pct / 30.0)
        
        expected_qty = int(np.random.poisson(lam=4.0 * seasonal_mult * price_factor * discount_factor))
        so_luong_da_ban = max(1, min(120, expected_qty))
        
        # Đánh giá & lượt đánh giá
        # Sách bán nhiều thường tích lũy nhiều lượt đánh giá
        so_luot_danh_gia = int(np.random.exponential(scale=so_luong_da_ban * 2.5) + np.random.randint(5, 50))
        
        # Điểm đánh giá (phân phối lệch trái quanh 4.2 - 4.8)
        raw_score = np.random.beta(a=12, b=2.2) * 5.0
        diem_danh_gia = round(float(np.clip(raw_score, 1.0, 5.0)), 1)
        
        records.append({
            "ma_sach": book["ma_sach"],
            "ten_sach": book["ten_sach"],
            "tac_gia": book["tac_gia"],
            "the_loai": book["the_loai"],
            "nha_xuat_ban": book["nha_xuat_ban"],
            "nam_xuat_ban": book["nam_xuat_ban"],
            "gia_goc": gia_goc,
            "gia_ban": gia_ban,
            "phan_tram_giam_gia": discount_pct,
            "so_luong_da_ban": so_luong_da_ban,
            "diem_danh_gia": diem_danh_gia,
            "so_luot_danh_gia": so_luot_danh_gia,
            "ngay_ban": trans_date.strftime("%Y-%m-%d"),
            "kenh_ban": channel
        })

    df = pd.DataFrame(records)

    # 6. Cố ý đưa vào các lỗi thực tế (Dirty Data Injection) để phục vụ Giai đoạn 2
    print(f"-> Tạo dữ liệu gốc sạch ban đầu: {len(df)} dòng.")
    
    # 6.1. Dòng trùng lặp (160 dòng trùng lặp hoàn toàn do lỗi đồng bộ hóa)
    dup_indices = np.random.choice(len(df), size=160, replace=False)
    duplicates = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)
    print(f"-> Sau khi thêm 160 dòng duplicate: {len(df)} dòng.")
    
    # 6.2. Thiếu giá trị (Missing Values)
    # Nha xuat ban bi thieu
    missing_pub_idx = np.random.choice(len(df), size=130, replace=False)
    df.loc[missing_pub_idx, "nha_xuat_ban"] = np.nan
    
    # Diem danh gia bi thieu (chua co review hoac loi crawl)
    missing_rating_idx = np.random.choice(len(df), size=110, replace=False)
    df.loc[missing_rating_idx, "diem_danh_gia"] = np.nan
    
    # Nam xuat ban bi thieu
    missing_year_idx = np.random.choice(len(df), size=85, replace=False)
    df.loc[missing_year_idx, "nam_xuat_ban"] = np.nan
    
    # Tac gia bi thieu
    missing_auth_idx = np.random.choice(len(df), size=45, replace=False)
    df.loc[missing_auth_idx, "tac_gia"] = np.nan

    # 6.3. Sai định dạng chuỗi & khoảng trắng, chữ hoa/thường (Text inconsistency)
    # The loai: chen khoang trang, viet thuong, viet hoa
    dirty_genre_idx = np.random.choice(len(df), size=250, replace=False)
    for idx in dirty_genre_idx:
        val = df.loc[idx, "the_loai"]
        if isinstance(val, str):
            rand_opt = random.randint(1, 3)
            if rand_opt == 1:
                df.loc[idx, "the_loai"] = f"  {val.lower()}  "
            elif rand_opt == 2:
                df.loc[idx, "the_loai"] = val.upper()
            else:
                df.loc[idx, "the_loai"] = f"{val}  "
                
    # Nha xuat ban: chu thuong, khoang trang
    dirty_pub_idx = np.random.choice(len(df), size=200, replace=False)
    for idx in dirty_pub_idx:
        val = df.loc[idx, "nha_xuat_ban"]
        if pd.notna(val) and isinstance(val, str):
            rand_opt = random.randint(1, 3)
            if rand_opt == 1:
                df.loc[idx, "nha_xuat_ban"] = f"  {val.lower()} "
            elif rand_opt == 2:
                df.loc[idx, "nha_xuat_ban"] = val.upper()
            else:
                df.loc[idx, "nha_xuat_ban"] = f"  {val}  "

    # 6.4. Sai định dạng số (Formatting & Negative values)
    # gia_ban co chuoi dang "150,000" hoac float kem string
    df["gia_ban_raw"] = df["gia_ban"].astype(object)
    string_price_idx = np.random.choice(len(df), size=120, replace=False)
    for idx in string_price_idx:
        val = df.loc[idx, "gia_ban"]
        if pd.notna(val):
            df.loc[idx, "gia_ban_raw"] = f"{int(val):,} VNĐ"
            
    # Thay the cot gia_ban bang gia_ban_raw
    df["gia_ban"] = df["gia_ban_raw"]
    df.drop(columns=["gia_ban_raw"], inplace=True)
    
    # 6.5. Gia tri am hoac 0 phi ly
    anomaly_price_idx = np.random.choice(len(df), size=15, replace=False)
    for idx in anomaly_price_idx:
        df.loc[idx, "gia_ban"] = -50000 if random.random() > 0.5 else 0

    # 6.6. Ngoại lai số lượng bán (Outliers phi lý: so am hoac so qua lon nhu 99999 do loi nhap lieu)
    outlier_qty_idx = np.random.choice(len(df), size=15, replace=False)
    for i, idx in enumerate(outlier_qty_idx):
        if i < 8:
            df.loc[idx, "so_luong_da_ban"] = random.choice([5555, 9999, 99999])
        else:
            df.loc[idx, "so_luong_da_ban"] = -10

    # Xao tron vi tri
    df = df.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"-> Đã ghi file dữ liệu thô: {output_path} | Kích thước: {df.shape}")
    return df

if __name__ == "__main__":
    generate_book_sales_data()
