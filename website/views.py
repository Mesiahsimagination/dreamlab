from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Video
from . import db

from pytube import YouTube
from pathlib import Path

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        date = request.form.get("date")

        if "youtube.com/" not in url:
            flash("Video URL is not valid.", category="error")
        else:
            yt = YouTube(url)
            yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            downloads_path = str(Path.home() / "Downloads")
            print(downloads_path)
            yt.download(downloads_path)

            if current_user.is_authenticated:
                new_video = Video(title=yt.title, url=url, date=date, user_id=current_user.id)
                db.session.add(new_video)
                db.session.commit()
            
            flash("Video converted successfully!", category="success")
        
    return render_template("home.html", user=current_user)

@views.route("/history", methods=["GET", "POST"])
@login_required
def history():
    return render_template("history.html", user=current_user)