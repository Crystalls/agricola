from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)

# обращение и подколючение к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog1.db'
# отключение функции, чтобы не возникали ошибки
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# создание объекта на основе базы данных
db = SQLAlchemy(app)
moment = Moment(app)


# создание класса с таблицей базы данных
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, primary_key=False)
    intro = db.Column(db.String(200), nullable=False, primary_key=False)
    text = db.Column(db.Text, nullable=False, primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # функция которая выдет объект из базы данных и его id
    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('html/main.html', content='<img src="static/img/bg1.jpg" alt="">')


@app.route('/download')
def download():
    return render_template('html/download.html', content='<img src ="static/img/bg1.jpg" alt"">')


@app.route('/faq')
def about():
    return render_template('html/FAQ.html', content='<img src ="static/img/bg1.jpg" alt"">')


@app.route('/wiki')
def wiki():
    return render_template('html/wiki.html', content='<img src ="static/img/bg1.jpg" alt"">')


@app.route('/blog')
def blog():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('html/blog.html', content='<img src ="static/img/bg1.jpg" alt"">', articles=articles)


@app.route('/blogadm')
def blogadm():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('html/blogadm.html', content='<img src ="static/img/bg1.jpg" alt"">', articles=articles)


@app.route('/posts/<int:id>')
def posts(id):
    article = Article.query.get(id)
    return render_template('html/posts.html', content='<img src ="static/img/bg1.jpg" alt"">', article=article)


@app.route('/posts/<int:id>/delete')
def posts_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/blog')
    except:
        return 'При удалении статьи произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def posts_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/blog')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template('html/post_update.html', article=article)


@app.route('/create-article', methods=['POST', 'GET'])  # получение данных при помощи POST
def ca():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/blog')

        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('html/create-article.html')


if __name__ == '__main__':
    app.run(debug=True)
