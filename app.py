from flask import Flask, render_template, request, redirect, url_for, session, send_file
from weasyprint import HTML
from io import BytesIO
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Add zip to Jinja environment
app.jinja_env.globals.update(zip=zip)

segment_questions = {
    1: [
        "Age at First Misconduct",
        "Number of Previous Misconduct(s)",
        "Extent of Involvment in Organized Crimes",
        "Number of Derogatory Record",
        "Type of Offender",
        "History of Violence"
    ],
    2: [
        "Type of Companions",
        "Type of Activities with Companions",
        "Friends' Support"
    ],
    3.: [
        "Is it okay to break the rules/laws as long as I can help my family.",
        "Is it okay to break the rules/laws because I don't know it.",
        "Is it okay to break the rules/laws when nobody sees me or I don't get caught.",
        "It is okay to commit a crime if you're a victim of social injustice/inequality.",
        "Is it okay to commit a crime when you are in a desperate situation/crisis"
    ],
    4: [
        "I find it hard to follow rules.",
        "I lie and cheat to get what I want.",
        "I act without thinking of the consequences of my actions.",
        "I easily get irritated or angry.",
        "I don't care who gets hurt as long as I get what I want.",
        "I find it hard to follow through with responsibilities/assigned tasks"
    ],
    5: [
        "Educational Attainment",
        "Educational Attachment",
        "Overall Conduct in School",
        "Employment Status at the Time of Arrest",
        "Employable Skills",
        "Employment History"
    ],
    6: [
        "Quality of Family/Marital Relationships",
        "Parental Guidance and Supervision",
        "Family Acceptability in the Community",
        "Spirituality/Religiosity"
    ],
    7: [
        "History of Drug Abuse",
        "frequency of Drug Use",
        "History of Alcohol Abuse",
        "Frequency of Alcohol Use",
        "Desire/Urge for Substance Use",
        "Cut down onn Substance Use",
        "Family History of Substance Use"
    ],
    8: [
        "I can perform my daily activities with minimal support from others",
        "I can easily make good decisions on my own",
        "I have experienced sadness for 14 days over the last 6 months",
        "I have received consultation/treatment/counseling for a psychological/psychiatric problem",
        "I sometimes hear or see things not normally seen or heard by others"
    ]
}

