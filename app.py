from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import base64


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///category.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# define image model
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary, nullable=False)  
    filename = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Category field for predefined categories
    is_favorite = db.Column(db.Boolean, default=False)
    is_disliked = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

# Home route
@app.route('/')
def index():
    return render_template('ui.html')

# Categories route
@app.route('/categories')
def categories():
    predefined_categories = ['shirt', 'pant', 'hat', 'shoes', 'dress', 'jacket', 'glasses', 'bag', 'watch', 'scarf']
    return render_template('categories.html', categories=predefined_categories)

# Dynamic route to view images by category
@app.route('/category/<string:category_name>')
def view_category(category_name):
    images = Image.query.filter_by(category=category_name).all()  # Fetch images based on category
    return render_template('view_category.html', category=category_name, images=images)

# Upload page route
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        # Read the image file as binary data
        file_data = file.read()

        # Run the image through the ML model to determine the category
        category = classify_image(file_data)  # Use your actual ML model to classify the image

        # Store the binary data, filename, and category in the database
        new_image = Image(data=file_data, filename=file.filename, category=category)
        db.session.add(new_image)
        db.session.commit()

        return redirect(url_for('categories'))
    return render_template('upload.html')

@app.route('/upload/<string:category>', methods=['POST'])
def upload_image(category):
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    # Read the image file as binary data
    file_data = file.read()

    # Store the binary data, filename, and category in the database
    new_image = Image(data=file_data, filename=file.filename, category=category)
    db.session.add(new_image)
    db.session.commit()

    return redirect(url_for('view_category', category_name=category))


# Simulated ML model function for classifying images into predefined categories
def classify_image(image_data):
    # Replace this with actual ML model logic
    predefined_categories = ['shirt', 'pant', 'hat', 'shoes', 'dress', 'jacket', 'glasses', 'bag', 'watch', 'scarf']

    # Simulate categorization (you can replace this with real logic)
    return 'dress'  # For now, always return 'shirt' as the category

# Route to mark an image as favorite
@app.route('/favorite/<int:image_id>', methods=['POST'])
def favorite_image(image_id):
    image = Image.query.get_or_404(image_id)
    try:
        image.is_favorite = True
        db.session.commit()
        return 'Image added to favorites.'
    except:
        db.session.rollback()
        return 'Failed to favorite the image.'

# Route to mark an image as disliked
@app.route('/dislike/<int:image_id>', methods=['POST'])
def dislike_image(image_id):
    image = Image.query.get_or_404(image_id)
    try:
        image.is_disliked = True
        db.session.commit()
        return 'Image marked as disliked.'
    except:
        db.session.rollback()
        return 'Failed to mark the image as disliked.'

@app.route('/delete/<int:image_id>', methods=['POST'])
def delete_image(image_id):
    # Query the database to find the image by its ID
    image_to_delete = Image.query.get_or_404(image_id)

    try:
        # Remove the image from the database
        db.session.delete(image_to_delete)
        db.session.commit()
        return 'Image deleted successfully.'
    except:
        # Handle any issues during the delete operation
        db.session.rollback()
        return 'There was a problem deleting the image.'
# Running the application
if __name__ == '__main__':
    app.run(debug=True)
