import csv
from io import StringIO
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify


app = Flask(__name__)

# Define the grid cells and their initial colors
grid_cells = {
    'A1': 'light-grey',
    'A2': 'yellow',
    'A3': 'blue',
    'A4': 'green',
    'A5': 'red',
    'A6': 'yellow',
    'A7': 'blue',
    'A8': 'green',
    'A9': 'light-grey',
    'B1': 'red',
    'B2': 'yellow',
    'B3': 'blue',
    'B4': 'green',
    'B5': 'yellow',
    'B6': 'yellow',
    'B7': 'blue',
    'B8': 'green',
    'B9': 'red',
    'C1': 'green',
    'C2': 'yellow',
    'C3': 'blue',
    'C4': 'green',
    'C5': 'green',
    'C6': 'yellow',
    'C7': 'blue',
    'C8': 'green',
    'C9': 'yellow',
    'D1': 'blue',
    'D2': 'yellow',
    'D3': 'blue',
    'D4': 'green',
    'D5': 'green',
    'D6': 'yellow',
    'D7': 'blue',
    'D8': 'green',
    'D9': 'blue',
    'E1': 'yellow',
    'E2': 'blue',
    'E3': 'green',
    'E4': 'red',
    'E5': 'light-grey',
    'E6': 'yellow',
    'E7': 'yellow',
    'E8': 'red',
    'E9': 'green',
    'F1': 'red',
    'F2': 'yellow',
    'F3': 'blue',
    'F4': 'green',
    'F5': 'red',
    'F6': 'yellow',
    'F7': 'blue',
    'F8': 'green',
    'F9': 'red',
    'G1': 'red',
    'G2': 'yellow',
    'G3': 'blue',
    'G4': 'green',
    'G5': 'red',
    'G6': 'yellow',
    'G7': 'blue',
    'G8': 'green',
    'G9': 'yellow',
    'H1': 'green',
    'H2': 'yellow',
    'H3': 'blue',
    'H4': 'green',
    'H5': 'green',
    'H6': 'yellow',
    'H7': 'blue',
    'H8': 'green',
    'H9': 'blue',
    'I1': 'light-grey',
    'I2': 'yellow',
    'I3': 'red',
    'I4': 'green',
    'I5': 'blue',
    'I6': 'yellow',
    'I7': 'red',
    'I8': 'green',
    'I9': 'light-grey',
}

players = [
    {"name": "a", "color": "red", "x": 5, "y": 5},
    {"name": "b", "color": "blue", "x": 5, "y": 5},
    {"name": "c", "color": "green", "x": 5, "y": 5},
    {"name": "d", "color": "yellow", "x": 5, "y": 5}
]
# List of hardcoded questions and answers
questions = [
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    # Add more questions as needed
]


# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trivial.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Player model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('questions', lazy=True))
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    flagged = db.Column(db.Boolean, default=False, nullable=False)  # Add the flagged column



# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_players', methods=['GET'])
def get_players():
    players = Player.query.all()
    player_data = [{'name': player.name, 'color': player.color} for player in players]
    return jsonify(player_data)

@app.route('/grid_cells', methods=['GET'])
def get_grid_cells():
    grid = [{'cell_id': cell_id, 'color': grid_cells[cell_id]} for cell_id in grid_cells]
    return jsonify(grid)

@app.route('/update_cell', methods=['POST'])
def update_cell():
    cell_id = request.form['cell_id']
    color = request.form['color']
    grid_cells[cell_id] = color
    return jsonify({'message': 'Cell color updated successfully'})

@app.route('/move_player', methods=['POST'])
def move_player():
    global players

    # Get the chosen direction and number of steps from the form data
    direction = request.form['direction']
    steps = int(request.form['steps'])

    # Update the player's position based on the chosen direction and steps
    player = players[current_player_index]
    if direction == 'up':
        player['y'] = max(1, player['y'] - steps)
    elif direction == 'down':
        player['y'] = min(9, player['y'] + steps)
    elif direction == 'left':
        player['x'] = max(1, player['x'] - steps)
    elif direction == 'right':
        player['x'] = min(9, player['x'] + steps)

    return jsonify({'message': 'Player position updated successfully'})


@app.route('/players', methods=['GET', 'POST'])
def players():
    if request.method == 'POST':
        with app.app_context():
            players = []
            for i in range(1, 5):
                player_name = request.form.get(f'player{i}')
                player_color = request.form.get(f'player{i}_color')

                if player_name:
                    player = Player(name=player_name, color=player_color)
                    db.session.add(player)
                    players.append(player)
            
            db.session.commit()
            
            return render_template('players.html', players=players)
    else:
        with app.app_context():
            players = Player.query.all()
            return render_template('players.html', players=players)

@app.route('/edit_players', methods=['GET', 'POST'])
def edit_players():
    with app.app_context():
        if request.method == 'POST':
            players = []
            for i in range(1, 5):
                player_id = request.form.get(f'player{i}_id')
                player_name = request.form.get(f'player{i}')
                player_color = request.form.get(f'player{i}_color')

                if player_id:
                    player = Player.query.get(player_id)
                    player.name = player_name
                    player.color = player_color
                    db.session.commit()
                    players.append(player)

            return render_template('edit_players.html', players=players)
        else:
            players = Player.query.all()
            return render_template('edit_players.html', players=players)

