from celery import shared_task
from .model import *
import flask_excel as excel
from .mail_service import send_email
from jinja2 import Template
from flask import render_template

@shared_task(ignore_result=False)
def create_file():
    request_books = Request_books.query.with_entities(Request_books.book_name, Request_books.user_email, Request_books.days_requested, Request_books.expiration_date,  Request_books.date_issued).all()
    csv_output = excel.make_response_from_query_sets(request_books,["book_name", "user_email", "days_requested", "expiration_date", "date_issued"], "csv")
    filename = "test1.csv"

    with open(filename, 'wb') as f:
        f.write(csv_output.data)

    return filename



@shared_task(ignore_result=True)
def daily_reminder():
    users = User.query.filter(User.roles.any(name="student")).all()
    for user in users:
        sub = "Daily Report"
        body = "<html>Dear, <br> check your email retuen dates of books and given the feedbacks/n Regards, <br>  BookHavana Team </html>"
        send_email(user.email, sub, body)

    return "ok"
     





def generate_report(user):
    now = datetime.now()
    sections = Section.query.all()
    body = render_template('test.html', email=user, sections=sections)
    return(body)

@shared_task(ignore_result=True)
def Monthly_reminder():
    users = User.query.filter(User.roles.any(name="student")).all()
    for user in users:
            sub = "Monthly Report"
            body = generate_report(user)
            send_email(user.email, sub, body)

    return "ok"
    
