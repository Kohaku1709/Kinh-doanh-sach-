# Thay đổi so với commit gốc

Mốc gốc: `6bfe691904b4d721ee1a1743509f6b581b70ce81`, repository Kohaku1709/Kinh-doanh-sach-.

- Giữ đề tài kinh doanh sách và bảy nhóm câu hỏi EDA; thiết kế lại dữ liệu để có giá trị chuẩn kiểm chứng và nguồn gốc rõ.
- Thay ghép tên sách/tác giả/NXB thật ngẫu nhiên bằng danh tính giả lập, tránh kết luận sai về đơn vị thật.
- Giảm catalog từ 1.200 xuống 300 mã để cân đối số quan sát mỗi sách; giữ 6.500 dòng chuẩn và 24 tháng. Đây là bộ dữ liệu mới, không sửa số cũ để ép kết quả.
- Bổ sung mã đơn/dòng, raw_row_id, danh mục tham chiếu, dữ liệu chuẩn, nhãn lỗi, nhật ký ô và trạng thái dòng, dữ liệu cách ly.
- Dùng chung logic làm sạch, phân nhóm và tổng hợp trong notebook/pipeline; thêm kiểm tra biên, khóa, tổng và phục hồi.
- Phân biệt giá trị bán hàng với lợi nhuận; bỏ số thị phần, chuyển đổi giỏ hàng, ngân sách và lợi nhuận không được đo.
- Thêm 3 kịch bản × 50 seed, MCSE và kiểm tra thiếu điểm; không diễn giải phân vị mô phỏng thành khoảng tin cậy thị trường.
- Viết lại báo cáo có nguồn phương pháp; xuất Markdown, HTML và PDF từ cùng nội dung.
- Dashboard có lọc thật, KPI động, nhúng Plotly và CSS để mở ngoại tuyến.
- Bỏ XLSX cũ khỏi bản mới; CSV là dữ liệu chuẩn. Bản gốc được giữ riêng, không bị sửa trong quá trình bàn giao.

Đây là thay đổi lớn về phương pháp, cần đọc báo cáo mới toàn bộ. Không giữ các kết luận của báo cáo cũ rồi thay biểu đồ vào.
