from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pickle

# Load the pre-trained model
model = pickle.load(open('clf.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database functions (replace with your actual database implementation)
def get_user(email):
    # Replace this with your database query logic
    return None

def verify_password(user, password):
    # Replace this with your password verification logic
    return False

def insert_user(username, mobile, email, password):
    # Replace this with your database insertion logic
    pass

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = get_user(email)

        if verify_password(user, password):
            # Store user in the session
            session['user'] = email
            return redirect(url_for('predict_disease'))
        else:
            return 'Invalid username or password.'
    return render_template('login.html')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        username = request.form['name']
        phone = request.form['mobile']

        if password != confirm_password:
            return 'Password and Confirm Password do not match.'

        existing_user = get_user(email)
        if existing_user:
            return 'Email address is already registered.'

        # Create a new user
        insert_user(username=username, mobile=phone, email=email, password=password)

        # Redirect to login page after successful signup
        return redirect(url_for('login'))
    return render_template('signup.html')

# Predictor Page
@app.route('/predictor', methods=['GET', 'POST'])
def predict_disease():
    if request.method == 'POST':
        # Extract form data
        age = int(request.form.get('age'))
        gender = int(request.form.get('gender'))
        cp = int(request.form.get('cp'))
        trestbps = int(request.form.get('trestbps'))
        chol = int(request.form.get('chol'))
        fasting_blood_sugar = int(request.form.get('fasting_blood_sugar'))
        ecg = int(request.form.get('ecg'))
        thalach = int(request.form.get('thalach'))
        exang = int(request.form.get('exang'))
        oldpeak = float(request.form.get('oldpeak'))
        slope = int(request.form.get('slope'))
        ca = int(request.form.get('ca'))
        thal = int(request.form.get('thal'))

        # Prepare input features for the model
        final_features = np.array(
            [age, gender, cp, trestbps, chol, fasting_blood_sugar, ecg, thalach, exang, oldpeak, slope, ca, thal]
        ).reshape(1, -1)

        # Make prediction
        prediction = model.predict(final_features)
        result = "You have a heart disease." if prediction[0] == 1 else "You do not have a heart disease."

        # Render the result page
        return render_template('output.html', result=result)
    return render_template('predictor.html')

# Logout Route
@app.route('/logout')
def logout():
    # Clear the session
    session.pop('user', None)
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)