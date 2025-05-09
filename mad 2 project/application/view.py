from flask import current_app as app,jsonify,request,render_template,send_file
from flask_security import auth_required,roles_required
from .model import *
from werkzeug.security import check_password_hash
from .sec import datastore
from flask_restful import marshal, fields
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import base64
import io
import flask_excel as excel
from .tasks import create_file
from celery.result import AsyncResult

@app.get('/')
def home():
    return render_template('index.html')



@app.post('/librarian_login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not found"}), 404
    if check_password_hash(user.password,data.get('password')):
        return {"token": user.get_auth_token(),"email":user.email,"role":user.roles[0].name}
    
    else:
        return jsonify({"message": "Invalid password"}), 400



@app.post('/signup')
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid or missing JSON"}), 400

    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role_name = "student"

    if not username or not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if datastore.find_user(email=email):
        return jsonify({"message": "User already exists"}), 400

    # ✅ Create role if it doesn't exist
    role_obj = Role.query.filter_by(name=role_name).first()
    if not role_obj:
        role_obj = Role(name=role_name, description="Auto-created role")
        db.session.add(role_obj)
        db.session.commit()

    user = datastore.create_user(
        username=username,
        Name=name,
        email=email,
        password=generate_password_hash(password),
        roles=[role_obj]
    )

    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201






@app.post('/add_section')
@auth_required("token")
@roles_required("admin")
def add_section():
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"message": "Section name is required"}), 400
    
    new_section = Section.query.filter_by(name=name, description=description).first()
    if new_section:
        return jsonify({"message": "Section already exists"}), 400
    else:

        new_section = Section(name=name, description=description)
        db.session.add(new_section)
        db.session.commit()
        return jsonify({"message": "Section added successfully"}), 201


