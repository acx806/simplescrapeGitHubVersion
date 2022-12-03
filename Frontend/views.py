from flask import Blueprint, render_template, request, flash
from .models import Website, Data, User
from flask_login import login_required, current_user
from . import db
import Frontend.Scrape as Scrape

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("Home.html", user=current_user)


@views.route("/personalData")
def personalData():
    email = current_user.email
    userId = current_user.user_id
    userWebsite = current_user.website
    return render_template("/PersonalData.html", user=current_user, email=email, userId=userId, userWebsite=userWebsite)


@views.route("/ForgotPassword")
def forgotPassword():
    return render_template("/ForgotPassword.html", user=current_user)


@views.route("/scrape", methods=['GET', 'POST'])
@login_required
def scrape():
    if request.method == "POST":
        scraping_productname = request.form.get("product_name")
        scraping_suchstring = request.form.get("product_suchstring")
        scraping_url = request.form.get("product_url")

        try:
            scrape = Scrape.Scrape(scraping_url, scraping_suchstring)
            scrape.get_html()
            availability = scrape.is_available()

            website = Website(productname=scraping_productname,
                              url=scraping_url, search_string=scraping_suchstring,
                              user_id=current_user.user_id, available=availability)

            if scrape.is_available():
                website.available = "Yes"
                flash("In Stock", category="success")
            else:
                website.available = "No"
                flash("Sold Out", category="error")

            db.session.add(website)
            db.session.commit()

            data = Data(website_id=website.website_id, availability=availability)

            db.session.add(data)
            db.session.commit()
        except ValueError as e:
            flash('Incorrect URL')
            print("Averted value error for url")

        websites = Website.query

        return render_template("Scrape.html", user=current_user, availability=availability, websites=websites)
    else:
        websites = Website.query
        return render_template("Scrape.html", user=current_user, websites=websites)
