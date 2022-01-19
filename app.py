from flask import Flask, render_template ,Markup ,request
from fertilizer_dic import fertilizer_dic
import numpy as np
import pandas as pd
import pickle


crop_recommendation_model_path = 'model/RandomForest.pkl'
crop_recommendation_model = pickle.load(open(crop_recommendation_model_path, 'rb'))

#-----Flask App-----
app = Flask(__name__)


@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route("/")
def index():
    return render_template('home.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/crop")
def crop():
    return render_template('crop.html')

@app.route("/fertilizers")
def fertilizers():
    return render_template('fertilizers.html')

#-----Crop Prediction-----
@ app.route('/crop_prediction', methods=['POST'])
def crop_prediction():
    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['potassium'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction = crop_recommendation_model.predict(data)
        final_prediction = my_prediction[0]
        return render_template('crop_result.html', prediction=final_prediction, pred='images/crop/'+ final_prediction +'.jpg')

#-----Fertilizers-----
@ app.route('/fertilizer_recommend', methods=['POST'])
def fertilizer_recommend():
    
    crop_name = str(request.form['cropname'])
    N_filled = int(request.form['nitrogen'])
    P_filled = int(request.form['phosphorous'])
    K_filled = int(request.form['potassium'])

    df = pd.read_csv('Data/fertilizers.csv')

    N_desired = df[df['Crop'] == crop_name]['N'].iloc[0]
    P_desired = df[df['Crop'] == crop_name]['P'].iloc[0]
    K_desired = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = N_desired- N_filled
    p = P_desired - P_filled
    k = K_desired - K_filled

    if n < 0:
        key1 = "NHigh"
    elif n > 0:
        key1 = "Nlow"
    else:
        key1 = "NNo"

    if p < 0:
        key2 = "PHigh"
    elif p > 0:
        key2 = "Plow"
    else:
        key2 = "PNo"

    if k < 0:
        key3 = "KHigh"
    elif k > 0:
        key3 = "Klow"
    else:
        key3 = "KNo"

    abs_n = abs(n)
    abs_p = abs(p)
    abs_k = abs(k)

    response1 = Markup(str(fertilizer_dic[key1]))
    response2 = Markup(str(fertilizer_dic[key2]))
    response3 = Markup(str(fertilizer_dic[key3]))
    return render_template('fertilizer_result.html', recommendation1=response1,
                           recommendation2=response2, recommendation3=response3,
                           diff_n = abs_n, diff_p = abs_p, diff_k = abs_k)



if __name__ == "__main__":
    app.run(debug=True)

