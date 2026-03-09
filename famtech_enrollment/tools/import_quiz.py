import pandas as pd
from odoo import api, SUPERUSER_ID

def import_quiz(cr, uid, path):
    """
    Utility script to bulk import quiz questions from an Excel file.
    Run this via Odoo shell.
    """
    env = api.Environment(cr, uid, {})
    
    # Read the Excel file using pandas
    df = pd.read_excel(path)
    
    # Find the target eLearning course
    course = env['slide.channel'].search([('name', '=', 'Autodesk AutoCAD')], limit=1)
    
    if not course:
        print("Course not found! Please check the course name.")
        return

    # Loop through the Excel rows and create quiz slides
    for index, row in df.iterrows():
        slide = env['slide.slide'].create({
            'name': row['Question'],
            'slide_type': 'quiz',
            'channel_id': course.id,
            # Note: question/answer creation logic depends on Odoo version (survey vs slides)
        })
        print(f"Imported question: {row['Question']}")
        
    print("Quiz import completed successfully!")