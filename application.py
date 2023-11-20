from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

application = Flask(__name__)
app = application

# Home Page
@app.route('/')
def home_page():
    return render_template('index.html')

# Code for calculations
@app.route('/calculate', methods=['GET','POST'])
def calculate_sip():
    if request.method=='GET':
        return render_template('index.html')
    else:
        # Take Input from HTML Form
        P = float(request.form.get('investmentAmount'))
        N = float(request.form.get('investmentPeriod'))
        R = float(request.form.get('annualReturn'))
        # Returns Calculations        
        n = N*12
        i = R/1200
        x = (1+i)**n
        M = P*((x-1)/i)*(1+i)
        M = round(M)
        Inv = round(P*n) 
        Ret = round(M - Inv)       
        pct_ret = round((Ret/Inv)*100,2)
        # Plotly Graph preperation
        dct = {'Names':['Invested', 'Returns'], 'Values':[Inv, Ret]}
        df = pd.DataFrame(dct)
        fig = px.pie(df, values='Values', names='Names', title='Invested vs Returns')
        # Convert the Plotly figure to HTML
        graph_html = pio.to_html(fig, full_html=False)
        return render_template('index.html', Inv=Inv, M=M, Ret=Ret, pct_ret=pct_ret, graph_html=graph_html)
    
# Creating API
@app.route('/calculate_api', methods=['POST'])
def api_calculation():
    # Take Input from HTML Form
    P = request.json['investmentAmount']
    N = request.json['investmentPeriod']
    R = request.json['annualReturn']
    # Returns Calculations        
    n = N*12
    i = R/1200
    x = (1+i)**n
    M = P*((x-1)/i)*(1+i)
    M = round(M)
    Inv = round(P*n) 
    Ret = round(M - Inv)       
    pct_ret = round((Ret/Inv)*100,2)    
    return jsonify({'Amount Invested' : Inv,
                    'Estimated Returns' : Ret,
                    'Total Value' : M,
                    'Percentage Returns' : pct_ret})
        
if __name__=='__main__':
    app.run(host='0.0.0.0', debug=False)