@app.route('/qa', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        with app.app_context():
            category1 = request.form['category1']
            category2 = request.form['category2']
            category3 = request.form['category3']
            category4 = request.form['category4']

            categories = [
                {'name': category1},
                {'name': category2},
                {'name': category3},
                {'name': category4}
            ]

            # Save categories to the database
            for category in categories:
                new_category = Category(name=category['name'])
                db.session.add(new_category)
            db.session.commit()

            return render_template('qa.html', categories=categories)
    else:
        with app.app_context():
            categories = Category.query.all()
            questions = Question.query.all()
            return render_template('qa.html', categories=categories, questions=questions)


@app.route('/add_qa', methods=['POST'])
def add_qa():
    with app.app_context():
        category_id = request.form['category_id']
        question = request.form['question']
        answer = request.form['answer']
        flagged = 'flagged' in request.form  # Check if the 'flagged' checkbox is present in the form data

        new_question = Question(category_id=category_id, question=question, answer=answer, flagged=flagged)
        db.session.add(new_question)
        db.session.commit()

        return jsonify({'message': 'QA submitted successfully'})



@app.route('/update_question', methods=['POST'])
def update_question():
    with app.app_context():
        question_id = request.form['id']
        question_text = request.form['question']
        flagged = request.form.get('flagged', False) == 'true'  # Get the flagged status from the form

        question = Question.query.get(question_id)
        question.question = question_text
        question.flagged = flagged  # Update the flagged status
        db.session.commit()

        return jsonify({'message': 'Question updated successfully'})


@app.route('/update_answer', methods=['POST'])
def update_answer():
    with app.app_context():
        question_id = request.form['id']
        answer_text = request.form['answer']

        question = Question.query.get(question_id)
        question.answer = answer_text
        db.session.commit()

        return jsonify({'message': 'Answer updated successfully'})

@app.route('/delete_question', methods=['POST'])
def delete_question():
    with app.app_context():
        question_id = request.form['id']

        question = Question.query.get(question_id)
        db.session.delete(question)
        db.session.commit()

        return jsonify({'message': 'Question deleted successfully'})

@app.route('/delete_category', methods=['POST'])
def delete_category():
    with app.app_context():
        category_id = request.form['id']

        category = Category.query.get(category_id)
        db.session.delete(category)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully'})

@app.route('/update_category', methods=['POST'])
def update_category():
    category_id = request.form['id']
    name = request.form['name']
    category = Category.query.get(category_id)
    category.name = name
    db.session.commit()
    return jsonify({'message': 'Category updated successfully'})

@app.route('/delete_player', methods=['POST'])
def delete_player():
    with app.app_context():
        player_id = request.form['id']

        player = Player.query.get(player_id)
        db.session.delete(player)
        db.session.commit()

        return jsonify({'message': 'Player deleted successfully'})
    
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    csv_file = request.files['csv-file']
    if csv_file:
        stream = StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
        csv_data = csv.reader(stream)
        next(csv_data)  # Skip the header row
        
        for row in csv_data:
            question_text = row[0]
            answer_text = row[1]
            category_name = row[2]
            flagged = row[3] == 'flagged'

            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

            question = Question(question=question_text, answer=answer_text, flagged=flagged)
            question.category = category
            db.session.add(question)
            db.session.commit()

        return jsonify({'message': 'CSV file uploaded successfully'})

    return jsonify({'message': 'No CSV file provided'})

@app.route('/submit_players', methods=['POST'])
def submit_players():
    player_form = PlayerForm()

    if player_form.validate_on_submit():
        # Get the player names and colors from the form
        player1_name = player_form.player1_name.data
        player1_color = player_form.player1_color.data
        player2_name = player_form.player2_name.data
        player2_color = player_form.player2_color.data
        player3_name = player_form.player3_name.data
        player3_color = player_form.player3_color.data
        player4_name = player_form.player4_name.data
        player4_color = player_form.player4_color.data

        # Create Player objects and save them to the database
        player1 = Player(name=player1_name, color=player1_color)
        player2 = Player(name=player2_name, color=player2_color)
        player3 = Player(name=player3_name, color=player3_color)
        player4 = Player(name=player4_name, color=player4_color)

        db.session.add_all([player1, player2, player3, player4])
        db.session.commit()

        # Get all players from the database
        players = Player.query.all()

        # Pass the players' information to the index.html template
        return render_template('index.html', players=players)
    
    flash('Please fill in all player names and colors.')
    return redirect(url_for('players'))

@app.route('/question')
def question():
    # Retrieve the question and answer from the query parameters or request data
    question_text = request.args.get('question')
    answer = request.args.get('answer')

    return render_template('question.html', question=question_text, answer=answer)


@app.route('/check_answer', methods=['POST'])
def check_answer():
    # Retrieve the player's answer from the form submission
    player_answer = request.form['player_answer']

    # Retrieve the correct answer from the form data or other source
    correct_answer = request.form['correct_answer']

    # Check if the answer is correct
    is_correct = player_answer.lower() == correct_answer.lower()

    # Prepare the response to send back to the client
    response = {
        'is_correct': is_correct
    }

    return jsonify(response)

@app.route('/manual')
def manual():
    return render_template('manual.html')

    
# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
