from django.shortcuts import render, redirect
from .forms import CarbonFootprintForm
from .models import CarbonFootprintRecord
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

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


def generate_chart(data, labels, title):
    """Helper function to generate a chart and return base64 string."""
    plt.figure(figsize=(5, 3))
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    plt.bar(labels, data, color=colors[:len(labels)])
    plt.title(title)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    chart_data = base64.b64encode(image_png).decode('utf-8')
    plt.close()

    return f"data:image/png;base64,{chart_data}"

def carbon_result(request):
    # Fetch records sorted by the latest created_at timestamp
    records = CarbonFootprintRecord.objects.all().order_by('-created_at')
    if records.exists():
        latest_record = records[0]  # ✅ Get the latest entry
        latest_footprint = latest_record.total_footprint
    else:
        latest_footprint = 0  # Default value if no records exist

    # Group records by created_at
    records_by_time = {}
    for record in records:
        timestamp = record.created_at.strftime('%Y-%m-%d %H:%M:%S')  # 🔄 Updated
        if timestamp not in records_by_time:
            records_by_time[timestamp] = []
        records_by_time[timestamp].append(record)

    # Generate individual charts per timestamp
    timestamp_charts = {}
    for timestamp, records_list in records_by_time.items():
        travel_data = [
            sum(r.daily_car_km for r in records_list),
            sum(r.daily_bus_km for r in records_list),
            sum(r.daily_bike_km for r in records_list)
        ]
        travel_labels = ["Car Travel", "Bus Travel", "Bike Travel"]
        timestamp_charts[timestamp] = {
            "travel_chart": generate_chart(travel_data, travel_labels, f"Travel Usage ({timestamp})"),
        }

        electricity_data = [
            sum(r.num_ac for r in records_list),
            sum(r.ac_hours for r in records_list),
            sum(r.num_fridge for r in records_list),
            sum(r.num_fans for r in records_list),
            sum(r.fan_hours for r in records_list),
            sum(r.num_tv for r in records_list),
            sum(r.tv_hours for r in records_list)
        ]
        electricity_labels = ["AC", "AC Hours", "Fridge", "Fans", "Fan Hours", "TV", "TV Hours"]
        timestamp_charts[timestamp]["electricity_chart"] = generate_chart(electricity_data, electricity_labels, f"Electricity Usage ({timestamp})")

    # Overall Travel Usage
    travel_data = [
        sum(r.daily_car_km for r in records),
        sum(r.daily_bus_km for r in records),
        sum(r.daily_bike_km for r in records)
    ]
    travel_labels = ["Car", "Bus", "Bike"]
    overall_travel_chart = generate_chart(travel_data, travel_labels, "Overall Travel Usage")

    # Overall Electricity Usage
    electricity_data = [
        sum(r.num_ac for r in records),
        sum(r.ac_hours for r in records),
        sum(r.num_fridge for r in records),
        sum(r.num_fans for r in records),
        sum(r.fan_hours for r in records),
        sum(r.num_tv for r in records),
        sum(r.tv_hours for r in records)
    ]
    electricity_labels = ["AC", "AC Hours", "Fridge", "Fans", "Fan Hours", "TV", "TV Hours"]
    overall_electricity_chart = generate_chart(electricity_data, electricity_labels, "Overall Electricity Usage")

    # 🔹 Pass records separately to display them before visualizations
    return render(request, "registration/carbon_result.html", {
        "records": records,  # ✅ Send all records to display first
        "records_by_time": records_by_time,
        "timestamp_charts": timestamp_charts,
        "overall_travel_chart": overall_travel_chart,
        "overall_electricity_chart": overall_electricity_chart,
        "latest_footprint": latest_footprint
    })
