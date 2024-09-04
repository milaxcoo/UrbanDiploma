from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Quote {self.id} - {self.author}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    quotes = Quote.query.all()
    return render_template('quote_list.html', quotes=quotes)

@app.route('/add', methods=['GET', 'POST'])
def add_quote():
    if request.method == 'POST':
        text = request.form['text']
        author = request.form['author']
        new_quote = Quote(text=text, author=author)
        db.session.add(new_quote)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_quote.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_quote(id):
    quote = Quote.query.get_or_404(id)
    if request.method == 'POST':
        quote.text = request.form['text']
        quote.author = request.form['author']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_quote.html', quote=quote)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_quote(id):
    quote = Quote.query.get_or_404(id)
    db.session.delete(quote)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
