# Đối soát số liệu của bản gốc

Phạm vi: commit `6bfe691904b4d721ee1a1743509f6b581b70ce81`. Đây là đối soát dữ liệu cũ, **không phải kết quả bộ mô phỏng đã thiết kế lại**. Nguồn: `data/processed/book_sales_clean.csv` của commit gốc. Các kết luận kiểm tra được bằng groupby/corr; không suy đoán ý định của người viết.

| Chỉ tiêu | Bản cũ công bố | Tính lại trên CSV cũ |
|---|---:|---:|
| Tổng giá trị bán hàng | ~5,73 tỷ đồng | 5734827000 |
| Số mã sách xuất hiện | 1.200 (lẫn với quy mô catalog) | 1154 |
| Cuốn Kỹ năng sống | 11.850 | 13234 |
| r điểm–lượng | 0,12 | 0.009408 |
| r giảm giá–lượng | 0,35 | 0.529788 |
| r doanh thu–lượng | 0,76 | 0.523713 |
| Tháng cao nhất | 2025-11 / 338 triệu | 2025-12 / 391,833,000 đồng |
| Tháng thấp nhất | 2024-05 / 185 triệu | 2024-10 / 176,995,000 đồng |
| Tăng trưởng năm trên dashboard | 18,5% | 5.565564% |
| Tỷ lệ dòng có điểm ≥4 | Hơn 92% đơn tốt/xuất sắc | 75.988309% |

## Bằng chứng mã nguồn

- `report/bao_cao.md`: các đoạn 4.1, 4.3, 4.5, 4.6 và 5.1; số liệu và nhận xét không nhất quán với CSV/hình đã lưu.
- `src/dashboard_builder.py:204,224,236`: ghi cố định mức YoY, chiết khấu, tỷ lệ tốt/xuất sắc.
- `src/data_generator.py:75–79`: ghép tác giả/NXB ngẫu nhiên và thêm Tập vào tựa mẫu; không phải danh mục xuất bản đã xác thực.
- `src/data_cleaner.py:219–224`: tính IQR nhưng điều kiện loại là >150, không sử dụng biến upper_bound.
- Notebook ô làm sạch dùng `pd.cut` đóng phải; chương trình dùng các điều kiện biên khác. 62 dòng giá đúng 80.000 và 1.051 dòng có điểm đúng 3,0/4,0/4,5 có thể khác nhóm khi chạy hai cách.
- Xếp hạng NXB loại nhóm không rõ trước khi tính mẫu số. Thông tin lợi nhuận, chuyển đổi, bỏ giỏ và hiệu quả quảng cáo không có trong schema.

Nguồn nguyên bản: https://github.com/Kohaku1709/Kinh-doanh-sach-/tree/6bfe691904b4d721ee1a1743509f6b581b70ce81

Bản mới không giữ các số liệu cũ rồi sửa câu chữ: cơ chế dữ liệu đã thay đổi có tài liệu, tất cả kết quả mới được tính lại. Không có thao tác chỉnh sửa hoặc push vào GitHub gốc trong quá trình này.
