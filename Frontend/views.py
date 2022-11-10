from flask import Blueprint, render_template, request
from .models import Website
from flask_login import login_required, current_user
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("Home.html", user=current_user)


@views.route("/scrape", methods=['GET', 'POST'])
@login_required
def scrape():
    if request.method == "POST":
        scraping_regex = request.form.get("regex")
        scraping_url = request.form.get("url")

        new_scraping_request = Website(url=scraping_url, regex=scraping_regex)
        db.session.add(new_scraping_request)
        db.session.commit()
    else:
        return render_template("Scrape.html", user=current_user)