# Add this dictionary to your app.py after the segment_questions dictionary
segment_answers_data = {
    1: {  # Criminal History
        0: [  # First question
            {"text": "26 years old and above", "value": 0},
            {"text": "18-25 years old", "value": 1},
            {"text": "17 years old and below", "value": 2}
        ],
        1: [  # Second question
            {"text": "No misconduct", "value": 0},
            {"text": "1 misconduct", "value": 1},
            {"text": "2 or more misconducts", "value": 2}
        ],
        2: [  # Third question
            {"text": "No involvement", "value": 0},
            {"text": "Some involvement", "value": 1},
            {"text": "Heavy involvement", "value": 2}
        ],
        3: [  # Fourth question
            {"text": "No record", "value": 0},
            {"text": "With 1 record", "value": 1},
            {"text": "With 2 or more records", "value": 2}
        ],
        4: [  # Fifth question
            {"text": "Situational/Circumstantial", "value": 0},
            {"text": "Paminsan-minsan", "value": 1},
            {"text": "Career offender", "value": 2}
        ],
        5: [  # Sixth question
            {"text": "No history of violence", "value": 0},
            {"text": "1 incident of violence", "value": 1},
            {"text": "2 or more history of violence", "value": 2}
        ]
    },
    2: {  # Pro-Criminal Companions
        0: [
            {"text": "Mostly conventional", "value": 0},
            {"text": "Sometimes conventional, sometimes delinquent", "value": 1},
            {"text": "Mostly delinquent", "value": 2}
        ],
        1: [
            {"text": "Mostly conventional", "value": 0},
            {"text": "Sometimes conventional, sometimes delinquent", "value": 1},
            {"text": "Mostly delinquent", "value": 2}
        ],
        2: [
            {"text": "Mostly supportive friends", "value": 0},
            {"text": "Few supportive friends", "value": 1},
            {"text": "No supportive friends", "value": 2}
        ]
    },
    3: {  # Pro-Criminal Attitudes & Cognitions
        0: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 2}
        ],
        1: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 2}
        ],
        2: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 2}
        ], 
        3: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 2}
        ],
        4: [   
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 2}
        ]
    },
    4: {  # Anti-Social Personality Patterns
        0: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ],
        1: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ],
        2: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ],
        3: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ],
        4: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ],
        5: [
            {"text": "NO", "value": 0},
            {"text": "YES", "value": 1}
        ]
    },
    5: {  # Education and Employment
        0: [
            {"text": "Vocational/College level & above", "value": 0},
            {"text": "Grade 7 to 12", "value": 1},
            {"text": "Grade 6 and below", "value": 2}
        ],
        1: [
            {"text": "Interested in school", "value": 0},
            {"text": "Lacks interest in school", "value": 1},
            {"text": "Did not get along well with teachers and other students/No interest in school", "value": 2}
        ],
        2: [
            {"text": "Without misdemeanor", "value": 0},
            {"text": "With misdemeanor", "value": 2}
        ],
        3: [
            {"text": "Employed", "value": 0},
            {"text": "Irregularly employed", "value": 1},
            {"text": "Unemployed", "value": 2}
        ],
        4: [
            {"text": "With at least employable skill", "value": 0},
            {"text": "No employable skill but with potential and capacity to acquire one", "value": 1},
            {"text": "No employable skill", "value": 2}
        ],
        5: [
            {"text": "Treats job seriously; Finds work rewarding; Good relationship with employer and co-workers", "value": 0},
            {"text": "Inconsistent employment; No employment that lasts 3 months; Minimum attachment to work", "value": 1},
            {"text": "Does not like/love job; Conflict with the employer; No interest in working; No attachments to work; Frequently fired from work", "value": 2}
        ]
    },
    6: {  # Family and Marital Status
        0: [
            {"text": "With positive influence", "value": 0},
            {"text": "With occasional negative influence", "value": 1},
            {"text": "With regular negative influence", "value": 2}
        ],
        1: [
            {"text": "Adequate guidance and supervision", "value": 0},
            {"text": "Minimal guidance and supervision", "value": 1},
            {"text": "Without guidance and supervision; Overbearing/Over Protective", "value": 2}
        ],
        2: [
            {"text": "Acceptable", "value": 0},
            {"text": "Unacceptable", "value": 1},
            {"text": "Highly unacceptable", "value": 2}
        ],
        3: [
            {"text": "Integrated spiritual belief and religious activities", "value": 0},
            {"text": "Disintegrated spiritual belief but with some manifested positive religious belief", "value": 1},
            {"text": "Disintegrated religious belief and negative religious activities", "value": 2}
        ]
    },
    7: {  # Substance Abuse
        0: [
            {"text": "If client abused drugs (other than those required for medical reasons)", "value": 1},
            {"text": "Never", "value": 0}
        ],
        1: [
            {"text": "No usage", "value": 0},
            {"text": "At least once a month", "value": 1},
            {"text": "At least once a week", "value": 2},
            {"text": "Almost daily", "value": 3}
        ],
        2: [
            {"text": "If client abused alcoholic beverages", "value": 1},
            {"text": "At least once a month", "value": 0}
        ],
        3: [
            {"text": "No usage", "value": 0},
            {"text": "At least once a month", "value": 1},
            {"text": "At least once a week", "value": 2},
            {"text": "Almost daily", "value": 3}
        ],
        4: [
            {"text": "Never", "value": 0},
            {"text": "Sometimes", "value": 1},
            {"text": "Always", "value": 2}
        ],
        5: [  # Cut down on Substance Use
            {"text": "Always able to stop", "value": 0},
            {"text": "Unable to stop", "value": 1}
        ],
        6: [  # Family History of Substance Use
            {"text": "YES", "value": 1},
            {"text": "NO", "value": 0}
        ]
    },
    8: {  # Mental Health
        0: [
            {"text": "YES", "value": 0},
            {"text": "NO", "value": 1}
        ],
        1: [
            {"text": "YES", "value": 0},
            {"text": "NO", "value": 1}
        ], 
        2: [
            {"text": "YES", "value": 1},
            {"text": "NO", "value": 0}
        ],
        3: [
            {"text": "YES", "value": 1},
            {"text": "NO", "value": 0}
        ],
        4: [
            {"text": "YES", "value": 1},
            {"text": "NO", "value": 0}
        ]
    }
}

# Segment titles
segment_titles = {
    1: "CRIMINAL HISTORY",
    2: "PRO-CRIMINAL COMPANIONS",
    3: "PRO-CRIMINAL ATTITUDES & COGNITIONS",
    4: "ANTI-SOCIAL PERSONALITY PATTERNS",
    5: "EDUCATION AND EMPLOYMENT",
    6: "FAMILY AND MARITAL STATUS",
    7: "SUBSTANCE ABUSE",
    8: "MENTAL HEALTH"
}

