from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Website, Data, User
from flask_login import login_required, current_user
from . import db
from sqlalchemy import or_, and_
import Frontend.Scrape as Scrape
import smtplib

views = Blueprint("views", __name__)

# create an SMTP object
smtp_obj = smtplib.SMTP('smtp-mail.outlook.com', 587)

# start TLS encryption
smtp_obj.starttls()

# login to the Gmail account
smtp_obj.login('simplescrape@outlook.com', 'Meisterpacho20')


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


@views.route("/deleteHistory")
def delete_history():
    Website.query.filter(Website.user_id == current_user.user_id).delete()
    db.session.commit()
    return personalData()


@views.route("/scrape", methods=['GET', 'POST'])
@login_required
def scrape():
    if request.method == "POST":
        if request.form['btn'] == 'scrapeAll':
            scrape_all_interval()

            websites = get_regular_websites()
            return render_template("Scrape.html", user=current_user, websites=websites)

        else:
            scraping_productname = request.form.get("product_name")
            scraping_suchstring = request.form.get("product_suchstring")
            scraping_url = request.form.get("product_url")

            try:
                scrape = Scrape.Scrape(scraping_url, scraping_suchstring)
                scrape.get_html()
                availability = scrape.is_available()

                save_to_list = request.form.get("save")
                print("SAVE TO LIST?" + str(type(save_to_list)))

                if save_to_list is not None:
                    website = Website(productname=scraping_productname,
                                      url=scraping_url, search_string=scraping_suchstring,
                                      user_id=current_user.user_id, available=availability, regularly="ADD")
                else:
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

                websites = get_regular_websites()

                return render_template("Scrape.html", user=current_user, availability=availability, websites=websites)

            except ValueError as e:
                print("Website: " + scraping_url + " ist incorrect")
                flash('Incorrect URL')
                print("Averted value error for url")

            websites = get_regular_websites()

            # websites = Website.query.filter_by(user_id=current_user.user_id and .regularly is not None)
            return render_template("Scrape.html", user=current_user, websites=websites)

    else:

        websites = get_regular_websites()
        return render_template("Scrape.html", user=current_user, websites=websites)


def get_regular_websites():
    return db.session.query(
        Website
    ).filter(
        and_(
            Website.user_id == current_user.user_id,
            Website.regularly != None
        )
    ).all()


def scrape_all():
    websites = get_regular_websites()

    for website in websites:
        url = website.url
        search_string = website.search_string
        scrape = Scrape.Scrape(url, search_string)
        scrape.get_html()
        if scrape.is_available():
            website.available = "Yes"

            # send the email
            message = '''\
                    Subject: This is a test email
    
                    This is a test email sent using Python and the smtplib module.'''

            smtp_obj.sendmail('simplescrape@outlook.com', current_user.email, message)

        else:
            website.available = "No"
        db.session.commit()


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError

scheduler = BackgroundScheduler()
scheduler.start()


def scrape_all_interval():
    select = request.form.get('time_interval')
    import atexit

    try:
        scheduler.remove_job("regular")

    except JobLookupError as e:
        print("Job not found")
        pass

    if select == "once":
        scrape_all()

    elif select == "10m":
        scheduler.add_job(func=scrape_all, trigger="interval", seconds=600, id="regular")

    elif select == "1h":
        scheduler.add_job(func=scrape_all, trigger="interval", seconds=3600, id="regular")

    elif select == "1d":
        scheduler.add_job(func=scrape_all, trigger="interval", seconds=86400, id="regular")
    atexit.register(lambda: scheduler.shutdown())

