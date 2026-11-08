import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
import numpy as np
import pytest
from src.data_generator import generate,corrupt
from src.data_cleaner import clean,price_group,rating_group,parse_price
from src.config import PRICE_LABELS,RATING_LABELS,CAT_FIELDS
from src.analysis import evaluate,summarize

@pytest.fixture(scope='module')
def bundle():
    cat,t=generate();r,e=corrupt(t);d,s,q,c,l=clean(r,cat)
    return cat,t,r,e,d,s,q,c,l

def test_boundaries():
    assert price_group(pd.Series([79999,80000,200000,200001])).tolist()==[PRICE_LABELS[0],PRICE_LABELS[1],PRICE_LABELS[1],PRICE_LABELS[2]]
    assert rating_group(pd.Series([2.9,3.,4.,4.5,5.,np.nan])).tolist()==RATING_LABELS+[RATING_LABELS[-1],'Chưa biết']

@pytest.mark.parametrize('value,expected',[('120,000 VNĐ',120000),('120.000 VND',120000),('120000',120000),('-50000',-50000)])
def test_price_formats(value,expected):assert parse_price(value)==expected

def test_known_truth_recovery(bundle):
    cat,t,r,e,d,s,q,c,l=bundle
    matches,v=evaluate(t,d,r,e)
    assert matches.ty_le_khop.eq(1).all()
    assert v['retained_revenue_error']==0
    assert v['quarantine_precision']==v['quarantine_recall']==1
    assert len(d)==len(t)-20
    assert not d.ma_dong.duplicated().any()

def test_no_unaccounted_rows(bundle):
    cat,t,r,e,d,s,q,c,l=bundle
    assert len(l)==len(r)==l.raw_row_id.nunique()
    assert set(l.raw_row_id)==set(r.raw_row_id)
    assert len(d)+len(q)+l.trang_thai.eq('duplicate_collapsed').sum()==len(r)

def test_valid_bulk_sales_retained(bundle):
    _,t,_,e,d,*_=bundle
    invalid=set(e.loc[e.loai_loi.isin(['invalid_qty','duplicate_conflict']),'ma_dong'])
    good=t.loc[(t.so_luong>150)&~t.ma_dong.isin(invalid),'ma_dong']
    assert len(good)>0
    assert set(good).issubset(set(d.ma_dong))

def test_catalog_missing_does_not_invent_values(bundle):
    cat,t,r,e,*_=bundle
    empty=cat.iloc[:0]
    d,*_=clean(r,empty)
    assert d.diem_danh_gia.isna().any()
    assert d.tac_gia.eq('Không rõ tác giả').any()

def test_conflict_quarantines_both_variants(bundle):
    cat,t,*_=bundle
    r=t.iloc[:2].copy();r['raw_row_id']=['R1','R2']
    other=r.iloc[[0]].copy();other['raw_row_id']='R3';other['so_luong']+=1
    d,_,q,_,_=clean(pd.concat([r,other],ignore_index=True),cat)
    assert len(d)==1 and len(q)==2

@pytest.mark.parametrize('column,value',[('ngay_ban','not a date'),('gia_goc',0),('diem_danh_gia',6),('so_luong',2.5),('kenh_ban','unknown'),('nam_xuat_ban',2025)])
def test_invalid_inputs_are_quarantined(bundle,column,value):
    cat,t,*_=bundle
    r=t.iloc[:3].copy();r['raw_row_id']=['R1','R2','R3'];r[column]=r[column].astype(object);r.loc[r.index[0],column]=value
    d,_,q,_,_=clean(r,cat)
    assert 'R1' in q.raw_row_id.values

def test_determinism(bundle):
    cat,t,*_=bundle
    cat2,t2=generate()
    pd.testing.assert_frame_equal(cat,cat2);pd.testing.assert_frame_equal(t,t2)

def test_all_totals_reconcile(bundle):
    d=bundle[4];tables,m=summarize(d)
    for k in ['genre','channel','segment','month','year','publisher','author','books']:
        assert tables[k].doanh_thu.sum()==m['revenue']
        assert tables[k].so_luong.sum()==m['quantity']
    assert np.isclose(m['average_unit_price'],m['revenue']/m['quantity'])
