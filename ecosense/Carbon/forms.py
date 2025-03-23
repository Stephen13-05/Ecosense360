from django import forms

class CarbonFootprintForm(forms.Form):
    # 🏡 Household & Electricity Usage
    num_people = forms.IntegerField(label="How many people live in your house?", min_value=1)
    monthly_kwh = forms.IntegerField(label="How many units (kWh) of electricity do you consume monthly?", min_value=0)
    
    # ⚡ Appliance Usage
    num_ac = forms.IntegerField(label="Number of Air Conditioners", min_value=0)
    ac_hours = forms.IntegerField(label="Hours AC is used daily", min_value=0, max_value=24)
    
    num_fridge = forms.IntegerField(label="Number of Refrigerators", min_value=0)
    
    num_fans = forms.IntegerField(label="Number of Fans", min_value=0)
    fan_hours = forms.IntegerField(label="Hours Fans are used daily", min_value=0, max_value=24)
    
    num_tv = forms.IntegerField(label="Number of Televisions", min_value=0)
    tv_hours = forms.IntegerField(label="Hours TV is used daily", min_value=0, max_value=24)

    # 🚗 Transportation
    daily_car_km = forms.IntegerField(label="Kilometers traveled by car daily", min_value=0)
    daily_bus_km = forms.IntegerField(label="Kilometers traveled by bus daily", min_value=0)
    daily_bike_km = forms.IntegerField(label="Kilometers traveled by bike daily", min_value=0)

    # 🍽️ Diet Choices
    diet_type = forms.ChoiceField(
        label="What is your diet type?",
        choices=[('veg', 'Vegetarian'), ('nonveg', 'Non-Vegetarian'), ('vegan', 'Vegan')],
        widget=forms.RadioSelect
    )

    # 🗑️ Waste Management
    waste_type = forms.ChoiceField(
        label="How do you dispose of waste?",
        choices=[('recycle', 'Recycling & Composting'), ('normal', 'Normal Disposal (No Recycling)')],
        widget=forms.RadioSelect
    )
