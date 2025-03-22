from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Database Models
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    video_id = db.Column(db.String(20), unique=True, nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(20), db.ForeignKey('video.video_id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# Route to display video page
@app.route('/video/<video_id>', methods=['GET', 'POST'])
def video_page(video_id):
    video = Video.query.filter_by(video_id=video_id).first()
    comments = Comment.query.filter_by(video_id=video_id).all()

    if request.method == 'POST':
        username = request.form.get('username')
        comment_text = request.form.get('comment_text')

        if username and comment_text:
            new_comment = Comment(video_id=video_id, username=username, comment_text=comment_text)
            db.session.add(new_comment)
            db.session.commit()

        return redirect(url_for('video_page', video_id=video_id))

    return render_template('page.html', video=video, comments=comments)

# Homepage - List All Videos
@app.route('/')
def home():
    videos = Video.query.all()
    return render_template('base.html', videos=videos)

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
