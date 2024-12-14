from flask import Flask , render_template , request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)  # Use utcnow for consistency
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    try:
        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            desc = request.form.get('desc', '').strip()

            # Validate fields
            if not title:
                error = "Both Title and Description are required."
                allTodo = Todo.query.all()  # Fetch todos for re-rendering
                return render_template('index.html', allTodo=allTodo, error=error)

            # Add todo to the database
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()

            return redirect(url_for('hello_world'))

        # Fetch todos for GET request
        allTodo = Todo.query.all()

    except Exception as e:
        print(f"An error occurred: {e}")
        allTodo = []
        return render_template('index.html', allTodo=allTodo, error="An error occurred while processing your request.")

    return render_template('index.html', allTodo=allTodo)


@app.route('/update/<int:sno>')
def update(sno):
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'


@app.route('/delete/<int:sno>')
def delete(sno):
    todo= Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))





if __name__ == "__main__":
    app.run(debug=True)