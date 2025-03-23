from django import forms
from .models import CarbonFootprintRecord

class CarbonFootprintForm(forms.ModelForm):
    transport_mode = forms.MultipleChoiceField(
        label="Which transport modes do you use?",
        choices=[('car', 'Car'), ('bike', 'Bike'), ('bus', 'Bus'), ('train', 'Train')],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = CarbonFootprintRecord
        fields = [
            'num_people', 'monthly_kwh', 'num_ac', 'ac_hours', 'num_fridge', 'num_fans', 'fan_hours', 'num_tv', 'tv_hours',
            'daily_car_km', 'daily_bus_km', 'daily_bike_km', 'daily_train_km', 'diet_type'
        ]
        labels = {
            'num_people': 'Number of People in Household',
            'monthly_kwh': 'Monthly Electricity Consumption (kWh)',
            'num_ac': 'Number of Air Conditioners',
            'ac_hours': 'Daily AC Usage (hours)',
            'num_fridge': 'Number of Refrigerators',
            'num_fans': 'Number of Fans',
            'fan_hours': 'Daily Fan Usage (hours)',
            'num_tv': 'Number of Televisions',
            'tv_hours': 'Daily TV Usage (hours)',
            'daily_car_km': 'Daily Car Travel (km)',
            'daily_bus_km': 'Daily Bus Travel (km)',
            'daily_bike_km': 'Daily Bike Travel (km)',
            'diet_type': 'Diet Type',
        }
        widgets = {
            'diet_type': forms.Select(choices=[('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian')]),
        }
