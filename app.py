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
    return render_template('homepg.html')

@app.route('/ui')
def ui():
    return render_template('ui.html')

# Categories route
@app.route('/categories')
def categories():
    predefined_categories = ['shirt', 'pant', 'hat', 'shoes', 'dress', 'jacket', 'glasses', 'bag', 'watch', 'scarf','temporary']
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

@app.route('/upload_temp', methods = ['POST'])
def upload_temp():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        file_data = file.read()

        category = 'temporary'  # Use your actual ML model to classify the image

        new_image = Image(data=file_data, filename=file.filename, category=category)
        db.session.add(new_image)
        db.session.commit()

        # return redirect(url_for('upload'))
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

# Route to view favorite images
@app.route('/favorites')
def view_favorites():
    favorites = Image.query.filter_by(is_favorite=True).all()  # Fetch favorite images
    return render_template('favorites.html', images=favorites)

# Route to view disliked images
@app.route('/dislikes')
def view_dislikes():
    dislikes = Image.query.filter_by(is_disliked=True).all()  # Fetch disliked images
    return render_template('dislikes.html', images=dislikes)

@app.route('/favorites/<int:image_id>', methods=['POST'])
def favorite_image(image_id):
    image = Image.query.get_or_404(image_id)
    image.is_favorite = True
    db.session.commit()
    return 'Image added to favorites.'

@app.route('/dislikes/<int:image_id>', methods=['POST'])
def dislike_image(image_id):
    image = Image.query.get_or_404(image_id)
    image.is_disliked = True
    db.session.commit()
    return 'Image marked as disliked.'

@app.route('/remove_dislike/<int:image_id>', methods=['POST'])
def remove_dislike(image_id):
    image_to_remove = Image.query.get_or_404(image_id)
    try:
        image_to_remove.is_disliked = False
        db.session.commit()
        return 'Image removed from dislike list successfully.'
    except:
        db.session.rollback()
        return 'There was a problem removing the image from the dislike list.'

@app.route('/remove_favorite/<int:image_id>', methods=['POST'])
def remove_favorite(image_id):
    image_to_remove = Image.query.get_or_404(image_id)
    try:
        image_to_remove.is_favorite = False
        db.session.commit()
        return 'Image removed from favorite list successfully.'
    except:
        db.session.rollback()
        return 'There was a problem removing the image from the favorite list.'


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




















#  uploading










# Running the application
if __name__ == '__main__':
    app.run(debug=True)
