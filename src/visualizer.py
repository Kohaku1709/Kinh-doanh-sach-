"""
src/visualizer.py
Tạo toàn bộ biểu đồ trực quan hóa dữ liệu kinh doanh sách (Stage 3).
Đảm bảo định dạng chuẩn mực, font tiếng Việt hiển thị sắc nét, xuất PNG chất lượng cao.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Cấu hình font tiếng Việt và giao diện đồ họa
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({'font.size': 11, 'figure.titlesize': 14})

CHART_DIR = "charts"
os.makedirs(CHART_DIR, exist_ok=True)

def generate_all_charts(data_path="data/processed/book_sales_clean.csv"):
    print("=" * 70)
    print("BẮT ĐẦU QUY TRÌNH TRỰC QUAN HÓA DỮ LIỆU (DATA VISUALIZATION)")
    print("=" * 70)

    df = pd.read_csv(data_path)
    df["ngay_ban"] = pd.to_datetime(df["ngay_ban"])

    # -------------------------------------------------------------
    # CÂU HỎI 1: Thể loại nào bán chạy nhất / Doanh thu cao nhất?
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 1: Thể loại bán chạy nhất & Doanh thu cao nhất...")
    genre_stats = df.groupby("the_loai").agg(
        tong_doanh_thu=("doanh_thu", "sum"),
        tong_so_luong=("so_luong_da_ban", "sum")
    ).reset_index()
    genre_stats["doanh_thu_ty_dong"] = genre_stats["tong_doanh_thu"] / 1e9
    genre_stats.sort_values(by="doanh_thu_ty_dong", ascending=False, inplace=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    x = np.arange(len(genre_stats))
    width = 0.4

    bars1 = ax1.bar(x - width/2, genre_stats["doanh_thu_ty_dong"], width, label="Doanh thu (Tỷ VNĐ)", color="#1f77b4")
    ax1.set_ylabel("Doanh thu (Tỷ VNĐ)", color="#1f77b4", fontweight="bold")
    ax1.tick_params(axis='y', labelcolor="#1f77b4")
    ax1.set_xticks(x)
    ax1.set_xticklabels(genre_stats["the_loai"], rotation=30, ha="right")

    ax2 = ax1.twinx()
    bars2 = ax2.bar(x + width/2, genre_stats["tong_so_luong"], width, label="Số lượng bán (Cuốn)", color="#ff7f0e", alpha=0.85)
    ax2.set_ylabel("Số lượng bán (Cuốn)", color="#ff7f0e", fontweight="bold")
    ax2.tick_params(axis='y', labelcolor="#ff7f0e")
    ax2.grid(False)

    # Hiển thị số liệu trên cột Doanh thu
    for b in bars1:
        height = b.get_height()
        ax1.annotate(f'{height:.2f}B',
                    xy=(b.get_x() + b.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color="#1f77b4")

    plt.title("BIỂU ĐỒ 1: DOANH THU VÀ SỐ LƯỢNG BÁN THEO THỂ LOẠI SÁCH", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    chart1_path = os.path.join(CHART_DIR, "01_the_loai_doanh_thu_so_luong.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"   + Đã lưu: {chart1_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 2: Top 10 Sách & Top 10 Tác giả / NXB nổi bật
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 2: Top 10 Sách & Tác giả/Nhà xuất bản...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Top 10 Sách theo doanh thu
    top_books = df.groupby("ten_sach")["doanh_thu"].sum().reset_index()
    top_books["doanh_thu_trieu"] = top_books["doanh_thu"] / 1e6
    top_books = top_books.sort_values(by="doanh_thu_trieu", ascending=True).tail(10)

    axes[0].barh(top_books["ten_sach"], top_books["doanh_thu_trieu"], color="#2ca02c")
    axes[0].set_title("Top 10 Tựa Sách Doanh Thu Cao Nhất", fontweight="bold", fontsize=12)
    axes[0].set_xlabel("Doanh thu (Triệu VNĐ)", fontweight="bold")
    for i, v in enumerate(top_books["doanh_thu_trieu"]):
        axes[0].text(v + 1, i, f"{v:.1f} tr", va='center', fontsize=9, fontweight='bold', color="#1b6d1b")

    # Top 10 Tác giả theo số lượng bán
    top_authors = df[df["tac_gia"] != "Không rõ tác giả"].groupby("tac_gia")["so_luong_da_ban"].sum().reset_index()
    top_authors = top_authors.sort_values(by="so_luong_da_ban", ascending=True).tail(10)

    axes[1].barh(top_authors["tac_gia"], top_authors["so_luong_da_ban"], color="#9467bd")
    axes[1].set_title("Top 10 Tác Giả Có Lượng Bán Lớn Nhất", fontweight="bold", fontsize=12)
    axes[1].set_xlabel("Số lượng bán (Cuốn)", fontweight="bold")
    for i, v in enumerate(top_authors["so_luong_da_ban"]):
        axes[1].text(v + 10, i, f"{v:,} cuốn", va='center', fontsize=9, fontweight='bold', color="#582a83")

    plt.suptitle("BIỂU ĐỒ 2: TOP 10 SÁCH VÀ TOP 10 TÁC GIẢ BÁN CHẠY HÀNG ĐẦU", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    chart2_path = os.path.join(CHART_DIR, "02_top_10_sach_ban_chay.png")
    plt.savefig(chart2_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"   + Đã lưu: {chart2_path}")

    # Top Nhà xuất bản
    print("-> Đang vẽ Biểu đồ 2b: Xếp hạng Nhà xuất bản...")
    plt.figure(figsize=(10, 5))
    pub_sales = df[df["nha_xuat_ban"] != "NXB Khác"].groupby("nha_xuat_ban")["doanh_thu"].sum().reset_index()
    pub_sales["doanh_thu_ty"] = pub_sales["doanh_thu"] / 1e9
    pub_sales.sort_values(by="doanh_thu_ty", ascending=False, inplace=True)
    sns.barplot(data=pub_sales, x="doanh_thu_ty", y="nha_xuat_ban", hue="nha_xuat_ban", palette="Blues_r", legend=False)
    plt.title("XẾP HẠNG DOANH THU THEO CÁC NHÀ XUẤT BẢN", fontsize=13, fontweight="bold")
    plt.xlabel("Tổng doanh thu (Tỷ VNĐ)", fontweight="bold")
    plt.ylabel("Nhà xuất bản", fontweight="bold")
    for i, v in enumerate(pub_sales["doanh_thu_ty"]):
        plt.text(v + 0.05, i, f"{v:.2f} Tỷ ({v/pub_sales['doanh_thu_ty'].sum()*100:.1f}%)", va='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    chart3_path = os.path.join(CHART_DIR, "03_top_10_tac_gia_nha_xuat_ban.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"   + Đã lưu: {chart3_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 3: Biến động Doanh thu & Lượng bán theo thời gian (Tháng/Quý)
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 3: Xu hướng doanh thu và lượng bán theo thời gian...")
    monthly_sales = df.groupby("thang_nam").agg(
        doanh_thu=("doanh_thu", "sum"),
        so_luong=("so_luong_da_ban", "sum")
    ).reset_index()
    monthly_sales["doanh_thu_ty"] = monthly_sales["doanh_thu"] / 1e9

    fig, ax1 = plt.subplots(figsize=(14, 6))
    
    line1 = ax1.plot(monthly_sales["thang_nam"], monthly_sales["doanh_thu_ty"], marker='o', color="#d62728", linewidth=2.5, label="Doanh thu (Tỷ VNĐ)")
    ax1.set_ylabel("Doanh thu (Tỷ VNĐ)", color="#d62728", fontweight="bold")
    ax1.tick_params(axis='y', labelcolor="#d62728")
    ax1.set_xticklabels(monthly_sales["thang_nam"], rotation=45, ha="right")
    
    # Đánh dấu các mốc cao điểm mùa vụ
    # T8 (Tựu trường), T11 (Mega Sale)
    for idx, row in monthly_sales.iterrows():
        month_num = int(row["thang_nam"].split("-")[1])
        if month_num in [8, 9]:
            ax1.annotate("Mùa Tựu Trường", xy=(idx, row["doanh_thu_ty"]), xytext=(idx - 0.5, row["doanh_thu_ty"] + 0.3),
                         arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
                         fontsize=8, fontweight="bold", color="#8b0000")
        elif month_num in [11, 12]:
            ax1.annotate("Mega Sale 11-12", xy=(idx, row["doanh_thu_ty"]), xytext=(idx - 0.5, row["doanh_thu_ty"] + 0.35),
                         arrowprops=dict(facecolor='darkblue', shrink=0.05, width=1, headwidth=5),
                         fontsize=8, fontweight="bold", color="darkblue")

    ax2 = ax1.twinx()
    line2 = ax2.plot(monthly_sales["thang_nam"], monthly_sales["so_luong"], marker='s', linestyle="--", color="#1f77b4", linewidth=2, label="Số lượng bán (Cuốn)")
    ax2.set_ylabel("Số lượng bán (Cuốn)", color="#1f77b4", fontweight="bold")
    ax2.tick_params(axis='y', labelcolor="#1f77b4")
    ax2.grid(False)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=True)

    plt.title("BIỂU ĐỒ 3: BIẾN ĐỘNG DOANH THU & SẢN LƯỢNG THEO THÁNG (2024 - 2025)", fontsize=14, fontweight="bold", pad=15)
    fig.tight_layout()
    chart4_path = os.path.join(CHART_DIR, "04_xu_huong_doanh_thu_thoi_gian.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"   + Đã lưu: {chart4_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 4: Mức giảm giá & Giá bán ảnh hưởng đến Lượng bán
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 4: Ảnh hưởng của giảm giá và giá bán...")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Nhóm mức giảm giá
    df["nhom_giam_gia"] = pd.cut(
        df["phan_tram_giam_gia"],
        bins=[-1, 5, 15, 25, 35, 100],
        labels=["0% - 5%", "6% - 15%", "16% - 25%", "26% - 35%", "> 35%"]
    )

    sns.boxplot(data=df, x="nhom_giam_gia", y="so_luong_da_ban", ax=axes[0], palette="Reds", hue="nhom_giam_gia", legend=False, showmeans=True,
                meanprops={"marker":"o", "markerfacecolor":"blue", "markeredgecolor":"blue", "markersize":"8"})
    axes[0].set_title("Phân Phối Số Lượng Bán Theo Mức Giảm Giá (Boxplot)", fontweight="bold", fontsize=11)
    axes[0].set_xlabel("Mức giảm giá (%)", fontweight="bold")
    axes[0].set_ylabel("Số lượng bán mỗi đơn (Cuốn)", fontweight="bold")

    # Mối quan hệ giữa Giá bán thực tế và Lượng bán (Scatter + trendline)
    sample_scatter = df.sample(n=min(1500, len(df)), random_state=42)
    axes[1].scatter(sample_scatter["gia_ban"] / 1000, sample_scatter["so_luong_da_ban"], alpha=0.35, color="#2b5c8f", edgecolors="none")
    sns.regplot(data=sample_scatter, x=sample_scatter["gia_ban"]/1000, y="so_luong_da_ban", ax=axes[1], scatter=False, color="red", line_kws={"linewidth": 2.5})
    axes[1].set_title("Tương Quan Nghịch Giữa Giá Bán và Lượng Bán (Scatter Plot)", fontweight="bold", fontsize=11)
    axes[1].set_xlabel("Giá bán thực tế (Nghìn VNĐ)", fontweight="bold")
    axes[1].set_ylabel("Số lượng bán mỗi đơn (Cuốn)", fontweight="bold")

    plt.suptitle("BIỂU ĐỒ 4: TÁC ĐỘNG CỦA MỨC GIẢM GIÁ VÀ GIÁ BÁN LÊN SỨC MUA", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    chart5_path = os.path.join(CHART_DIR, "05_tac_dong_giam_gia_va_gia_ban.png")
    plt.savefig(chart5_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"   + Đã lưu: {chart5_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 5: Điểm đánh giá cao có đồng nghĩa với bán nhiều không?
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 5: Đánh giá sao và lượng bán...")
    corr_rating_qty = df["diem_danh_gia"].corr(df["so_luong_da_ban"])
    
    plt.figure(figsize=(10, 6))
    rating_sample = df.sample(n=min(2000, len(df)), random_state=42)
    
    sns.scatterplot(
        data=rating_sample,
        x="diem_danh_gia",
        y="so_luong_da_ban",
        hue="the_loai",
        alpha=0.6,
        palette="tab10",
        s=45
    )
    sns.regplot(data=df, x="diem_danh_gia", y="so_luong_da_ban", scatter=False, color="darkred", line_kws={"linewidth": 2.5, "label": f"Đường xu thế (r = {corr_rating_qty:.3f})"})
    
    plt.title(f"BIỂU ĐỒ 5: TƯƠNG QUAN ĐIỂM ĐÁNH GIÁ VÀ SỐ LƯỢNG BÁN (Hệ số Pearson r = {corr_rating_qty:.3f})", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Điểm đánh giá (Thang điểm 1 - 5 Sao)", fontweight="bold")
    plt.ylabel("Số lượng bán mỗi đơn (Cuốn)", fontweight="bold")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0, title="Thể loại")
    plt.tight_layout()
    chart6_path = os.path.join(CHART_DIR, "06_tuong_quan_diem_danh_gia_luong_ban.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f"   + Đã lưu: {chart6_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 6: Ma trận tương quan giữa các biến số (Heatmap)
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 6: Ma trận tương quan Heatmap...")
    numeric_cols = [
        "gia_goc", "gia_ban", "phan_tram_giam_gia",
        "so_luong_da_ban", "doanh_thu", "diem_danh_gia",
        "so_luot_danh_gia", "nam_xuat_ban"
    ]
    corr_labels = [
        "Giá Gốc", "Giá Bán", "% Giảm Giá",
        "Số Lượng Bán", "Doanh Thu", "Điểm Đánh Giá",
        "Lượt Đánh Giá", "Năm XB"
    ]
    corr_matrix = df[numeric_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.8,
        xticklabels=corr_labels,
        yticklabels=corr_labels,
        cbar_kws={'label': 'Hệ số tương quan Pearson'}
    )
    plt.title("BIỂU ĐỒ 6: MA TRẬN TƯƠNG QUAN GIỮA CÁC BIẾN SỐ ĐỊNH LƯỢNG", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    chart7_path = os.path.join(CHART_DIR, "07_ma_tran_tuong_quan.png")
    plt.savefig(chart7_path, dpi=300)
    plt.close()
    print(f"   + Đã lưu: {chart7_path}")

    # -------------------------------------------------------------
    # CÂU HỎI 7: Cơ cấu Doanh thu theo Phân khúc giá & Kênh bán
    # -------------------------------------------------------------
    print("-> Đang vẽ Biểu đồ 7: Cơ cấu doanh thu theo Phân khúc giá & Kênh bán...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # Donut Chart theo Phân khúc giá (<= 3 nhóm - chuẩn quy tắc biểu đồ tròn)
    price_seg = df.groupby("phan_khuc_gia", observed=False)["doanh_thu"].sum()
    colors_pie = ["#6baed6", "#3182bd", "#08519c"]
    wedges, texts, autotexts = axes[0].pie(
        price_seg,
        labels=price_seg.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors_pie,
        pctdistance=0.75,
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=2)
    )
    for at in autotexts:
        at.set_color('white')
        at.set_fontweight('bold')
    axes[0].set_title("Cơ Cấu Doanh Thu Theo Phân Khúc Giá", fontweight="bold", fontsize=12)

    # Bar Chart theo Kênh bán
    channel_sales = df.groupby("kenh_ban", observed=False)["doanh_thu"].sum().reset_index()
    channel_sales["doanh_thu_ty"] = channel_sales["doanh_thu"] / 1e9
    channel_sales.sort_values(by="doanh_thu_ty", ascending=False, inplace=True)

    bars_chan = axes[1].bar(channel_sales["kenh_ban"], channel_sales["doanh_thu_ty"], color=["#ff7f0e", "#2ca02c", "#1f77b4", "#d62728", "#9467bd"])
    axes[1].set_title("Doanh Thu Theo Kênh Phân Phối", fontweight="bold", fontsize=12)
    axes[1].set_ylabel("Doanh thu (Tỷ VNĐ)", fontweight="bold")
    axes[1].set_xticklabels(channel_sales["kenh_ban"], rotation=20, ha="right")
    
    total_rev = channel_sales["doanh_thu_ty"].sum()
    for b in bars_chan:
        h = b.get_height()
        pct = (h / total_rev) * 100
        axes[1].annotate(f'{h:.2f}B\n({pct:.1f}%)',
                         xy=(b.get_x() + b.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.suptitle("BIỂU ĐỒ 7: CƠ CẤU DOANH THU THEO PHÂN KHÚC GIÁ VÀ KÊNH BÁN", fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout()
    chart8_path = os.path.join(CHART_DIR, "08_co_cau_doanh_thu_phan_khuc_kenh_ban.png")
    plt.savefig(chart8_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"   + Đã lưu: {chart8_path}")

    print("=" * 70)
    print("HOÀN TẤT TẠO TOÀN BỘ 7 BIỂU ĐỒ PNG!")
    print("=" * 70)

if __name__ == "__main__":
    generate_all_charts()
