from datetime import datetime, timedelta, date
from webapp import app, db
from flask import render_template, redirect, url_for, flash, request
from webapp.form import (
    BookingForm,
    LoginForm,
    RegisterForm,
    BookingForm,
    RemoveRecordForm,
)
from webapp.models import Instrument, Record, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Success! You are logged in as: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("instruments_page"))
        else:
            flash(
                "Username and password are not match! Please try again",
                category="danger",
            )
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f"Account created successfully! You are now logged in as {user_to_create.username}",
            category="success",
        )
        return redirect(url_for("instruments_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"There was an error with creating a user: {err_msg}", category="danger"
            )

    return render_template("register.html", form=form)


@app.route("/instruments", methods=["GET", "POST"])
@login_required
def instruments_page():

    # event_bucket send all events to the calendar for displaying prupose.
    event_bucket = {}
    all_ins_name = set()
    for ins in Instrument.query.all():
        all_ins_name.add(ins.ins_name)

    for ins_name in all_ins_name:
        events = []
        all_books = Record.query.filter_by(ins_name=ins_name)
        for book in all_books:
            curr = {}
            curr["user"] = User.query.filter_by(id=book.owner_user).first().username
            curr["date_start"] = book.start
            events.append(curr)
        event_bucket[ins_name] = events

    # Read the booking request from the form and save them into the database in the unit of 1 day.
    form = BookingForm()
    if form.validate_on_submit():
        start_date = form.start.data
        end_date = form.end.data
        ins_name = form.ins_name.data

        total_booked = (end_date - start_date).days + 1

        for i in range(total_booked):
            new_record = Record(start=start_date + timedelta(days=i), ins_name=ins_name)
            db.session.add(new_record)
            db.session.commit()
            new_record.booked_by(current_user)

        return redirect(url_for("instruments_page"))

    # Print out the errors from the validations
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error: {err_msg}", category="danger")

    # To support the Current Status color change function.
    d = date.today()
    # d is in the data type of date, but the database stores the data in datatime.
    # One cannot compare date to datetime, so here is the conversion.
    today = datetime.combine(d, datetime.min.time())
    color_events = {}

    # color_event{'ins_name': [events of that instrument]}
    for ins_name in all_ins_name:
        events = set()
        all_books = Record.query.filter_by(ins_name=ins_name)
        for event in all_books:
            events.add(event.start)
        color_events[ins_name] = events

    all_HPLCs = Instrument.query.filter_by(ins_type="HPLC")
    return render_template(
        "instruments.html",
        all_HPLCs=all_HPLCs,
        event_bucket=event_bucket,
        form=form,
        today=today,
        color_events=color_events,
    )


@app.route("/my_reservation", methods=["GET", "POST"])
@login_required
def my_reservation_page():

    # Read record id from the form and remove that record, only if the request method equal to POST
    form = RemoveRecordForm()

    # def get_upcoming_reservations(owner)

    if request.method == "GET":
        # Filter out the reservations that earlier than today
        all_reservations = Record.query.filter_by(owner_user=current_user.id)
        d = date.today()
        today = datetime.combine(d, datetime.min.time())
        upcoming_reservations = []
        for reservation in all_reservations:
            if reservation.start >= today:
                upcoming_reservations.append(reservation)
        return render_template(
            "my_reservation.html",
            upcoming_reservations=upcoming_reservations,
            form=form,
        )

    if request.method == "POST":
        remove_record_id = form.record_id.data
        record = Record.query.filter_by(id=remove_record_id).first()
        if record:
            record.remove()

        return redirect(url_for("my_reservation_page"))


@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("home_page"))
