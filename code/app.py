from flask import Flask, render_template, request, redirect, url_for, flash,session
from db import *
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
from collections import Counter
import base64

app = Flask(__name__)
app.secret_key = "saregamamusic"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"



from resourse import api
api.init_app(app)

bcrypt = Bcrypt(app)

db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


#user 
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        new_username = User.query.filter_by(username = username).first()
        new_name = User.query.filter_by(Name = name).first()
        new_email = User.query.filter_by(email = email).first()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if new_username:
            flash('username is already exits.please choose another username')
            return render_template('user_register.html')
        elif new_name:
            flash('name is already exits.please choose another name')
            return render_template('user_register.html')
        if new_email:
            flash('email already exits.please choose another email')
            return render_template('user_register.html')
        else:
            new_user = User(username=username,Name = name, password=hashed_password , email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('successful register')
            return redirect(url_for('user_login'))
    return render_template('user_register.html')


@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['username'] = username
                return redirect(url_for('user_dashboard')) 
            else:
                flash('wrong password .Please Try again')
        else:
            flash('Invalid username . Please Try again.')
            return redirect(url_for('user_login'))
    return render_template('user_login.html')


@app.route('/user_dashboard')
def user_dashboard():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('user_dashboard.html',user = user)


@app.route('/user_profile')
def user_profile():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('user_profile.html',user = user)


@app.route('/user_books')
def user_books():
    books = Book.query.all()
    return render_template('user_books.html', books=books)


@app.route('/search_book', methods=['GET'])
def search_book():
    search_query = request.args.get('search')
    books = Book.query.filter(Book.name.ilike(f'%{search_query}%')).all()
    if books: 
        return render_template('user_books.html', books=books)
    else:
        flash('Book not found. Please try again.')
        return render_template('user_books.html')
        

@app.route('/request_book', methods=['POST'])
def request_book():
    book_id = request.form['book_id']
    return redirect(url_for('request_book_form', book_id=book_id))


@app.route('/request_book_form/<int:book_id>', methods=['GET', 'POST'])
def request_book_form(book_id):
    user = User.query.filter_by(username=session['username']).first()
    book = Book.query.get(book_id)
    section = book.section  
    if request.method == 'POST':
        existing_requests = Request_books.query.filter_by(user_id=user.id).count()
        existing_book = Request_books.query.filter_by(book_name = book.name,user_id=user.id).first()
        if existing_requests >= 5:
                flash('You cannot request any books after you meet your maximum requests. Your maximum request has been met')
                return redirect(url_for('user_books')) 
        day_request = int(request.form.get('day_request'))
        date_issued = datetime.now()
        expiration_date = datetime.now() + timedelta(days=day_request)
        if day_request < 1:
            flash('plese enter a valid day')
            return redirect(url_for('request_book_form',book_id = book.book_id))
        if existing_book:
            flash('you send already request.')
            return redirect(url_for('user_books'))
        else:
            new_request = Request_books(book_id=book_id,book_name = book.name, days_requested=day_request,user_id=user.id,date_issued = date_issued,status = 0, expiration_date=expiration_date)
            db.session.add(new_request)
            db.session.commit()
            flash('request sent successfully.')
            return redirect(url_for('user_books')) 
    return render_template('request_book.html', book=book, user=user, section=section, book_id=book_id)



@app.route('/search_book_my', methods=['GET'])
def search_book_my():
    user = User.query.filter_by(username=session['username']).first()
    search_query = request.args.get('search')
    if search_query:
        books = Approval.query.filter_by(user_id=user.id).filter(Approval.book_name.ilike(f'%{search_query}%')).all()
        if books:
            return render_template('my_books.html', books=books)
        else:
            flash('Books not found!')
            return render_template('my_books.html')
    else:
        return redirect(url_for('my_books'))



@app.route('/my_books')
def my_books():
    user = User.query.filter_by(username=session['username']).first()
    approvals = Approval.query.filter_by(user_id=user.id).all()
    user_books = Request_books.query.filter_by(user_id=user.id).all()
    current_time = datetime.utcnow()
    for book in user_books:
        if book.expiration_date and book.expiration_date < current_time:
            db.session.delete(book)
    db.session.commit()
    return render_template('my_books.html',books=approvals,user_books=user_books)


@app.route('/read_book/<int:approval_id>', methods=['GET','POST'])
def read_book(approval_id):
    book = Approval.query.filter_by(book_id = approval_id).all()
    return render_template('read_book.html', book=book)


@app.route('/requested_books', methods=['GET','POST'])
def requested_books():
    user = User.query.filter_by(username=session['username']).first()
    user_books = Request_books.query.filter_by(user_id=user.id).all()
    return render_template('requested_books.html',user = user_books)


@app.route('/delete_request/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    book = Request_books.query.get(request_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('requested_books'))



@app.route('/user_stats')
def user_stats():
    user = User.query.filter_by(username=session['username']).first()
    existing_requests = Request_books.query.filter_by(user_id=user.id).count()
    approvals = Approval.query.filter_by(user_id = user.id).all()
    max_request = 5
    approvals_request = Approval.query.filter_by(user_id = user.id).count()
    section_counts = Counter(approval.section_name for approval in approvals)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)  
    plt.bar(section_counts.keys(), section_counts.values(), color='skyblue')
    plt.xlabel('Section Name')
    plt.ylabel('Number of Books')
    plt.title('Section-wise Book Counts')
    plt.xticks(rotation=45, ha='right')  
    plt.subplot(1, 2, 2)  
    plt.pie(section_counts.values(), labels=section_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Section Distribution')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return render_template('user_stats.html',approvals_requests = approvals_request,max_request = max_request, existing_request =  existing_requests, section_counts=section_counts, chart_image=chart_image)


@app.route('/submit_feedback/<int:book_id>', methods=['POST'])
def submit_feedback(book_id):
    if request.method == 'POST':
        feedback_content = request.form['feedback']
        new_feedback = Feedback(content=feedback_content, book_id=book_id)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback submitted successfully!')
        return redirect(url_for('read_book', book_id=book_id))
    return redirect(url_for('read_book', book_id=book_id)) 




#librarian  
@app.route('/librarian_register', methods=['GET', 'POST'])
def librarian_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_librarian = Librarian(username=username, password=hashed_password )
        db.session.add(new_librarian)
        db.session.commit()
        return redirect(url_for('librarian_login'))
    return render_template('librarian_register.html')


@app.route('/librarian_login', methods=['GET', 'POST'])
def librarian_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Librarian.query.filter_by(username=username).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                session['username'] = username
                return redirect(url_for('librarian_dashboard')) 
            else:
                flash('wrong password .Please Try again')
                return redirect(url_for('librarian_login'))
        else:
            flash('Invalid username . Please Try again.')
            return redirect(url_for('librarian_login'))
    return render_template('librarian_login.html')


@app.route('/librarian_dashboard')
def librarian_dashboard():
    librarian = Librarian.query.filter_by(username=session['username']).first()
    return render_template('librarian_dashboard.html',librarian=librarian)


@app.route('/add_section', methods=['GET','POST'])
def add_section():
    if request.method == 'POST':
        title = request.form['name']
        description = request.form['description']
        date =datetime.now()
        librarian = Librarian.query.filter_by(username=session['username']).first()
        new_section = Section.query.filter_by(name=title, description=description).first()
        if new_section:
            flash('section name is already exits choose another name and description')
            return redirect(url_for('section_details'))
        else:
            adding_section = Section(name=title, description=description,date_created = date,librarian_id = librarian.id)
            db.session.add(adding_section)
            db.session.commit()
            flash('section added successfully')
            return redirect(url_for('section_details'))
    return render_template('adding_section.html')


@app.route('/section_details')
def section_details():
    sections = Section.query.all()
    return render_template('section_details.html', sections=sections)


@app.route('/search_section', methods=['GET'])
def search_section():
    search_query = request.args.get('search')
    sections = Section.query.filter(Section.name.ilike(f'%{search_query}%')).all()
    if sections: 
        return render_template('section_details.html', sections=sections)       
    else:
        flash('section not found. Please try again.')
        return render_template('section_details.html')
        


@app.route('/<int:section_id>/update_section', methods=['POST','GET'])
def update_section(section_id):
    this_section = Section.query.get(section_id)
    if request.method == "POST":
        updated_name = request.form.get('name')
        updated_description = request.form.get('description')
        this_section.name = updated_name
        this_section.description = updated_description
        db.session.commit()
        return redirect(url_for('section_details'))
    return render_template('update_section.html', this_section=this_section)


@app.route('/delete_section/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if section:
            books = Book.query.filter_by(section_id=section_id).all()
            for book in books:
                flash('You can delete this section. Because this section contains the book which is approved for the user')
                return redirect(url_for('section_details'))
    else:
        flash('section is deleted successfully.')
        db.session.delete(section)
        db.session.commit()
        return redirect(url_for('section_details'))



@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        section_id = request.form.get('section')
        new_book = Book.query.filter_by(name=title, authors=author).first()
        if new_book:
            flash('book is already exits. choose another name')
            return render_template('book_summary.html',section_id = section_id)
        else:
            adding_book = Book(name=title, authors=author,content = content ,section_id=section_id)
            db.session.add(adding_book)
            db.session.commit()
            flash('book added successfully.')
        return redirect(url_for('section_details'))

@app.route('/book/<int:section_id>')
def book(section_id):
    books = Book.query.filter_by(section_id=section_id).all()
    sections = Section.query.all()
    return render_template('book.html', books=books, sections=sections)

@app.route('/book_summary/<int:section_id>', methods=['GET'])
def book_summary(section_id):
    section = Section.query.get(section_id)
    books = Book.query.filter_by(section_id=section_id).all()
    return render_template('book_summary.html', section_name=section.name, section_id=section_id, books=books)


@app.route('/search_book_in_section/<int:section_id>', methods=['GET'])
def search_book_in_section(section_id):
    section = Section.query.get(section_id)
    search_query = request.args.get('search', '')
    if search_query:
        books = Book.query.filter(Book.section_id == section_id, Book.name.ilike(f'%{search_query}%')).all()
        if books:
            return render_template('book_summary.html', section_name=section.name, section_id=section.section_id, books=books)
        else:
            flash('book not found')
            return render_template('book_summary.html', section_id=section.section_id)
    else:
        books = Book.query.filter_by(section_id=section_id).all()
    return render_template('book_summary.html', section_name=section.name, section_id=section.section_id, books=books)

        
@app.route('/<int:book_id>/update_book', methods=['POST','GET'])
def update_book(book_id):
    this_book = Book.query.get(book_id)
    section_id = this_book.section_id
    if request.method == "POST":
        updated_name = request.form.get('name')
        updated_author = request.form.get('author')
        update_content = request.form.get('content')
        this_book.name = updated_name
        this_book.authors = updated_author
        this_book.content = update_content
        db.session.commit()
        return redirect(url_for('book_summary',section_id=section_id))
    return render_template('update_book.html', this_book=this_book)


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    approve = Approval.query.get(book_id)
    if approve is not None:
        flash('You cannot delete this book because this book is approved for the user')
        return redirect(url_for('section_details'))
    else:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('section_details'))



@app.route('/handle_request/<int:request_id>', methods=['POST'])
def handle_request(request_id):
    requests = Request_books.query.get(request_id)
    action = request.form.get('action')
    if action == 'approve':
            book = requests.book
            user = requests.user
            new_approval = Approval(book_id = book.book_id,book_name=book.name,book_content = book.content, book_author=book.authors,user_id=user.id,section_name=book.section.name)
            db.session.add(new_approval)
            requests.status = 1
            db.session.commit()
    elif action == 'reject':
            db.session.delete(requests)
            db.session.commit()
    return redirect(url_for('librarian_dashboard_requests',requests = requests))


@app.route('/librarian_dashboard_requests')
def librarian_dashboard_requests():
    requests = Request_books.query.all()
    return render_template('librarian_dashboard_requests.html', requests=requests)


@app.route('/monitor_books')
def monitor_books():
    books = Approval.query.all()
    user = User.query.filter_by(username=session['username']).first()
    books_info = []
    for book in books:
        books_info.append({'book_name': book.book_name, 'user_id':user.username,'book_author':book.book_author,'section_name':book.section_name})
    return render_template('monitor_books.html', books_info=books_info)


def generate_section_pie_chart():
    sections = Section.query.all()
    section_counts = {section.name: len(section.books) for section in sections}
    plt.figure(figsize=(8, 6))
    plt.pie(section_counts.values(), labels=section_counts.keys(), autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Section Distribution')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return chart_image

def generate_bar_chart():
    sections = Section.query.all()  
    section_counts = {section.name: len(section.books) for section in sections}
    plt.figure(figsize=(10, 5)) 
    plt.bar(section_counts.keys(), section_counts.values())  
    plt.xlabel('Sections')
    plt.ylabel('Number of Books')
    plt.title('Section Distribution')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(1)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return chart_image



@app.route('/librarian_stats')
def librarian_stats():
    section_chart = generate_section_pie_chart()
    bar_chart = generate_bar_chart()
    return render_template('librarian_stats.html', section_chart=section_chart,book_chart = bar_chart)



@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
