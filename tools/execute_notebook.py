import os,sys,json,tempfile
import asyncio
from pathlib import Path
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
if sys.platform=='win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
path=ROOT/'notebooks/book_sales_analysis.ipynb'
with tempfile.TemporaryDirectory(prefix='book-sales-kernel-') as tmp:
    spec=Path(tmp)/'kernels'/'book-sales';spec.mkdir(parents=True)
    (spec/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Book sales validation','language':'python'}),encoding='utf8')
    os.environ['JUPYTER_PATH']=tmp+os.pathsep+os.environ.get('JUPYTER_PATH','')
    nb=nbformat.read(path,as_version=4)
    NotebookClient(nb,timeout=300,kernel_name='book-sales',resources={'metadata':{'path':str(ROOT)}}).execute()
    nb.metadata['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}
    nbformat.write(nb,path)
    print('Notebook executed:',len([c for c in nb.cells if c.cell_type=='code']),'code cells, no execution errors.')
