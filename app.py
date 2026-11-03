from flask import Flask, render_template, request
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

popular_df = pickle.load(open(os.path.join(BASE_DIR, 'popular.pkl'), 'rb'))
pt = pickle.load(open(os.path.join(BASE_DIR, 'pt.pkl'), 'rb'))
books = pickle.load(open(os.path.join(BASE_DIR, 'books.pkl'), 'rb'))
similarity_scores = pickle.load(open(os.path.join(BASE_DIR, 'similarity_scores.pkl'), 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_rating'].to_list()
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')

    # 1. Check if the book actually exists in the index to prevent the IndexError
    if user_input not in pt.index:
        error_message = f"Sorry, '{user_input}' was not found in our database. Please check your spelling or try another book!"
        return render_template('recommend.html', error=error_message)

    # 2. If it does exist, run the recommendation algorithm safely
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].to_list())
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].to_list())

        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
