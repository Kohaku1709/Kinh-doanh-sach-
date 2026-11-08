# DỰ ÁN: XÂY DỰNG BỘ DỮ LIỆU KINH DOANH SÁCH, XỬ LÝ, TRỰC QUAN HÓA VÀ RÚT RA CÁC Ý NGHĨA KINH DOANH

Dự án phân tích dữ liệu toàn diện (End-to-End Data Analytics & Engineering) về hoạt động kinh doanh sách bán lẻ đa kênh tại thị trường Việt Nam giai đoạn 2024 - 2025.

---

## 1. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
Datacrawl/
├── data/
│   ├── raw/
│   │   └── book_sales_raw.csv           # Dữ liệu thô ban đầu (6,660 dòng, 14 cột)
│   ├── processed/
│   │   ├── book_sales_clean.csv         # Dữ liệu đã làm sạch & tạo đặc trưng (6,501 dòng, 22 cột)
│   │   └── book_sales_clean.xlsx        # File Excel dữ liệu sạch chuẩn hóa
│   └── data_dictionary.md               # Từ điển dữ liệu mô tả chi tiết tất cả các cột
├── notebooks/
│   └── book_sales_analysis.ipynb        # Jupyter Notebook hoàn chỉnh, chạy sạch từ đầu đến cuối
├── src/
│   ├── __init__.py
│   ├── data_generator.py                # Mã nguồn sinh dữ liệu mô phỏng sát thực tế (Seed=42)
│   ├── data_cleaner.py                  # Mã nguồn làm sạch, chuẩn hóa chuỗi, xử lý missing & ngoại lai
│   ├── visualizer.py                    # Mã nguồn vẽ toàn bộ biểu đồ phân tích chuẩn tiếng Việt (PNG)
│   └── dashboard_builder.py             # Mã nguồn tạo Dashboard HTML tương tác (Plotly + Tailwind)
├── charts/
│   ├── 01_the_loai_doanh_thu_so_luong.png
│   ├── 02_top_10_sach_ban_chay.png
│   ├── 03_top_10_tac_gia_nha_xuat_ban.png
│   ├── 04_xu_huong_doanh_thu_thoi_gian.png
│   ├── 05_tac_dong_giam_gia_va_gia_ban.png
│   ├── 06_tuong_quan_diem_danh_gia_luong_ban.png
│   ├── 07_ma_tran_tuong_quan.png
│   ├── 08_co_cau_doanh_thu_phan_khuc_kenh_ban.png
│   └── dashboard.html                   # Dashboard tương tác độc lập (Mở bằng trình duyệt bất kỳ)
├── report/
│   └── bao_cao.md                       # Báo cáo chuyên sâu 6 phần theo yêu cầu
├── README.md                            # Hướng dẫn cài đặt và vận hành toàn bộ dự án
└── requirements.txt                     # Danh sách các thư viện phụ thuộc
```

---

## 2. HƯỚNG DẪN CÀI ĐẶT MÔI TRƯỜNG

### 2.1. Yêu cầu hệ thống
* **Python:** Phiên bản `>= 3.9` (Khuyến nghị Python 3.10, 3.11 hoặc 3.12/3.14).
* Trình duyệt web (Chrome, Edge, Firefox) để mở Dashboard HTML.

### 2.2. Cài đặt các thư viện cần thiết
Mở terminal / PowerShell tại thư mục gốc của dự án (`Datacrawl/`) và chạy lệnh sau:

```bash
pip install -r requirements.txt
```

Các thư viện chính được sử dụng:
* `pandas` & `numpy`: Xử lý, tính toán và làm sạch dữ liệu bảng.
* `matplotlib` & `seaborn`: Vẽ đồ thị trực quan hóa tĩnh độ phân giải cao (300 DPI), hỗ trợ font tiếng Việt.
* `plotly`: Xây dựng biểu đồ tương tác và dashboard điều hành.
* `openpyxl`: Đọc và ghi file dữ liệu Excel `.xlsx`.
* `nbformat` & `ipykernel`: Khởi tạo và thực thi Jupyter Notebook.

---

## 3. HƯỚNG DẪN CHẠY LẠI TOÀN BỘ DỰ ÁN TỪ ĐẦU ĐẾN CUỐI

Bạn có thể chạy toàn bộ quy trình chỉ bằng các lệnh sau:

### Bước 1: Khởi tạo dữ liệu thô (Giai đoạn 1)
```bash
python src/data_generator.py
```
*Kết quả:* Tạo file `data/raw/book_sales_raw.csv` gồm 6,660 dòng, bao quát 10 thể loại trong 24 tháng, có chứa các lỗi thực tế (trùng lặp, khuyết thiếu, định dạng sai).

### Bước 2: Làm sạch và chuẩn hóa dữ liệu (Giai đoạn 2)
```bash
python src/data_cleaner.py
```
*Kết quả:* Làm sạch 100% missing values, loại bỏ 117 dòng trùng lặp, lọc 15 ngoại lai phi lý, tạo 8 đặc trưng mới và xuất ra `data/processed/book_sales_clean.csv` và `data/processed/book_sales_clean.xlsx`.

### Bước 3: Tạo hệ thống biểu đồ PNG (Giai đoạn 3)
```bash
python src/visualizer.py
```
*Kết quả:* Xuất 8 biểu đồ định dạng PNG chất lượng cao vào thư mục `charts/`.

### Bước 4: Tạo Dashboard HTML tương tác
```bash
python src/dashboard_builder.py
```
*Kết quả:* Xuất file `charts/dashboard.html`. Bạn chỉ cần click đúp vào file này để mở trên trình duyệt (Edge, Chrome) và trải nghiệm giao diện tương tác với đầy đủ thẻ KPI, bộ lọc hover và phóng to thu nhỏ.

---

## 4. HƯỚNG DẪN MỞ VÀ CHẠY JUPYTER NOTEBOOK

Để xem và chạy toàn bộ quy trình trong môi trường Notebook tương tác:

```bash
jupyter notebook notebooks/book_sales_analysis.ipynb
```
Hoặc mở trực tiếp file `notebooks/book_sales_analysis.ipynb` bằng VS Code / Google Colab / JupyterLab. Notebook đã được chạy sẵn và lưu đầy đủ toàn bộ kết quả phân tích, đồ thị và bảng số liệu.

---

## 5. TÓM TẮT KẾT QUẢ ĐỐI SOÁT DỮ LIỆU (BEFORE & AFTER)

| Chỉ số | Dữ liệu thô ban đầu | Dữ liệu sạch sau xử lý | Thay đổi |
| :--- | :---: | :---: | :--- |
| **Số dòng** | 6,660 dòng | **6,501 dòng** | Loại 117 dòng trùng, 15 ngoại lai, 27 trùng sau chuẩn hóa |
| **Số cột** | 14 cột | **22 cột** | Bổ sung 8 cột đặc trưng kinh doanh mới |
| **Số dòng trùng lặp** | 117 dòng | **0 dòng** | Khử sạch 100% bản ghi trùng lặp |
| **Số ô khuyết thiếu** | 370 ô | **0 ô** | Khử sạch 100% missing values bằng Median/Mean hợp lý |
| **Định dạng số & chuỗi** | Lỗi VNĐ, âm, chuỗi text lệch | Chuẩn hóa toàn diện | Ép kiểu số nguyên VNĐ, chuẩn Title Case |

---

## 6. BA INSIGHT KINH DOANH NỔI BẬT NHẤT

1. **Thương mại điện tử & Kênh xã hội chiếm thế thượng phong (59.9% Doanh số):** Shopee Mall (2.06 tỷ VNĐ, 36.0%) và TikTok Shop (1.37 tỷ VNĐ, 23.9%) là hai kênh bán chủ lực của toàn hệ thống, vượt trội hoàn toàn so với chuỗi Cửa hàng Offline truyền thống (12.4%).
2. **"Điểm ngọt" định giá và Đòn bẩy khuyến mãi:** Phân khúc sách giá trung bình từ 80,000 đến 200,000 VNĐ đóng góp tới 60.6% doanh thu. Các mức chiết khấu hiển thị từ 20% - 30% tạo ra điểm bùng nổ sức mua mạnh nhất (lượng bán tăng gấp 2.1 lần so với giảm giá nhẹ).
3. **Hiệu ứng mùa vụ tập trung cao độ:** Doanh thu Quý 4 bùng nổ mạnh mẽ (đặc biệt là đợt Mega Sale Tháng 11 và 12 đạt đỉnh trên 338 triệu VNĐ/tháng, tăng 82.7% so với tháng đáy), cùng điểm rơi phụ vào mùa Tựu trường Tháng 8 - 9.