# Update segment thresholds
segment_thresholds = {
    1: {"threshold": 5, "program": "ICARE", "highest_score": 10},
    2: {"threshold": 4, "program": "ICARE", "highest_score": 8},
    3: {"threshold": 4, "program": "ICARE", "highest_score": 8},
    4: {"threshold": 4, "program": "ICARE", "highest_score": 8},
    5: {
        "threshold": 4, 
        "program": "LEAP",
        "highest_score": 8,
        "education": {
            "name": "EDUCATION",
            "threshold": 4,
            "questions": [0, 1, 2]  # indices of education questions
        },
        "employment": {
            "name": "EMPLOYMENT",
            "threshold": 4,
            "questions": [3, 4, 5]  # indices of employment questions
        }
    },
    6: {"threshold": 4, "program": "LEAP", "highest_score": 8},
    7: {"threshold": 4, "program": "ICARE", "highest_score": 8},
    8: {"threshold": 4, "program": "Hulagpos", "highest_score": 8}
}

# Mandatory programs
mandatory_programs = [
    "Monthly/periodic report-in-person",
    "Monitoring and Supervision",
    "Therapeutic Community Ladderized Program (TCLP) Mandatory Reinforcing Activities",
    "Restorative Justice Processes",
    "Individual/Group Family/Marital Coaching",
    "Community Work Service/Involvement in community/barangay integration activities",
    "Spiritual/Moral Formation/Reformation activities"
]

# Risk level assessment
def assess_risk_level(total_score, length_of_sentence):
    if total_score <= 17:
        return {
            "level": "Low Risk (Level 1)",
            "probation": "6 months" if length_of_sentence == "2-years-or-less" else "1 year",
            "supervision": "Once in 2 months"
        }
    elif total_score <= 28:
        return {
            "level": "Medium Risk (Level 2)",
            "probation": "6 months" if length_of_sentence == "2-years-or-less" else "1 year",
            "supervision": "Once a month"
        }
    elif total_score <= 39:
        return {
            "level": "High Risk (Level 3)",
            "probation": "1 year" if length_of_sentence == "2-years-or-less" else "2 years",
            "supervision": "Twice a month"
        }
    else:
        return {
            "level": "Very High Risk (Level 4)",
            "probation": "2 years" if length_of_sentence == "2-years-or-less" else "3 years",
            "supervision": "Twice a month"
        }

def calculate_segments_per_page():
    """Calculate how many segments fit on first page based on content height"""
    average_segment_height = 200  # pixels
    page_height = 1122  # A4 height in pixels at 96dpi
    usable_height = page_height - 150  # Subtract header
    segments_per_column = usable_height // average_segment_height
    return segments_per_column * 2  # Two columns per page

@app.route('/')
def index():
    session.clear()
    # Initialize scores for all segments
    for i in range(1, 9):
        session[f'segment{i}_scores'] = []
    return render_template('index.html')

@app.route('/segment/<int:segment_id>', methods=['GET', 'POST'])
def segment(segment_id):
    if request.method == 'POST':
        if segment_id == 1:
            # Save initial form data
            session['client_name'] = request.form.get('client_name')
            session['officer_name'] = request.form.get('officer_name')
            session['chief_name'] = request.form.get('chief_name')
            session['length_of_sentence'] = request.form.get('length_of_sentence')
        
        # Save scores from previous segment
        prev_segment = segment_id - 1
        if prev_segment > 0:
            scores = []
            # Get all radio button responses with the segment prefix
            form_data = [k for k in request.form.keys() if k.startswith(f'seg{prev_segment}_q')]
            question_count = len(form_data)
            
            # Extract scores in order
            for i in range(1, question_count + 1):
                score = int(request.form.get(f'seg{prev_segment}_q{i}', 0))
                scores.append(score)
            
            session[f'segment{prev_segment}_scores'] = scores
            
    # If we've completed all segments, go to results
    if segment_id > 8:
        return redirect(url_for('results'))
        
    return render_template(
        'segment.html', 
        segment_id=segment_id, 
        title=segment_titles[segment_id],
        next_segment=segment_id + 1
    )

# Add this route to handle saving notes
@app.route('/save_notes', methods=['POST'])
def save_notes():
    notes = request.form.get('notes', '')
    session['notes'] = notes
    return '', 204  # Return a no content response

