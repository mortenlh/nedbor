from os import listdir
from os.path import isfile, join
from string import Template
import pandas as pd
import numpy as np
import math

def getNedborFiles(path):
    out = []    
    dirlist = listdir(path)
    for item in dirlist:
        if isfile(join(path,item)) and item.endswith('.csv') and item.startswith('n'):            
            out.append(item) 
    out.sort()                       
    return out            

def nedborToDataframe(path, **params):
    csvfiles = getNedborFiles(path)    
    index = []
    column = []
    if "lang" in params and params["lang"]=="da":
        rows = []
        for i,e in enumerate(csvfiles):
            rows.append(['','','','','','','','','','','','',''])
    else:    
        rows = np.zeros((len(csvfiles), 13))       
    for i,file in enumerate(csvfiles):
        f = path + file
        ftext = str(file)[1:-4]
        index.append(ftext)
        fdata = pd.read_csv(f, delimiter=';', header=None)
        fvalues = fdata[1].to_numpy()  
        sum = 0.0;              
        for j,fv in enumerate(fvalues):        
            if len(column)==0:                
                column = fdata[0].to_list()                    
                column.append('Total')                                    
            if "lang" in params and params["lang"]=="da":            
                rows[i][j] = str(float(fv)).replace(".", ",")
            else:    
                rows[i,j] = float(fv)  
            sum += 0.0 if math.isnan(float(fv)) else float(fv)
        if "lang" in params and params["lang"]=="da":            
            rows[i][12] = str(round(sum,1)).replace(".", ",")
        else:    
            rows[i,12] = round(sum,1)
    df = pd.DataFrame(rows,index=index,columns=column)        
    return df 

def nedborDataframe(path):
    csvfiles = getNedborFiles(path)
    columns = []
    index = []
    data = []    
    for i,file in enumerate(csvfiles):
        f = path + file
        ftext = str(file)[1:-4]
        tmp = pd.read_csv(f,sep=';', header=None)
        if len(columns)==0:
            columns = tmp.iloc[0:12, 0]
        index.append(ftext)
        data.append(tmp[1].to_numpy())
    dataframe = pd.DataFrame(data,index=index,columns=columns)
    return dataframe    
            
            

def saveDataFrame(path,dataframe,lang="None"):
    if lang=="da":
        file = path + 'alldata_da.csv'
    else:
        file = path + 'alldata.csv'    
    data = dataframe.to_csv(sep=';',index_label='periode')        
    fhandle = open(file,'w',newline='')
    fhandle.write(data)
    fhandle.close()

def saveDataFrameHtml(path,dataframe):
    file = path + 'alldata.html'
    data = dataframe.to_html(border=0)            
    fhandle = open(file,'w',newline='')
    fhandle.write(data)
    fhandle.close()    
    
def saveAllNedborData(path, **params):
    language = params["lang"] if "lang" in params else "None"
    df = nedborToDataframe(path,lang=language)
    type = params["type"] if "type" in params else "csv"
    if type=="html":
        saveDataFrameHtml(path, df)
    else:                         
        saveDataFrame(path, df, language) 
    
def makeHtml(path, dataframe, flip=False):
    if not flip:
        monthcolumns = dataframe.columns[:-1] #All columns minus the last column
        totalcolumn = dataframe.columns[-1:] #Last column
        tablehtml = dataframe.style.format(precision=1, decimal=",")\
            .set_table_attributes('class="table table-bordered"')\
            .map(lambda v: 'color:blue;font-weight:bold;background-color:lightblue;' if v>=100.0 else None,subset=monthcolumns)\
            .map(lambda v: 'color:black;font-weight:normal;background-color:#eceff1;',subset=totalcolumn)\
            .highlight_max(axis=0, props='color:lightblue;background-color:darkblue;font-weight:bold;')\
            .highlight_min(axis=0, props='color:#B87333;font-weight:bold;background-color:yellow;')\
            .to_html()
    else:
        columns = dataframe.columns[:]
        monthindexes = dataframe.index[:-1]
        lastindex = dataframe.index[-1:]
        tablehtml = dataframe.style.format(precision=1, decimal=",")\
            .set_table_attributes('class="table table-bordered"')\
            .map(lambda v: 'color:blue;font-weight:bold;background-color:lightblue;' if v>=100.0 else None,subset=(monthindexes, columns))\
            .map(lambda v: 'color:black;font-weight:normal;background-color:#eceff1;',subset=(lastindex, columns))\
            .highlight_max(axis=1, props='color:lightblue;background-color:darkblue;font-weight:bold;')\
            .highlight_min(axis=1, props='color:#B87333;font-weight:bold;background-color:yellow;')\
            .to_html()
    
    s = '''<!DOCTYPE html>
    <html>
        <head>
            <title>$title</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">            
            <style>
                .table td {
                    text-align:right;
                }
                
                .table thead th {
                    color:white;
                    background-color:#37474f;
                }
                
                .table tbody th {
                    color:white;
                    background-color:#37474f;
                }
            </style>
        </head>
        <body>
            <div class="container pt-3">
                <div class="row">
                    <div class="col">
                        <h1>$title</h1>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
    '''
    html = Template(s).substitute(title="Nedbør")        
    html += tablehtml
    html += '''
                    </div>
                </div>
            </div>
        </body>
    </html>        
    '''
    file = path + 'nedbor.html'
    fhandle = open(file,'w',newline='',encoding='utf-8')
    fhandle.write(html)
    fhandle.close()