# TỪ ĐIỂN DỮ LIỆU KINH DOANH SÁCH (DATA DICTIONARY)

Bộ dữ liệu ghi nhận thông tin bán sách tại thị trường Việt Nam (giai đoạn 2024 - 2025), gồm dữ liệu giao dịch bán lẻ đa kênh với các thuộc tính sách, tài chính, phân loại và phản hồi của người tiêu dùng.

---

## 1. Dữ liệu thô ban đầu (`data/raw/book_sales_raw.csv`)

| Tên cột | Kiểu dữ liệu gốc | Ý nghĩa | Ví dụ / Giá trị hợp lệ | Ghi chú & Lỗi thực tế |
| :--- | :--- | :--- | :--- | :--- |
| `ma_sach` | String | Mã định danh duy nhất của đầu sách | `BK00001`, `BK00845` | Định dạng tiền tố `BK` + 5 chữ số |
| `ten_sach` | String | Tên tựa sách xuất bản | `Thay Đổi Tí Hon Hiệu Quả Bất Ngờ`, `Mắt Biếc` | Tựa sách phổ biến trên thị trường |
| `tac_gia` | String | Tên tác giả hoặc dịch giả chính | `James Clear`, `Nguyễn Nhật Ánh` | Có khoảng 45 dòng bị thiếu (`NaN`) |
| `the_loai` | String | Thể loại sách theo danh mục bán lẻ | `Kỹ năng sống`, `Văn học`, `Kinh tế - Quản trị`... | 10 thể loại; tồn tại lỗi chữ hoa, thường và khoảng trắng |
| `nha_xuat_ban` | String | Đơn vị xuất bản phát hành | `NXB Trẻ`, `NXB Kim Đồng`, `NXB Hội Nhà Văn`... | 8 nhà xuất bản lớn; có lỗi khoảng trắng và thiếu giá trị |
| `nam_xuat_ban` | Float/Int | Năm phát hành ấn bản sách | `2015` - `2024` | Chứa ~85 giá trị thiếu (`NaN`) |
| `gia_goc` | Integer | Giá bìa niêm yết của sách (VNĐ) | `85000`, `150000`, `280000` | Dao động từ 45.000 đến 350.000 VNĐ |
| `gia_ban` | Object (String/Num) | Giá bán thực tế tới khách hàng | `72000`, `"120,000 VNĐ"`, `-50000`, `0` | Có lỗi chuỗi ký tự, giá trị âm và giá bằng 0 |
| `phan_tram_giam_gia` | Float | Tỷ lệ giảm giá so với giá gốc (%) | `0.0`, `15.0`, `35.0` | Phạm vi hợp lý: 0% - 50% |
| `so_luong_da_ban` | Integer | Số cuốn bán ra trong giao dịch | `1`, `5`, `12`, `99999`, `-10` | Có lỗi giá trị âm và ngoại lai nhập liệu |
| `diem_danh_gia` | Float | Điểm đánh giá trung bình (thang 5) | `4.6`, `4.8`, `3.9`, `NaN` | ~110 dòng bị thiếu giá trị |
| `so_luot_danh_gia` | Integer | Tổng số lượt khách hàng nhận xét | `18`, `154`, `1280` | Phân phối theo độ thịnh hành của sách |
| `ngay_ban` | String | Ngày phát sinh giao dịch bán hàng | `2024-05-18`, `2025-11-11` | Định dạng chuẩn `YYYY-MM-DD` |
| `kenh_ban` | String | Kênh phân phối phát sinh đơn hàng | `Shopee Mall`, `TikTok Shop`, `Tiki Trading`, `Cửa hàng Offline`, `Website Nhà sách` | 5 kênh bán lẻ chính |

---

## 2. Dữ liệu sau xử lý & làm giàu đặc trưng (`data/processed/book_sales_clean.csv` / `.xlsx`)

Sau quy trình làm sạch (loại bỏ trùng lặp, xử lý missing values, sửa định dạng số, chuẩn hóa chuỗi, xử lý ngoại lai IQR) và tạo đặc trưng (Feature Engineering):

| Tên cột | Kiểu dữ liệu chuẩn | Ý nghĩa | Công thức / Quy tắc tính | Ví dụ |
| :--- | :--- | :--- | :--- | :--- |
| `ma_sach` | `category` / `str` | Mã định danh đầu sách | Giữ nguyên | `BK00123` |
| `ten_sach` | `str` | Tên tựa sách | Chuẩn hóa khoảng trắng | `Đắc Nhân Tâm` |
| `tac_gia` | `str` | Tên tác giả | Điền khuyết tật `"Không rõ tác giả"` | `Dale Carnegie` |
| `the_loai` | `category` | Thể loại sách chuẩn hóa | Title case, xóa khoảng trắng thừa | `Kỹ Năng Sống` |
| `nha_xuat_ban` | `category` | Nhà xuất bản chuẩn hóa | Title case, điền khuyết tật `"NXB Khác"` | `NXB Trẻ` |
| `nam_xuat_ban` | `int64` | Năm xuất bản | Điền khuyết tật bằng trung vị (`median`) | `2020` |
| `gia_goc` | `int64` | Giá niêm yết (VNĐ) | Giữ nguyên | `120000` |
| `gia_ban` | `int64` | Giá bán thực tế (VNĐ) | Ép kiểu số, tính lại nếu bị âm/0: `gia_goc * (1 - giam_gia)` | `96000` |
| `phan_tram_giam_gia`| `float64` | Phần trăm giảm giá (%) | Chuẩn hóa: `round((1 - gia_ban/gia_goc)*100, 1)` | `20.0` |
| `so_luong_da_ban` | `int64` | Số lượng bán hợp lệ | Lọc bỏ ngoại lai phi lý (< 1 hoặc > ngưỡng IQR 99.5%) | `4` |
| `doanh_thu` | `int64` | Tổng doanh thu đơn hàng (VNĐ) | `gia_ban * so_luong_da_ban` | `384000` |
| `diem_danh_gia` | `float64` | Điểm đánh giá (1.0 - 5.0) | Điền trung bình thể loại (`genre mean`) | `4.5` |
| `so_luot_danh_gia` | `int64` | Lượt đánh giá | Giữ nguyên kiểu nguyên | `45` |
| `ngay_ban` | `datetime64[ns]`| Ngày ghi nhận đơn | Ép kiểu chuẩn datetime | `2024-11-11` |
| `thang_ban` | `int32` | Tháng bán hàng (1 - 12) | Trích xuất từ `ngay_ban` | `11` |
| `quy_ban` | `str` | Quý bán hàng trong năm | `Q1`, `Q2`, `Q3`, `Q4` | `Q4` |
| `nam_ban` | `int32` | Năm phát sinh đơn | `2024`, `2025` | `2024` |
| `thang_nam` | `str` | Chu kỳ Tháng - Năm | `YYYY-MM` | `2024-11` |
| `thu_trong_tuan` | `str` | Thứ trong tuần | `Thứ Hai` đến `Chủ Nhật` | `Thứ Sáu` |
| `kenh_ban` | `category` | Kênh phân phối | Chuẩn hóa danh mục | `Shopee Mall` |
| `phan_khuc_gia` | `category` | Phân khúc giá trị sách | `< 80k: Giá rẻ`<br>`80k - 200k: Trung bình`<br>`> 200k: Cao cấp` | `Trung bình` |
| `nhom_danh_gia` | `category` | Phân loại chất lượng đánh giá | `>= 4.5: Xuất sắc`<br>`4.0 - < 4.5: Tốt`<br>`3.0 - < 4.0: Trung bình`<br>`< 3.0: Thấp` | `Xuất sắc` |
