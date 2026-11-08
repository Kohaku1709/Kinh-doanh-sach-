from pathlib import Path
import nbformat as nbf

ROOT=Path(__file__).resolve().parents[1]
nb=nbf.v4.new_notebook()
cells=[]
def md(s):cells.append(nbf.v4.new_markdown_cell(s))
def code(s):cells.append(nbf.v4.new_code_cell(s))
md('''# Kinh doanh sách: nghiên cứu mô phỏng có kiểm chứng

**Dữ liệu mô phỏng hoàn toàn; không đại diện thị trường.** Notebook dùng cùng hàm với pipeline. Một dòng là một đơn một đầu sách giả lập. Mọi con số dưới đây được tính khi chạy; phần diễn giải và tài liệu tham khảo đầy đủ nằm trong `report/bao_cao.pdf` và `docs/QUY-TRINH.md`.

Mục tiêu: xây dựng dữ liệu, kiểm chứng làm sạch, trả lời bảy câu hỏi EDA và đánh giá độ nhạy. Không suy ra lợi nhuận, chuyển đổi hay tác động nhân quả. Chạy `python run.py` trước để tạo các dữ liệu và kết quả thí nghiệm.''')
code('''from pathlib import Path
import sys, json
import pandas as pd
from IPython.display import display, Image, Markdown
ROOT = Path.cwd() if (Path.cwd()/'src').exists() else Path.cwd().parent
sys.path.insert(0,str(ROOT))
from src.data_cleaner import clean
from src.analysis import summarize, evaluate
from src.visualizer import generate_all_charts
pd.set_option('display.max_columns',12)
pd.set_option('display.float_format',lambda x:f'{x:,.3f}')
raw=pd.read_csv(ROOT/'data/raw/book_sales_raw.csv')
catalog=pd.read_csv(ROOT/'data/reference/catalog.csv')
print('Dòng/cột raw:',raw.shape,'; số mã sách trong catalog:',len(catalog))
display(raw.head())''')
md('''## 1. Khảo sát dữ liệu thô

Đếm riêng bản sao cùng mã và ô thiếu. Số mã lặp không tự quyết định số dòng bị xóa: cần xem nội dung có giống nhau sau chuẩn hóa hay không.''')
code('''display(pd.DataFrame({'dtype':raw.dtypes.astype(str),'missing':raw.isna().sum()}))
print('Mã dòng lặp:',raw.ma_dong.duplicated().sum())''')
md('''## 2. Làm sạch dùng chung quy tắc

Hàm chỉ nhận raw và catalog, không nhận truth hoặc nhãn lỗi. Quy trình: chuẩn hóa → phục hồi có căn cứ → gộp bản sao giống nhau → cách ly xung đột → gắn cờ IQR → tạo đặc trưng. Chi tiết và lý do từng bước ở `docs/QUY-TRINH.md`.''')
code('''df,stages,quarantine,changes,lineage=clean(raw,catalog)
display(stages)
display(quarantine.groupby('ly_do').size().rename('so_dong'))
assert len(lineage)==len(raw)==lineage.raw_row_id.nunique()
assert not df.ma_dong.duplicated().any()
display(changes.head(10))''')
md('''## 3. Đối soát kết quả và phục hồi

Chỉ từ bước đánh giá mới đọc dữ liệu chuẩn. So sánh theo mã dòng; kiểm tra cả tính đúng của dòng giữ lại và chênh lệch tổng kỳ do cách ly.''')
code('''stored=pd.read_csv(ROOT/'data/processed/book_sales_clean.csv')
pd.testing.assert_frame_equal(df.astype('string').reset_index(drop=True),stored.astype('string').reset_index(drop=True))
truth=pd.read_csv(ROOT/'data/reference/ground_truth.csv')
errors=pd.read_csv(ROOT/'data/audit/injected_errors.csv')
recovery,validation=evaluate(truth,df,raw,errors)
display(recovery)
display(pd.Series(validation,name='gia_tri'))
tables,metrics=summarize(df)
published=json.loads((ROOT/'results/metrics.json').read_text(encoding='utf8'))
assert metrics==published['metrics']
display(pd.Series(metrics,name='gia_tri'))''')
md('''## 4. EDA cơ bản và các bảng kết quả

Các biến phụ thuộc theo định nghĩa: giá trị bán hàng = giá × lượng; giảm giá thực tế từ giá bán/giá gốc. Pearson chỉ mô tả tương quan, không là bằng chứng nhân quả.''')
code("display(tables['describe'])\ndisplay(tables['discount'])")
md('''## 5. Bảy câu hỏi kinh doanh trong kịch bản

Tất cả đồ thị được tạo lại từ chính `df` vừa làm sạch. Kết quả độ nhạy đã tính bởi pipeline được đọc từ CSV; notebook không âm thầm chạy lại 150 mô phỏng.''')
code("exp=pd.read_csv(ROOT/'results/sensitivity_runs.csv')\ngenerate_all_charts(df,tables,exp,ROOT/'charts')")
for title,key,chart,interpretation in [
('Thể loại','genre','01_genre.png','So sánh giá trị và số cuốn trên hai trục riêng. Thứ hạng chịu ảnh hưởng trọng số thể loại đã đặt, không là thị phần thị trường.'),
('Mã sách','books','02_books.png','Xếp theo mã sách, không theo tên hoặc tác giả thiếu. Đọc kèm số dòng và số cuốn để nhận biết ảnh hưởng mua số lượng lớn.'),
('Theo tháng','month','03_month.png','Hệ số mùa vụ đã được cài. Tăng trưởng giữa hai năm có thể do ngẫu nhiên; không gọi là tăng trưởng thị trường.'),
('Giá và giảm giá','discount','04_discount.png','Nhóm dùng mức giảm niêm yết; tương quan dùng mức thực tế. Giá và giảm giá đã có trong công thức sinh lượng.'),
('Điểm và lượng theo sách','books','05_rating.png','Điểm giả lập được cố định trước kỳ bán. Tổng hợp lên cấp sách để tránh đánh đồng dòng giao dịch với một sách độc lập.'),
('Tương quan','correlation','06_correlation.png','Biến được tính từ nhau có tương quan theo định nghĩa. Không suy ra tối ưu doanh thu hoặc nhân quả từ ma trận.'),
('Kênh và phân khúc','channel','07_composition.png','Tỷ trọng có mẫu số toàn bộ tập sạch; không có số thị phần thực. Dashboard thay mẫu số khi lọc.')]:
    md('### '+title+'\n\n'+interpretation)
    code(f"display(tables['{key}'].head(24))\ndisplay(Image(filename=str(ROOT/'charts/{chart}')))")
