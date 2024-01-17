from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace 'YOUR_GIPHY_API_KEY' with your actual Giphy API key
GIPHY_API_KEY = 'IaND2UXC2UpLSA5zyPDPbSZUDGEPHJqN'
GIPHY_API_URL = 'https://api.giphy.com/v1/gifs/random'


@app.route('/get_gif')
def get_random_gif():
    params = {
        'api_key': GIPHY_API_KEY,
        'tag': '8bit pastel animated',
        'rating': 'g',  # You can adjust the rating based on your preference
    }

    try:
        response = requests.get(GIPHY_API_URL, params=params)
        data = response.json()

        if 'data' in data and 'images' in data['data']:
            gif_url = data['data']['images']['original']['webp']
            return jsonify({'gif_url': gif_url})

    except Exception as e:
        print(f"Error fetching Giphy API: {e}")

    return jsonify({'error': 'Failed to fetch a random 8-bit GIF'})


def calculate_cgpa(grades, credit_hours):
    total_credit_points = 0
    total_credits = 0

    for grade, credit in zip(grades, credit_hours):
        if grade == 'A':
            grade_point = 4.0
        elif grade == 'A-':
            grade_point = 3.7
        elif grade == 'B+':
            grade_point = 3.3
        elif grade == 'B':
            grade_point = 3.0
        elif grade == 'B-':
            grade_point = 2.7
        elif grade == 'C+':
            grade_point = 2.3
        elif grade == 'C':
            grade_point = 2.0
        elif grade == 'C-':
            grade_point = 1.7
        elif grade == 'D+':
            grade_point = 1.3
        elif grade == 'D':
            grade_point = 1.0
        else:
            grade_point = 0.0

        total_credit_points += grade_point * credit
        total_credits += credit

    if total_credits == 0:
        return 0.0
    else:
        cgpa = total_credit_points / total_credits
        return round(cgpa, 2)


@app.route('/')
def index():
    num_courses = 3
    return render_template('index.html', num_courses=num_courses)


@app.route('/calculate', methods=['POST'])
def calculate():
    current_cgpa = float(request.form['current_cgpa'])
    completed_credit_hours = float(request.form['completed_credit_hours'])

    num_courses = int(request.form['num_courses'])

    grades = []
    credit_hours = []

    for i in range(num_courses):
        grade = request.form[f'grade_{i}']
        credit = float(request.form[f'credit_{i}'])

        grades.append(grade)
        credit_hours.append(credit)

    total_credit_hours = completed_credit_hours + sum(credit_hours)
    total_cgpa_points = current_cgpa * completed_credit_hours

    cgpa = calculate_cgpa(grades, credit_hours)
    new_cgpa_points = cgpa * sum(credit_hours)

    estimated_cgpa = (total_cgpa_points + new_cgpa_points) / total_credit_hours

    return render_template('result.html', estimated_cgpa=round(estimated_cgpa, 2))


if __name__ == '__main__':
    app.run(debug=True)
