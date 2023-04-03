from flask import Flask , render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite' #/// -> relative path
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False
db=SQLAlchemy(app)

class ToDo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean)

@app.route('/')
def index():
    # show all todos
    todo_list=ToDo.query.all()
    print(todo_list)
    return render_template('base.html',todo_list=todo_list)

# route
@app.route('/add',methods=["POST"])
def add():
    # add new item
    title=request.form.get("title")
    new_todo=ToDo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # update
    todo=ToDo.query.filter_by(id=todo_id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete
    todo=ToDo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.create_all()
    app.run(host="127.0.0.1",port=5001, debug=True)
