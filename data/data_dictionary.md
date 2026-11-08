# Từ điển dữ liệu và hợp đồng phân tích

Mọi dữ liệu đều giả lập. Một dòng nghiệp vụ là một đơn chứa một đầu sách, có thể nhiều cuốn. CSV dùng UTF-8 BOM; tiền là đồng, số lượng là cuốn. Không có thông tin cá nhân. Kiểu dưới đây là kiểu logic; CSV không lưu kiểu pandas/category.

## Các tệp

| Tệp | Vai trò / khóa |
|---|---|
| `reference/catalog.csv` | 300 sách giả lập; `ma_sach` duy nhất. Đầu vào có thể dùng để phục hồi thuộc tính sách. |
| `reference/ground_truth.csv` | 6.500 dòng trước khi cài lỗi; `ma_dong` duy nhất. Chỉ dùng đánh giá, không làm đầu vào làm sạch. |
| `raw/book_sales_raw.csv` | 6.660 dòng có lỗi và bản sao; `raw_row_id` duy nhất, `ma_dong` có thể lặp. |
| `processed/book_sales_clean.csv` | 6.480 dòng cơ sở sau xử lý; một mã dòng/một mã đơn trong kịch bản. |
| `audit/injected_errors.csv` | Cột mã dòng, cột bị lỗi, loại lỗi, giá trị chuẩn trước lỗi; chỉ dùng kiểm chứng. |
| `audit/cell_changes.csv` | `raw_row_id`, `ma_dong`, `cot`, `truoc`, `sau`. Có cả thay đổi biểu diễn kiểu số, không chỉ thay đổi giá trị nghiệp vụ. |
| `audit/row_lineage.csv` | Một trạng thái cuối cho mỗi raw_row_id: retained, duplicate_collapsed, conflicting_line_id, quantity_needs_review hoặc invalid_required_fields. |
| `audit/quarantine.csv` | Các biến thể chưa đủ tin cậy để đưa vào EDA, có cột `ly_do`; không xóa mất dấu. |
| `audit/cleaning_stages.csv` | Dòng, ô thiếu và mã lặp theo giai đoạn. Ô thiếu tính trên các trường nghiệp vụ gốc, không tính cờ/đặc trưng mới. |

## Trường đầu vào

| Trường | Kiểu logic / miền | Ý nghĩa và nguồn |
|---|---|---|
| `raw_row_id` | Chuỗi R + 6 số | Định danh dòng nguồn sau thêm bản sao; chỉ raw/clean/audit có. |
| `ma_dong` | Chuỗi L + 6 số | Định danh dòng nghiệp vụ; bản sao phải giữ nguyên mã. |
| `ma_don` | Chuỗi O + 6 số | Đơn một đầu sách theo giả định mô hình; chưa hỗ trợ giỏ nhiều đầu sách. |
| `ma_sach` | Chuỗi BK + 4 số | Mã sách giả lập, nối catalog nhiều-một. |
| `ten_sach` | Chuỗi | Sách mô phỏng 001…300; không mô tả xuất bản thật. |
| `the_loai` | Danh mục 10 giá trị | Thứ tự và xác suất trong config.py. |
| `tac_gia` | Chuỗi giả lập / không rõ | Nhãn danh mục, không là người thật; thiếu tra catalog, nếu không có thì giữ nhãn không rõ. |
| `nha_xuat_ban` | Chuỗi giả lập / không rõ | Không đại diện đơn vị xuất bản thực. |
| `nam_xuat_ban` | Số nguyên / thiếu | Cơ sở sinh 2015–2023; kiểm tra chấp nhận 1900–2023. |
| `gia_goc` | Số nguyên đồng, >0 | Giá bìa giả lập, sinh 45.000–350.000; nguồn catalog. |
| `gia_ban` | Số nguyên đồng, 0<giá≤giá gốc | Giá sau giảm làm tròn nghìn; raw có thể là chuỗi tiền hoặc giá sai. |
| `giam_gia_niem_yet` | Phần trăm [0,100) | Mức giảm giả lập trước làm tròn; đầu vào được giả định đáng tin khi sửa giá. |
| `so_luong` | Nguyên dương | Cuốn/dòng; >1.000 được cách ly để rà soát theo quy tắc kịch bản. |
| `diem_danh_gia` | Số [1,5] hoặc thiếu | Thuộc tính sách giả lập cố định trước kỳ bán, không là nhận xét trên từng đơn hay dữ liệu tương lai. |
| `ngay_ban` | YYYY-MM-DD | Nằm trong 2024-01-01 đến 2025-12-31. |
| `kenh_ban` | Sàn A/B/C, Cửa hàng, Website | Nhãn giả lập; chỉ trọng số chọn và tập mức giảm khác nhau. |

## Trường sau xử lý

| Trường | Định nghĩa |
|---|---|
| `doanh_thu` | `gia_ban × so_luong`. Tên kỹ thuật kế thừa; nghĩa dùng trong báo cáo: giá trị bán hàng sau giảm giá, chưa trừ hoàn/hủy, phí, thuế hay chi phí. Không gọi là lợi nhuận/doanh thu thuần. |
| `giam_gia_thuc_te` | `100 × (1 − gia_ban/gia_goc)`, làm tròn 3 chữ số thập phân; có thể khác mức niêm yết do làm tròn nghìn. |
| `phan_khuc_gia` | Giá <80.000; 80.000≤giá≤200.000; giá>200.000 đồng. |
| `nhom_danh_gia` | <3,0; [3,0;4,0); [4,0;4,5); ≥4,5; thiếu → Chưa biết. |
| `nhom_giam_gia` | Mức niêm yết: [0;5], (5;15], (15;25], (25;40]. Kịch bản chỉ sinh tối đa 40%. |
| `thang_nam`, `nam_ban`, `quy_ban` | Trích từ ngày; quý luôn kèm năm, ví dụ 2024Q1. |
| `co_ngoai_lai_iqr` | True khi lượng > Q3 + 1,5×IQR trên tập đã cách ly lỗi; chỉ gắn cờ. |
| `gia_ban_duoc_sua` | True khi giá thiếu/không dương được tính lại có căn cứ. |
| `khoi_phuc_*` | Bảy cờ cho từng thuộc tính catalog: tên, thể loại, tác giả, NXB, năm, giá gốc, điểm. True khi ô thiếu được điền bằng giá trị catalog có thật trong kịch bản. |

## Mẫu số và kết quả

- Tỷ trọng nhóm: giá trị nhóm / giá trị toàn tập sau bộ lọc. Giữ nhóm không rõ trong mẫu số.
- Giá bán bình quân theo cuốn: tổng giá trị / tổng cuốn, không phải trung bình không trọng số của dòng.
- Tương quan cấp dòng dùng các dòng sạch; tương quan cấp sách nhóm một lần theo ma_sach.
- `sensitivity_runs.csv`: 150 dòng, mỗi dòng một seed/kịch bản; `sensitivity_summary.csv`: R, mean, SD, MCSE, p025/p975. Các khoảng không là khoảng tin cậy thị trường.
- `missing_sensitivity.csv`: kiểm tra che điểm một seed. MAE rỗng ở phương án giữ thiếu nghĩa không áp dụng, không phải lỗi xuất tệp.
