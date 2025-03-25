from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz, process
import csv
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///faq.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# Hardcoded Admin Credentials
ADMINS = {
    "anand_srivastava": "anand123",
    "mohini_khattri": "mohini123"
}

# FAQ Model
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

# Ensure Database is Created
with app.app_context():
    db.create_all()

# Home Page (Chatbot)
@app.route('/')
def home():
    return render_template('index.html')

# Function to get best matching response
def get_best_match(user_message):
    faqs = FAQ.query.all()
    questions = {faq.question: faq.answer for faq in faqs}

    if not questions:
        return "No FAQs available. Please ask the admin to add some."

    best_match, score = process.extractOne(user_message, questions.keys(), scorer=fuzz.ratio)

    if score > 50:
        return questions[best_match]
    else:
        return "Sorry, I don't have an answer for that. You can ask the admin."

# Chatbot API (Fetch Answer)
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message'].strip().lower()
    if not user_message:
        return jsonify({'response': "Please ask a valid question."})
    response = get_best_match(user_message)
    return jsonify({'response': response})

# Admin Login Page
@app.route('/admin')
def admin_login():
    return render_template('login.html')

# Admin Authentication
@app.route('/admin_login', methods=['POST'])
def admin_authenticate():
    username = request.form['username']
    password = request.form['password']
    
    if username in ADMINS and ADMINS[username] == password:
        session['admin'] = username  # Store the logged-in admin username
        return redirect('/dashboard')
    else:
        return render_template('login.html', error="Invalid Credentials! Try again.")

# Admin Dashboard
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/admin')
    faqs = FAQ.query.all()
    return render_template('dashboard.html', faqs=faqs)

# Add FAQ
@app.route('/add_faq', methods=['POST'])
def add_faq():
    if 'admin' not in session:
        return redirect('/admin')
    
    question = request.form['question'].strip()
    answer = request.form['answer'].strip()
    if not question or not answer:
        return redirect('/dashboard')

    new_faq = FAQ(question=question, answer=answer)
    db.session.add(new_faq)
    db.session.commit()
    return redirect('/dashboard')

# ✅ Edit FAQ
@app.route('/edit_faq/<int:id>', methods=['GET', 'POST'])
def edit_faq(id):
    if 'admin' not in session:
        return redirect('/admin')
    
    faq = FAQ.query.get(id)
    if request.method == 'POST':
        faq.question = request.form['question'].strip()
        faq.answer = request.form['answer'].strip()
        db.session.commit()
        return redirect('/dashboard')

    return render_template('edit_faq.html', faq=faq)

# Delete FAQ
@app.route('/delete_faq/<int:id>')
def delete_faq(id):
    if 'admin' not in session:
        return redirect('/admin')
    
    faq = FAQ.query.get(id)
    if faq:
        db.session.delete(faq)
        db.session.commit()
    
    return redirect('/dashboard')

# ✅ CSV Upload (Replace Old FAQs with New CSV Data)
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'admin' not in session:
        return redirect('/admin')

    if 'csv_file' not in request.files:
        return redirect('/dashboard')

    file = request.files['csv_file']
    
    if file.filename == '':
        return redirect('/dashboard')

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 🔥 पुराना डेटा डिलीट करें
    FAQ.query.delete()
    db.session.commit()

    # ✅ नया डेटा अपलोड करें
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  # हेडर को स्किप करें
        for row in reader:
            if len(row) >= 2:
                question, answer = row[:2]
                new_faq = FAQ(question=question.strip(), answer=answer.strip())
                db.session.add(new_faq)

    db.session.commit()

    return redirect('/dashboard')

# ✅ CSV Download (Export FAQs)
@app.route('/download_csv')
def download_csv():
    if 'admin' not in session:
        return redirect('/admin')

    faqs = FAQ.query.all()
    csv_filepath = os.path.join(UPLOAD_FOLDER, "faqs_export.csv")

    with open(csv_filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Question", "Answer"])  # Header Row
        for faq in faqs:
            writer.writerow([faq.question, faq.answer])

    return send_file(csv_filepath, as_attachment=True)

# Logout Admin
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
