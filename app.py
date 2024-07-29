from flask import Flask, render_template, request
from joblib import load
from datetime import datetime
import pandas as pd

app = Flask(__name__)
best_bagging_regressor = "best_bagging_regressor.joblib"
loaded_model = load(best_bagging_regressor)

def predict_commulative_gross_gen(model, input_date):
    input_data = pd.DataFrame({
        'month': [input_date.month],
        'year': [input_date.year],
        'day': [input_date.day],
    })
    predicted_value = model.predict(input_data)
    return predicted_value[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_value = None
    sales_value = None

    if request.method == 'POST':
        user_input_date = request.form['input_date']
        user_input_date = datetime.strptime(user_input_date, '%Y-%m-%d')
        predicted_value = predict_commulative_gross_gen(loaded_model, user_input_date)
        sales_value = predicted_value * 3.5

    return render_template('home.html', predicted_value=predicted_value, sales_value=sales_value)

if __name__ == '__main__':
    app.run(debug=True)
