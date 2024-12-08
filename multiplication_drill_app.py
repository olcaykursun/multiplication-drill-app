import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random

def generate_pdf():
    buffer = BytesIO()

    # Page setup
    page_width, page_height = letter
    c = canvas.Canvas(buffer, pagesize=letter)
    margin = 50
    col_width = (page_width - 2 * margin) / 4
    row_height = 20 * 1.25
    num_rows = 25  # Number of rows per column
    num_cols = 4  # Number of columns

    # Title and header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, page_height - 40, "Multiplication Drill")
    c.setFont("Helvetica", 12)
    c.drawString(margin, page_height - 60, "Name: ____________________________")
    c.drawString(page_width - 200, page_height - 60, "Date: _____________________")

    # Draw rectangles around column pairs
    c.setStrokeColor("black")
    c.setLineWidth(1)

    # Rectangle for first two columns
    rect1_x = margin
    rect1_y = page_height - 100 - num_rows * row_height
    c.rect(rect1_x, rect1_y, col_width * 2, num_rows * row_height+20)

    # Rectangle for last two columns
    rect2_x = margin + col_width * 2
    rect2_y = rect1_y
    c.rect(rect2_x, rect2_y, col_width * 2, num_rows * row_height+20)

    # Generate questions
    question_number = 1
    for col in range(num_cols):
        for row in range(num_rows):
            x = margin + col * col_width
            y = page_height - 100 - row * row_height

            # Generate random multiplication question
            num1 = random.randint(0, 10)
            num2 = random.randint(0, 10)

            # Format question
            question = f"{question_number}. {num1} × {num2} = ______"
            c.drawString(x, y, question)

            # Increment question number
            question_number += 1

        # Reset question number for next pair of columns
        if col == 1:  # Last column of the first pair
            question_number = 1

    # Add Time and Score inside each box
    c.setFont("Helvetica-Bold", 12)

    # For first box
    time_score_x1 = rect1_x + 10
    time_score_y1 = rect1_y + 5
    c.drawString(time_score_x1, time_score_y1, "Time: ________  Score: ________")

    # For second box
    time_score_x2 = rect2_x + 10
    time_score_y2 = rect2_y + 5
    c.drawString(time_score_x2, time_score_y2, "Time: ________  Score: ________")

    c.save()

    # Ensure the buffer is ready for download
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title("Multiplication Drill Generator")
st.write("Click the button below to generate and download your worksheet.")

pdf = generate_pdf()  # Call the generate_pdf function
st.download_button(
    label="Download Worksheet",
    data=pdf,
    file_name="multiplication_drill.pdf",
    mime="application/pdf"
)
