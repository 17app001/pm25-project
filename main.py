from flask import Flask, render_template,request
from datetime import datetime
from pm25 import get_pm25
import ssl,json

app = Flask(__name__)

ssl._create_default_https_context = ssl._create_unverified_context


@app.route('/pm25-chart')
def draw_pm25():
    return render_template('./pm25-chart.html')

@app.route('/get-pm25-data',methods=['GET','POST'])
def get_pm25_json():
    columns, values, error = get_pm25()
    
    columns = ['city', 'stationName', 'resultTime', 'result']

    stationName=[ value[1] for value in values]
    result=[value[-1] for value in values]

    datas={'columns':columns,'stationName':stationName,'result':result}

    return json.dumps(datas,ensure_ascii=False)
     

     


@app.route('/pm25',methods=['GET','POST'])
def pm25():
    sort=False   
    if request.method=='POST':              
        if request.form.get('sort'):
            sort=True
        if request.form.get('update'):
            sort=False   

    columns, values, error = get_pm25(sort)
    time = get_today()
    return render_template('./pm25.html', **locals())


@app.route('/test')
def test():
    return render_template('./test.html')


@app.route('/')
@app.route('/<name>')
def index(name='GUEST'):
    time = get_today()
    result = {'time': time, 'name': name}
    return render_template('./index.html',
                           result=result)


@app.route('/stock')
def stock():
    time = get_today()
    stocks = [
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]

    return render_template('./stock.html', **locals())
    # return json.dumps(stocks, ensure_ascii=False)


@app.route('/sum/x=<x>&y=<y>')
def get_sum(x, y):
    try:
        return f'總合為:{eval(x)+eval(y)}'
    except Exception as e:
        return e


@app.route('/book/page=<int:page>')
def get_page(page):
    if page == 1:
        return 'JAVA'
    elif page == 2:
        return 'PYTHON'
    elif page == 3:
        return 'C++'

    return 'NO BOOK!'


@app.route('/bmi/height=<height>&weight=<weight>')
def get_bmi(height, weight):
    try:
        return f'''
        身高:{height}cm 體重{weight}kg==>
        BMI:{round(eval(weight)/(eval(height)/100)**2, 2)}'''
    except Exception as e:
        return '<h2>數值傳入錯誤!</h2>'


def get_today():
    today = datetime.now()
    return today.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    get_pm25_json()
    app.run(debug=True)
