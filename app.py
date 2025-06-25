from flask import Flask, jsonify, request

app = Flask(__name__)


books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho"},
    {"id": 2, "title": "1984", "author": "George Orwell"}
]


@app.route('/')
def home():
    return "Welcome to the Book API!"


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    return jsonify(book) if book else ("Book not found", 404)


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_id = max([b['id'] for b in books], default=0) + 1
    new_book = {
        "id": new_id,
        "title": data['title'],
        "author": data['author']
    }
    books.append(new_book)
    return jsonify(new_book), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    for book in books:
        if book['id'] == book_id:
            book['title'] = data.get('title', book['title'])
            book['author'] = data.get('author', book['author'])
            return jsonify(book)
    return ("Book not found", 404)


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return ("", 204)

if __name__ == '__main__':
    app.run(debug=True)