# Update the results route to handle the split segment
@app.route('/results')
def results():
    subtotals = {}
    total_score = 0
    
    for i in range(1, 9):
        segment_scores = session.get(f'segment{i}_scores', [])
        if i == 5:  # Handle split segment
            # First half (Education)
            subtotals[5] = sum(segment_scores[:3])
            # Second half (Employment)
            subtotals[6] = sum(segment_scores[3:])
            total_score += sum(segment_scores)
        elif i < 5:  # Segments before split
            subtotal = sum(segment_scores)
            subtotals[i] = subtotal
            total_score += subtotal
        else:  # Segments after split (adjust index)
            subtotal = sum(segment_scores)
            subtotals[i+1] = subtotal  # Shift index by 1
            total_score += subtotal
    
    length_of_sentence = session.get('length_of_sentence', '2-years-or-less')
    risk_assessment = assess_risk_level(total_score, length_of_sentence)
    
    # Determine recommended programs
    recommended_programs = []
    for segment_id, data in segment_thresholds.items():
        threshold_met = subtotals.get(segment_id, 0) >= data["threshold"]
        if threshold_met:
            program_name = f"{data['program']} ({data.get('name', segment_titles.get(segment_id, ''))})"
            recommended_programs.append(program_name)
    
    return render_template(
        'results.html',
        subtotals=subtotals,
        total_score=total_score,
        risk_assessment=risk_assessment,
        recommended_programs=recommended_programs,
        mandatory_programs=mandatory_programs,
        segment_titles=segment_titles,
        segment_thresholds=segment_thresholds,
        notes=session.get('notes', '')
    )

def calculate_split_scores(segment_answers, segment_id=5):
    """Calculate separate scores for education and employment sections"""
    education_score = 0
    employment_score = 0
    
    if segment_id in segment_answers:
        edu_indices = segment_thresholds[segment_id]['education']['questions']
        emp_indices = segment_thresholds[segment_id]['employment']['questions']
        
        for i, score in enumerate(segment_answers[segment_id]['scores']):
            if i in edu_indices:
                education_score += score
            elif i in emp_indices:
                employment_score += score
    
    return education_score, employment_score

@app.route('/generate_pdf')
def generate_pdf():
    subtotals = {}
    segment_answers = {}
    segment_data = {}  # New dictionary to store remapped data
    total_score = 0
    
    # First, collect all scores
    for i in range(1, 9):
        segment_scores = session.get(f'segment{i}_scores', [])
        if i == 5:  # Split segment
            # Education (stays as segment 5)
            subtotals[5] = sum(segment_scores[:3])
            segment_answers[5] = {
                'questions': segment_questions[5][:3],
                'scores': segment_scores[:3]
            }
            segment_data[5] = segment_answers_data[5]  # Education data
            
            # Employment (becomes segment 6)
            subtotals[6] = sum(segment_scores[3:])
            segment_answers[6] = {
                'questions': segment_questions[5][3:],
                'scores': segment_scores[3:]
            }
            # Create new employment data from second half of segment 5
            segment_data[6] = {
                k-3: segment_answers_data[5][k] 
                for k in range(3, 6)
            }
            
            total_score += sum(segment_scores)
        elif i < 5:  # Segments 1-4 stay the same
            subtotal = sum(segment_scores)
            subtotals[i] = subtotal
            total_score += subtotal
            segment_answers[i] = {
                'questions': segment_questions[i],
                'scores': segment_scores
            }
            segment_data[i] = segment_answers_data[i]
        else:  # Segments 6-8 become 7-9
            subtotal = sum(segment_scores)
            subtotals[i+1] = subtotal
            total_score += subtotal
            segment_answers[i+1] = {
                'questions': segment_questions[i],
                'scores': segment_scores
            }
            segment_data[i+1] = segment_answers_data[i]
    
    length_of_sentence = session.get('length_of_sentence', '2-years-or-less')
    risk_assessment = assess_risk_level(total_score, length_of_sentence)
    
    # Determine recommended programs
    recommended_programs = []
    for segment_id, data in segment_thresholds.items():
        if subtotals.get(segment_id, 0) >= data["threshold"]:
            program_name = f"{data['program']} ({data.get('name', segment_titles.get(segment_id, ''))})"
            recommended_programs.append(program_name)
    
    # Calculate education and employment scores
    education_score, employment_score = calculate_split_scores(segment_answers)
    
    # Render the PDF template
    html = render_template(
        'pdf_template copy.html',
        subtotals=subtotals,
        total_score=total_score,
        risk_assessment=risk_assessment,
        recommended_programs=recommended_programs,
        mandatory_programs=mandatory_programs,
        segment_titles=segment_titles,
        segment_answers=segment_answers,
        segment_thresholds=segment_thresholds,
        length_of_sentence=length_of_sentence,
        client_name=session.get('client_name', ''),
        officer_name=session.get('officer_name', ''),
        chief_name=session.get('chief_name', ''),
        date=datetime.now().strftime("%B %d, %Y"),
        segment_answers_data=segment_data,  # Pass the remapped data
        education_score=education_score,
        employment_score=employment_score
    )
    
    # Convert the HTML to a PDF
    pdf = HTML(string=html).write_pdf()
    
    return send_file(
        BytesIO(pdf),
        download_name='risk_assessment_results.pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)