md('''## 6. Độ nhạy và sai số Monte Carlo

50 seed/kịch bản, 3 kịch bản. Phân vị giữa các lượt mô phỏng không phải khoảng tin cậy thị trường. MCSE đánh giá độ chính xác trung bình mô phỏng có điều kiện trên mô hình. Kịch bản bỏ hệ số giảm giá vẫn giữ đường ảnh hưởng qua giá bán.''')
code("display(pd.read_csv(ROOT/'results/sensitivity_summary.csv'))\ndisplay(Image(filename=str(ROOT/'charts/08_sensitivity.png')))")
md('''## 7. Kiểm tra điền thiếu

Thí nghiệm che điểm MCAR một seed, không dùng catalog. Giữ thiếu không có MAE phục hồi; điền trung bình tăng độ bao phủ nhưng không đảm bảo khôi phục điểm từng sách. Cần nhiều cơ chế/seed nếu muốn kết luận tổng quát.''')
code("display(pd.read_csv(ROOT/'results/missing_sensitivity.csv'))")
md('''## Kết luận và giới hạn

Notebook đã kiểm tra cùng dữ liệu sạch và số liệu KPI với pipeline. Các trường khớp trên tập giữ lại không đồng nghĩa tổng kỳ đầy đủ. Kết quả mô tả chỉ áp dụng cho mô phỏng. Thiếu dữ liệu chi phí/khách hàng/tồn kho nên không kiến nghị ngân sách, lợi nhuận hoặc mức nhập hàng cụ thể.

Tham khảo: [Morris et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/); [NIST Box Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/boxplot.htm); [pandas.cut](https://pandas.pydata.org/docs/reference/api/pandas.cut.html); [FAIR](https://www.gofair.foundation/fair-principles). Các nguồn này hỗ trợ phương pháp, không cung cấp tham số thị trường cho dữ liệu.''')
nb.cells=cells
nb.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}}
(ROOT/'notebooks').mkdir(exist_ok=True)
nbf.write(nb,ROOT/'notebooks/book_sales_analysis.ipynb')
