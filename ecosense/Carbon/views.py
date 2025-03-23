from django.shortcuts import render, redirect
from .forms import CarbonFootprintForm
from .models import CarbonFootprintRecord

# Emission Factors (kg CO₂ per unit)
ELECTRICITY_EMISSION_FACTOR = 0.92  # kg CO₂ per kWh (India)
CAR_EMISSION_FACTOR = 0.21  # kg CO₂ per km
BIKE_EMISSION_FACTOR = 0.10  # kg CO₂ per km
BUS_EMISSION_FACTOR = 0.06  # kg CO₂ per km
TRAIN_EMISSION_FACTOR = 0.02  # kg CO₂ per km (Train is very eco-friendly)

DIET_EMISSIONS = {
    'vegan': 83,  # Vegan (~1 ton CO₂ per year)
    'veg': 125,   # Vegetarian (~1.5 tons CO₂ per year)
    'pesc': 170,  # Pescatarian (~2 tons CO₂ per year)
    'nonveg': 250  # Non-Vegetarian (~3 tons CO₂ per year)
}

# Appliance Power Ratings (Watts)
APPLIANCE_POWER = {
    'ac': 1500, 'fridge': 250, 'fan': 75, 'tv': 120
}

def carbon_footprint(request):
    if request.method == "POST":
        form = CarbonFootprintForm(request.POST)
        if form.is_valid():
            # Calculate Carbon Footprint
            electricity_kwh = form.cleaned_data['monthly_kwh']
            electricity_footprint = electricity_kwh * ELECTRICITY_EMISSION_FACTOR

            ac_footprint = (form.cleaned_data['num_ac'] * form.cleaned_data['ac_hours'] * APPLIANCE_POWER['ac'] * 30) / 1000 * ELECTRICITY_EMISSION_FACTOR
            fan_footprint = (form.cleaned_data['num_fans'] * form.cleaned_data['fan_hours'] * APPLIANCE_POWER['fan'] * 30) / 1000 * ELECTRICITY_EMISSION_FACTOR
            tv_footprint = (form.cleaned_data['num_tv'] * form.cleaned_data['tv_hours'] * APPLIANCE_POWER['tv'] * 30) / 1000 * ELECTRICITY_EMISSION_FACTOR
            fridge_footprint = form.cleaned_data['num_fridge'] * APPLIANCE_POWER['fridge'] * 24 * 30 / 1000 * ELECTRICITY_EMISSION_FACTOR

            appliance_footprint = ac_footprint + fan_footprint + tv_footprint + fridge_footprint

            transport_footprint = 0
            transport_modes = form.cleaned_data['transport_mode']

            if 'car' in transport_modes:
                transport_footprint += form.cleaned_data['daily_car_km'] * 30 * CAR_EMISSION_FACTOR
            if 'bike' in transport_modes:
                transport_footprint += form.cleaned_data['daily_bike_km'] * 30 * BIKE_EMISSION_FACTOR
            if 'bus' in transport_modes:
                transport_footprint += form.cleaned_data['daily_bus_km'] * 30 * BUS_EMISSION_FACTOR
            if 'train' in transport_modes:
                transport_footprint += form.cleaned_data['daily_train_km'] * 30 * TRAIN_EMISSION_FACTOR

            diet_footprint = DIET_EMISSIONS[form.cleaned_data['diet_type']]

            total_footprint = electricity_footprint + appliance_footprint + transport_footprint + diet_footprint

            # Save data in the database
            CarbonFootprintRecord.objects.create(
                num_people=form.cleaned_data['num_people'],
                monthly_kwh=form.cleaned_data['monthly_kwh'],
                num_ac=form.cleaned_data['num_ac'],
                ac_hours=form.cleaned_data['ac_hours'],
                num_fridge=form.cleaned_data['num_fridge'],
                num_fans=form.cleaned_data['num_fans'],
                fan_hours=form.cleaned_data['fan_hours'],
                num_tv=form.cleaned_data['num_tv'],
                tv_hours=form.cleaned_data['tv_hours'],
                daily_car_km=form.cleaned_data['daily_car_km'],
                daily_bus_km=form.cleaned_data['daily_bus_km'],
                daily_bike_km=form.cleaned_data['daily_bike_km'],
                diet_type=form.cleaned_data['diet_type'],
                total_footprint=total_footprint
            )

            return redirect('carbon_result')

    else:
        form = CarbonFootprintForm()

    return render(request, "registration/carbon.html", {"form": form})

def carbon_result(request):
    records = CarbonFootprintRecord.objects.all().order_by('-created_at')
    latest_record = records.first()
    return render(request, "registration/carbon_result.html", {"records": records, "total_footprint": latest_record.total_footprint})
