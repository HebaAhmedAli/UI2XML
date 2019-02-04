import nbformat
from nbformat.v4 import new_notebook, new_code_cell

nb = new_notebook()
files = ['Constants','LoadData','Preprocessing','Utils','testModel','Model/CNN','Model/EncoderDecoderRNN','Model/Model']
for file in files:
    nb = new_notebook()
    with open(file+'.py') as f:
        code = f.read()
    nb.cells.append(new_code_cell(code))
    nbformat.write(nb, file+'.ipynb')