section_fields = {
    'section_id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

@app.get('/sections')
@auth_required('token')
@roles_required('admin')
def sections():
    sections = Section.query.all()
    if len(sections) == 0:
        return jsonify({"message": "No sections found"}), 404
    return marshal(sections, section_fields)



@app.post('/book/<int:section_id>')
@auth_required('token')
@roles_required('admin')
def add_book(section_id):
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    authors = data.get('authors')

    if not name or not content or not authors :
        return jsonify({"message": "All fields are required"}), 400

    new_book = Book(name=name, content=content, authors=authors, section_id=section_id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201





book_fields = {
    'book_id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'authors': fields.String,
    'section_id': fields.Integer
    
}
@app.get('/book_summary/<int:section_id>')
@auth_required('token')
@roles_required('admin')
def books(section_id):
    books = Book.query.filter_by(section_id=section_id).all()
    if len(books) == 0:
        return jsonify({"message": "No books found"}), 404
    return marshal(books, book_fields)



@app.post('/approve_request/<int:book_id>')
@auth_required('token')
@roles_required('admin')
def approve_request(book_id):   
    books = Request_books.query.filter_by(book_id=book_id).first()
    
    if not books:
        return jsonify({"message": "Book request not found"}), 404
    
    main_book = Book.query.filter_by(book_id=book_id).first()
    
    

    book_id = books.book_id
    book_name = books.book_name
    user_email = books.user_email
    book_content = main_book.content
    book_section_id = main_book.section_id
    book_author = main_book.authors
    

    new_book = Approval(book_name=book_name, book_id=book_id, book_content=book_content, book_author=book_author, user_email=user_email, section_id=book_section_id)
    db.session.add(new_book)
    books.status = 1
    
   
    db.session.commit()
    return jsonify({"message": "Book approved successfully"}), 201

@app.post('/reject_request/<int:book_id>')
@auth_required('token')
@roles_required('admin')
def reject_request(book_id):
    books = Request_books.query.filter_by(book_id=book_id).first()
    if not books:
        return jsonify({"message": "Book request not found"}), 404
    db.session.delete(books)
    db.session.commit()
    return jsonify({"message": "Book rejected successfully"}), 201





approval_books_fields = {
    'approval_id': fields.Integer,
    'book_id': fields.Integer,
    'book_name': fields.String,
    'book_author': fields.String,
    'book_content': fields.String,
    'section_id': fields.Integer,
    'user_email': fields.String
}

@app.get('/monitor_books')
@auth_required('token')
@roles_required('admin')
def monitor_books():
    books = Approval.query.all()
    if len(books) == 0:
        return jsonify({"message": "No books found"}), 404
    return marshal(books, approval_books_fields)



@app.post('/update_section/<int:section_id>')
@auth_required('token')
@roles_required('admin')
def update_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if not section:
        return jsonify({"message": "Section not found"}), 404
    data = request.get_json()
    section.name = data.get('name')
    section.description = data.get('description')
    db.session.commit()
    return jsonify({"message": "Section updated successfully"}), 201

@app.delete('/delete_section/<int:section_id>')
@auth_required('token')
@roles_required('admin')
def delete_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    
    if not section:
        return jsonify({"message": "Section not found"}), 404
    
    # Fetch books related to the section
    books = Book.query.filter_by(section_id=section.section_id).all()
    
    # Delete related entries in request_books and approval tables
    if books:
        for book in books:
            # Delete requests related to the book
            request_books = Request_books.query.filter_by(book_id=book.book_id).all()
            for request_book in request_books:
                db.session.delete(request_book)
            
            # Delete approvals related to the section
            approv_books = Approval.query.filter_by(section_id=section_id).all()
            for approv_book in approv_books:
                db.session.delete(approv_book)
            
            # Delete the book itself
            db.session.delete(book)
    
    # Finally, delete the section
    db.session.delete(section)
    db.session.commit()
    
    return jsonify({"message": "Section deleted successfully"}), 200




@app.delete('/delete_book/<int:book_id>')
@auth_required('token')
@roles_required('admin')
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if book:
        # Delete related entries in Request_books
        request_books = Request_books.query.filter_by(book_id=book.book_id).all()
        for request_book in request_books:
            db.session.delete(request_book)
        
        # Delete related entries in Approval
        approv_books = Approval.query.filter_by(book_id=book_id).all()
        for approv_book in approv_books:
            db.session.delete(approv_book)
        
        # Delete the book itself
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 201
    


            

@app.post('/update_book/<int:book_id>')
@auth_required('token')
@roles_required('admin')
def update_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404
    data = request.get_json()
    book.name = data.get('name')
    book.authors = data.get('authors')
    book.content = data.get('content')
    db.session.commit()
    return jsonify({"message": "Book updated successfully"}), 201


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
    plt.close()
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
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return chart_image

@app.route('/librarian_stats')
@auth_required('token')
@roles_required('admin')
def librarian_stats():
    section_chart = generate_section_pie_chart()
    bar_chart = generate_bar_chart()
    return jsonify(section_chart=section_chart, bar_chart=bar_chart)





@app.get('/user_books')
@auth_required('token')
@roles_required('student')
def user_books():
    books = Book.query.all()
    if len(books) == 0:
        return jsonify({"message": "No books found"}), 404
    return marshal(books, book_fields)

@app.post('/request_book/<int:book_id>')
@auth_required('token')
@roles_required('student')
def return_book(book_id):
    books = Book.query.filter_by(book_id=book_id).first()
    data = request.get_json()
    book_name = books.name
    user = data.get('user')

   
    existing_requests = Request_books.query.filter_by(user_email=user).count()
    existing_book = Request_books.query.filter_by(book_name = book_name,user_email=user).first()
    if existing_requests >= 5:
        return jsonify({"message": "you can not request more than 5 books"}), 400
    day_request = int(data.get('day_request'))
    date_issued = datetime.now()
    expiration_date = datetime.now() + timedelta(days=day_request)
    if day_request < 1:
        return jsonify({"message": "plese enter a valid day"}), 400
    if existing_book:
            return jsonify({"message": "you have already requested this book"}), 400
    else:
        new_request = Request_books(book_id=book_id,book_name = book_name, days_requested=day_request,user_email=user,date_issued = date_issued, expiration_date=expiration_date)
        db.session.add(new_request)
        db.session.commit()
        return jsonify({"message": "Book added successfully"}), 201
        



requested_books_fields = {
    'request_id': fields.Integer,   
    'book_id': fields.Integer,
    'book_name': fields.String,
    'days_requested': fields.Integer,
    'user_email': fields.String,
    'expiration_date': fields.DateTime,
    'status': fields.Integer
}



@app.get('/requested_books')
@auth_required('token')
def requested_books():
    books = Request_books.query.all()
    if len(books) == 0:
        return jsonify({"message": "No books found"}), 404
    return marshal(books, requested_books_fields)



@app.route('/my_books', methods=['POST'])
@auth_required('token')
@roles_required('student')
def my_books():
    if not request.is_json:
        return jsonify({"message": "Request content-type must be application/json"}), 415

    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "Email is required"}), 400

    approvals = Approval.query.filter_by(user_email=email).all()
    user_books = Request_books.query.filter_by(user_email=email).all()
    
    current_time = datetime.utcnow()
    for book in user_books:
        if book.expiration_date and book.expiration_date < current_time:
            db.session.delete(book)
    db.session.commit()
    
    books = marshal(approvals, approval_books_fields)  # Ensure the data being marshaled is correct
    return jsonify(books), 200




@app.get('/read_book/<int:book_id>')
@auth_required('token')
@roles_required('student')
def read_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if not book:
        return jsonify({"message": "Book not found"}), 404

    book_data = {
        "name": book.name,
        "author": book.authors,
        "content": book.content,
    }
   
    return jsonify(book_data), 200

    
@app.post('/add_feedback/<int:book_id>')
@auth_required('token')
@roles_required('student')
def add_feedback(book_id):
    data = request.get_json()
    content = data.get('feedback')  # Corrected typo here
    feedback = Feedback(content=content, book_id=book_id)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback added successfully"}), 201



@app.delete('/request_delete_book/<int:book_id>')
@auth_required('token')
@roles_required('student')
def request_delete_book(book_id):
    book = Request_books.query.filter_by(book_id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 201






@app.get('/download-csv')
def download_csv():
    task = create_file.delay()
    return jsonify({"task-id": task.id})


@app.get('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
