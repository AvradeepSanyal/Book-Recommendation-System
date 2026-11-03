# 📚 Book Recommendation System

A Flask web app that helps readers discover their next book. It shows the **Top 50 most popular books** and gives **personalised recommendations** using item-based collaborative filtering with cosine similarity, trained on the Book-Crossing dataset.

## Features

- **Top 50 books** ranked by average rating, among books with at least 250 ratings
- **Similar-book recommendations**: enter a book title and get 4 similar books with cover, title, and author
- **Friendly error handling** when a title isn't in the database
- **Responsive UI** built with Bootstrap 3 and Jinja2 templates
- **Pre-computed models** (pickle files) so the app starts quickly and needs no training at runtime

## How It Works

### 1. Popularity-based recommendations
Ratings are merged with book metadata, then grouped by title to compute the number of ratings and the average rating. Only books with **250 or more ratings** are kept, and the **top 50 by average rating** are shown on the home page.

### 2. Collaborative filtering (item-based)
1. Keep only **active users** (more than 200 ratings) and **well-rated books** (at least 50 ratings from those users).
2. Build a pivot table: books as rows, users as columns, ratings as values (missing values filled with 0).
3. Treat each book as a vector in user-rating space and compute pairwise **cosine similarity**.
4. For a chosen book, return the books with the highest similarity scores (excluding the book itself).

## Tech Stack

| Area | Tools |
|------|-------|
| Language | Python |
| Web framework | Flask |
| Data / ML | pandas, NumPy, scikit-learn |
| Frontend | HTML, Jinja2, Bootstrap 3 |
| Model storage | Pickle (`.pkl`) |

## Project Structure

```
Book-Recommendation-System/
├── app.py                          # Flask application (routes + recommendation logic)
├── book-recommender-system.ipynb   # Data analysis, model building, and pickle export
├── requirements.txt                # Python dependencies
├── popular.pkl                     # Top 50 popular books
├── pt.pkl                          # Pivot table (books × users)
├── books.pkl                       # Book metadata (title, author, image URL)
├── similarity_scores.pkl           # Pre-computed cosine similarity matrix
├── datasets used/
│   ├── Books.csv
│   ├── Ratings.csv
│   └── Users.csv
└── templates/
    ├── index.html                  # Home page (Top 50 books)
    └── recommend.html              # Recommendation page
```

## Dataset

This project uses the [Book-Crossing dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset), which contains:

| File | Contents |
|------|----------|
| `Books.csv` | ~271K books: ISBN, title, author, year, publisher, cover image URLs |
| `Ratings.csv` | ~1.15M ratings: user ID, ISBN, rating |
| `Users.csv` | ~279K users: user ID, location, age |

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/AvradeepSanyal/Book-Recommendation-System.git
cd Book-Recommendation-System

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Usage

1. **Home page (`/`)**: browse the Top 50 books with cover, author, number of votes, and average rating.
2. **Recommend page (`/recommend`)**: type the exact title of a book (for example `1984`) and submit to see 4 similar books.

> **Tip:** Title matching is exact and case-sensitive, and only books that passed the filtering step (about 700 popular books) are searchable.

## Retraining the Model

To rebuild the pickle files from the raw data:

1. Open `book-recommender-system.ipynb` (Jupyter Notebook or JupyterLab).
2. Make sure the three CSV files are accessible (the notebook expects them in the working directory).
3. Run all cells. The last cells regenerate `popular.pkl`, `pt.pkl`, `books.pkl`, and `similarity_scores.pkl`.

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with the Top 50 books |
| `/recommend` | GET | Recommendation search page |
| `/recommend_books` | POST | Returns 4 recommendations for the submitted title |

## Possible Improvements

- Case-insensitive and fuzzy title search, or autocomplete suggestions
- Hybrid approach combining content-based and collaborative filtering
- Handle cold-start users and books outside the filtered set
- Deploy to a hosting platform (Render, Railway, Heroku, etc.)

## Contributing

Contributions are welcome. Fork the repo, create a feature branch, and open a pull request.

## License

Add a license of your choice (for example, [MIT](https://choosealicense.com/licenses/mit/)) and mention it here.

## Acknowledgements

- [Book-Crossing dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
- [Flask](https://flask.palletsprojects.com/) and [scikit-learn](https://scikit-learn.org/)
