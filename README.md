# SmartWardrobe

This Flask application allows users to upload images, categorize them using a machine learning model, and manage their wardrobe items. Users can view their uploaded images by category, mark items as favorites or dislikes, and manage wear counts for their items.

## Features

- **Image Upload**: Users can upload images along with a name and automatically classify them into predefined categories.
- **Category Management**: Users can view images sorted by category.
- **Favorites & Dislikes**: Users can mark images as favorites or dislikes.
- **Wear Count Tracking**: Users can track how often they wear specific items.
- **Recent Items Overview**: View recently uploaded images and statistics about the wardrobe.

## Technologies Used

- **Flask**: Web framework for building the application.
- **Keras**: Machine learning library for loading and predicting image categories.
- **SQLite**: Lightweight database for storing image metadata.
- **PIL (Pillow)**: Library for image processing.

## Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Spandana-M-Patil/Hackathon.git
   cd Hackathon
   ```
2. **Install dependencies**
   Make sure you have Python 3.x installed, then create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Download and Place the Model:**
Ensure your trained Keras model file (my_model.h5) is placed in the Model directory within the project root.
4. Initialize the Database:
The application will automatically create the database (category.db) on the first run in a instance folder.
5. Run the Application:
   ```bash
   python app.py
   ```
   Open your browser and navigate to http://127.0.0.1:5000 to access the application.
   
## Usage
**Upload Images:** Navigate to the upload page, select an image, and fill in the image name.
**View Categories:** Click on categories to view all images within that category.
**Manage Favorites and Dislikes:** Users can mark images as favorites or dislikes from the image view pages.
**Track Wear Count:** Mark items as worn to increase their wear count.

