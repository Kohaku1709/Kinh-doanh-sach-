# Quy trình nghiên cứu và điều kiện nghiệm thu

## 1. Xác định phạm vi

Đơn vị quan sát: dòng đơn một đầu sách; mỗi đơn một dòng. Tổng thể đích của nghiên cứu hiện tại chính là các kịch bản mô phỏng, không phải toàn thị trường. Quy mô vừa đủ để có nhiều nhóm, 24 tháng, các lỗi phân bố và các trường hợp biên; số dòng lớn hơn không tự tạo ý nghĩa học thuật.

Áp dụng cấu trúc ADEMP ở mức nhập môn: mục tiêu → cơ chế dữ liệu → đại lượng cần tính → phương pháp → đánh giá. Không thêm mô hình dự báo chỉ để tăng số thuật toán. Bảy câu hỏi kinh doanh và hai câu hỏi kiểm chứng được mô tả trong báo cáo.

## 2. Thiết kế trước khi đọc kết quả

`src/config.py` là cấu hình. Giữ seed cơ sở 42; 50 seed thí nghiệm 100–149; 3 kịch bản. Kịch bản thay đổi β hoặc mùa vụ có cùng danh mục/ngày/kênh/giảm giá theo seed; RNG lượng và bước cài lỗi tái lập. Dòng mua nhiều có RNG riêng để không đổi theo số lần gọi Poisson.

Không hiệu chỉnh tham số sau khi xem kết quả để làm kết luận “đẹp”. Khi đổi giả định phải ghi lại phiên bản và tái xuất kết quả. Mọi giá, trọng số, hệ số và ngưỡng kiểm tra là giả định tự đặt; chưa có dữ liệu thị trường dùng hiệu chỉnh.

Bộ bàn giao là một thiết kế nghiên cứu cố định, không phải công cụ tùy biến mọi giả định bằng giao diện. `--replications` có thể đổi trực tiếp; nếu sửa số sách, số dòng, seed hoặc cơ chế lỗi trong mã/cấu hình, phải sửa cả thiết kế thí nghiệm, diễn giải và các con số mô tả quy mô trong nguồn báo cáo/README. Không coi việc chạy thành công với cấu hình khác là báo cáo đã tự phù hợp với nghiên cứu mới.

## 3. Xây dựng và phân tách dữ liệu

1. Sinh catalog giả lập và truth sạch.
2. Cài thiếu ở 4 trường, định dạng thể loại/tiền, giá âm, số lượng sai, bản sao đúng và bản sao mâu thuẫn.
3. Lưu raw_row_id cho mỗi dòng nguồn; giữ ma_dong để truy xuất bản ghi nghiệp vụ.
4. Lưu nhãn lỗi riêng. Hàm làm sạch chỉ nhận raw và catalog.

Đây là tách dữ liệu phục vụ kiểm chứng, không phải chia train/test cho mô hình dự đoán.

## 4. Làm sạch có dấu vết

Chuẩn hóa kiểu và chuỗi → phục hồi từ thông tin nghiệp vụ có căn cứ → gộp bản sao cùng khóa và nội dung → cách ly xung đột/miền không hợp lệ → gắn cờ IQR → tạo đặc trưng dùng chung.

Ngưỡng >1.000 cuốn chỉ để cần rà soát trong kịch bản, không chứng minh đơn lớn là giả. Dữ liệu cách ly vẫn nằm trong `quarantine.csv`. Không xóa cứng outlier IQR, không điền điểm sách bằng trung bình trong pipeline chính. Nếu catalog không có thông tin, để thiếu có nhãn.

## 5. Đánh giá

- Khớp từng trường trên tập giữ lại, so bằng ma_dong.
- Tỷ lệ giữ = số mã sạch / số mã truth.
- Sai lệch tổng tương đối = (T sạch / T truth − 1) × 100%.
- Sai lệch trên tập mã giữ lại để tách lỗi giá trị khỏi thiếu bản ghi.
- Precision cách ly = số mã cần cách ly và đã cách ly / số mã bị cách ly.
- Recall cách ly = số mã cần cách ly và đã cách ly / số mã cần cách ly theo nhãn lỗi.
- Đối soát từng raw_row_id có đúng một trạng thái cuối.

Kết quả khớp hoàn hảo trong thí nghiệm không có nghĩa phương pháp tổng quát hoàn hảo: cơ chế lỗi được biết trước, chủ yếu dễ sửa và catalog được giả định đáng tin.

## 6. EDA và diễn giải

Kiểm tra phân phối và quy mô trước các bảng xếp hạng. Công bố mẫu số của tỷ lệ; dùng một bảng tổng hợp trung tâm. Tổng theo thể loại, kênh, tháng, phân khúc và mã sách đều phải khớp tổng toàn bộ. Phân biệt cấp dòng với cấp sách, mức giảm giá niêm yết với thực tế, tổng giá trị với lợi nhuận.

Tương quan là mô tả, không nhân quả. Doanh thu định nghĩa bởi giá × lượng; giá và giảm giá liên hệ theo công thức. Không diễn giải các quan hệ này như phát hiện độc lập. Các nhận xét về khách hàng, thị phần, hoàn hàng hoặc lợi nhuận phải có dữ liệu đo được trước khi thêm.

## 7. Độ nhạy

Lặp 50 lần mỗi kịch bản. Lưu từng lượt, trung bình, SD, MCSE và phân vị thực nghiệm; không gọi phân vị mô phỏng là khoảng tin cậy thị trường. So sánh cả có/không dòng mua nhiều cho tương quan. Thí nghiệm thiếu điểm 2%, 10%, 25% chỉ một seed và MCAR được cài, nên báo rõ là chẩn đoán hạn chế.

## 8. Kiểm tra và phát hành

Chạy tests → pipeline → notebook kernel mới → đối chiếu bảng/biểu đồ → kiểm tra dashboard ngoại tuyến và bộ lọc → render PDF, xem từng trang → kiểm tra link và manifest. Lưu phiên bản môi trường. Chỉ đánh dấu hoàn thành điều đã thực hiện; phần nhóm cần cung cấp ghi riêng, không suy đoán tên giảng viên hay kết quả xác nhận.
