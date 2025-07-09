from django import forms

class LaptopForm(forms.Form):
    Company = forms.ChoiceField(choices=[('Apple', 'Apple'), ('Dell', 'Dell'), ('HP', 'HP'), ('Lenovo', 'Lenovo')])
    TypeName = forms.ChoiceField(choices=[('Ultrabook', 'Ultrabook'), ('Notebook', 'Notebook'), ('Gaming', 'Gaming')])
    Ram = forms.IntegerField(label='RAM (GB)')
    Weight = forms.FloatField(label='Weight (kg)')
    Touchscreen = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    Ips = forms.ChoiceField(choices=[(0, 'No'), (1, 'Yes')])
    ppi = forms.FloatField(label='PPI')
    OpSys = forms.ChoiceField(choices=[('Windows 10', 'Windows 10'), ('Mac', 'Mac'), ('No OS', 'No OS')])
    Cpu_Brand = forms.ChoiceField(label='CPU Brand', choices=[
        ('Intel Core i3', 'Intel Core i3'), 
        ('Intel Core i5', 'Intel Core i5'),
        ('Intel Core i7', 'Intel Core i7'),
        ('Other Intel Processor', 'Other Intel Processor'),
        ('AMD Processor', 'AMD Processor')
    ])
    HDD = forms.IntegerField(label='HDD (GB)')
    SSD = forms.IntegerField(label='SSD (GB)')
    Gpu_brand = forms.ChoiceField(choices=[('Intel', 'Intel'), ('Nvidia', 'Nvidia'), ('AMD', 'AMD')])
