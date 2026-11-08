from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENRES = ['Kỹ năng sống', 'Văn học', 'Kinh tế - Quản trị', 'Thiếu nhi', 'Tâm lý học', 'Khoa học công nghệ', 'Giáo dục - Ngoại ngữ', 'Lịch sử - Triết học', 'Truyện tranh', 'Nuôi dạy con']
CHANNELS = ['Sàn A', 'Sàn B', 'Sàn C', 'Cửa hàng', 'Website']
PARAMS = {
    'seed': 42, 'n_lines': 6500, 'n_books': 300,
    'start': '2024-01-01', 'end': '2025-12-31',
    'genre_weights': [.20,.18,.15,.13,.09,.06,.07,.04,.05,.03],
    'channel_weights': [.35,.22,.18,.15,.10],
    'discount_strength': 1.0, 'seasonality': True,
    'missing_rate': .02, 'catalog_coverage': 1.0,
    'max_qty_review': 1000, 'replications': 50,
}
PRICE_LABELS = ['Dưới 80.000', '80.000–200.000', 'Trên 200.000']
RATING_LABELS = ['Dưới 3,0', '3,0–<4,0', '4,0–<4,5', 'Từ 4,5']
CAT_FIELDS = ['ten_sach','the_loai','tac_gia','nha_xuat_ban','nam_xuat_ban','gia_goc','diem_danh_gia']
