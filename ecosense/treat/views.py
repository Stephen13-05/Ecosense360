import google.generativeai as genai
from django.shortcuts import render
import markdown
from Carbon.models import CarbonFootprintRecord  
from django.conf import settings  # ✅ Import settings to access the API key
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.html import strip_tags
from reportlab.lib.utils import simpleSplit
import io
import textwrap



# ✅ Configure Gemini API with the key from settings
genai.configure(api_key=settings.GEMINI_API_KEY)

def get_tailored_recommendations(request):
    latest_record = CarbonFootprintRecord.objects.order_by('-created_at').first()

    if not latest_record:
        return render(request, "treat/recommendations.html", {"message": "No records found!"})

    prompt = f"""
    I have a monthly carbon footprint of {latest_record.total_footprint:.2f} kg CO₂.
    Here are my carbon emission details:
    - Car Travel: {latest_record.daily_car_km} km/day
    - Bus Travel: {latest_record.daily_bus_km} km/day
    - Bike Travel: {latest_record.daily_bike_km} km/day
    - Number of ACs: {latest_record.num_ac}
    - AC Usage Hours: {latest_record.ac_hours} per day
    - Fridges: {latest_record.num_fridge}
    - Fans: {latest_record.num_fans}
    - Fan Usage Hours: {latest_record.fan_hours} per day
    - TVs: {latest_record.num_tv}
    - TV Usage Hours: {latest_record.tv_hours} per day

    Please suggest tailored recommendations to **reduce my carbon footprint** effectively.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash-8b")  
        response = model.generate_content(prompt)
        recommendations = response.text if hasattr(response, "text") else "No recommendations generated."
        # Convert newlines to HTML line breaks & preserve formatting
        recommendations = markdown.markdown(recommendations)

    except Exception as e:
        recommendations = f"Error generating recommendations: {str(e)}"

    return render(request, "registration/recommendations.html", {
        "latest_record": latest_record,
        "recommendations": mark_safe(recommendations)  # ✅ Mark recommendations as safe HTML
    })

def download_pdf(request):
    if request.method == "POST":
        recommendations = request.POST.get("recommendations", "No recommendations available.")
    else:
        recommendations = request.GET.get("recommendations", "No recommendations available.")

    print("DEBUG: Recommendations received ->", recommendations)

    # Remove HTML tags to keep only the plain text for the PDF
    plain_text = strip_tags(recommendations)

    lines = plain_text.split("\n")

    # Create an in-memory buffer
    buffer = io.BytesIO()

    # Create a PDF object
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Carbon Footprint Recommendations")

    # Write the content with formatting
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 750, "Your Personalized Carbon Footprint Recommendations")

    pdf.setFont("Helvetica", 12)

    # Process multi-line text and fit into the PDF
    y_position = 730
    line_height = 16

    for line in lines:
        wrapped_lines = textwrap.wrap(line, width=80)  # Wrap text within the PDF width
        for wrapped_line in wrapped_lines:
            pdf.drawString(100, y_position, wrapped_line)
            y_position -= line_height

        # Move to next page if needed
            if y_position < 50:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y_position = 750

    pdf.showPage()
    pdf.save()

    # Move buffer position to the beginning
    buffer.seek(0)

    # Return the PDF response
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="recommendations.pdf"'
    
    return response