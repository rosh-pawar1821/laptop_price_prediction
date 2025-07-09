from django.shortcuts import render
import joblib
import numpy as np
from .forms import LaptopForm

model = joblib.load('laptopapp/model.pkl')
def predict_price(request):
    prediction = None

    if request.method == 'POST':
        form = LaptopForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

           
            input_data = np.array([[
                data['Company'],
                data['TypeName'],
                data['Ram'],
                data['Weight'],
                int(data['Touchscreen']),
                int(data['Ips']),
                data['ppi'],
                data['OpSys'],
                data['Cpu_Brand'],
                data['HDD'],
                data['SSD'],
                data['Gpu_brand']
            ]])

            import pandas as pd

           
            input_df = pd.DataFrame([{
                'Company': data['Company'],
                'TypeName': data['TypeName'],
                'Ram': data['Ram'],
                'Weight': data['Weight'],
                'Touchscreen': data['Touchscreen'],
                'Ips': data['Ips'],
                'ppi': data['ppi'],
                'OpSys': data['OpSys'],
                'Cpu Brand': data['Cpu_Brand'],
                'HDD': data['HDD'],
                'SSD': data['SSD'],
                'Gpu brand': data['Gpu_brand']
            }])

            
            prediction = round(model.predict(input_df)[0], 2)

    else:
        form = LaptopForm()

    return render(request, 'laptopapp/predict.html', {
        'form': form,
        'prediction': prediction
    })
