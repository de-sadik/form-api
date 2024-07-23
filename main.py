from fastapi import FastAPI, HTTPException, Form

from fastapi.responses import FileResponse
from fpdf import FPDF
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fpdf import FPDF
from fastapi import Form
from fastapi.exceptions import HTTPException

app = FastAPI(
    title="Form App",
    version="1.0",
    description="API for filling PDF form"
)

def generate_pdf_with_fpdf(name, date, address, favourite_activities, favourite_activity):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add text fields
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Date: {date}", ln=True)
    pdf.cell(0, 10, f"Address: {address}", ln=True)

    # Add checkboxes
    activities = ["Reading", "Walking", "Music", "Other"]
    pdf.cell(0, 10, "Favourite Activities:", ln=True)
    for activity in activities:
        checkbox = "X" if activity.lower() in [act.lower() for act in favourite_activities] else " "
        pdf.cell(0, 10, f"[{checkbox}] {activity}", ln=True)

    # Add radio buttons
    pdf.cell(0, 10, "Favourite Activity:", ln=True)
    for activity in activities:
        radio_button = "O" if activity.lower() == favourite_activity.lower() else " "
        pdf.cell(0, 10, f"({radio_button}) {activity}", ln=True)

    output_pdf_path = "filled_form.pdf"
    pdf.output(output_pdf_path)
    return output_pdf_path

@app.post("/fill-pdf-form")
async def generate_pdf(
    name: str = Form(...), 
    date: str = Form(...), 
    address: str = Form(...), 
    favourite_activities: list = Form(...), 
    favourite_activity: str = Form(...)
):
    if not name or not date or not address or not favourite_activities or not favourite_activity:
        raise HTTPException(status_code=400, detail="Missing required fields")

    output_pdf_path = generate_pdf_with_fpdf(name, date, address, favourite_activities, favourite_activity)
    return FileResponse(output_pdf_path, media_type='application/pdf', filename="filled_form.pdf")