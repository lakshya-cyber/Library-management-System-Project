from flask_restful import Resource , Api,reqparse,marshal_with,fields
from .model import Book,Section,db
from datetime import datetime
from .instances import cache

api = Api(prefix="/api")

parser = reqparse.RequestParser()
parser.add_argument('name', type=str,
                    help='name is required should be a string', required=True)
parser.add_argument('content', type=str,
                    help='content Link is required and should be a string', required=True)
parser.add_argument('authors', type=str,
                    help='author is required and should be a string', required=True)
parser.add_argument('section_id', type=int,
                    help='section_id is required and should be a integer', required=True)


parse = reqparse.RequestParser()
parse.add_argument('name', type=str,
                    help='name is required should be a string', required=True)
parse.add_argument('date_created', type=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'),
                    help='date_created is required and should be a datetime (format: YYYY-MM-DD HH:MM:SS)', required=True)
parse.add_argument('description', type=str,
                    help='description is required should be a string', required=True)




book_fields = {
                'book_id': fields.Integer,
                'name': fields.String,
                'content': fields.String,
                'authors': fields.String,
                'section_id': fields.Integer
        
}

class BookResource(Resource):
    @marshal_with(book_fields)
    def get(self):
        all_material = Book.query.all()
        if len(all_material) < 0:
            return {'message': "no records found"}, 404
        return all_material
        
    def post(self):
        args = parser.parse_args()
        book = Book(**args)
        db.session.add(book)
        db.session.commit()
        return {'message': 'book addded successfully'}


    def put(self, book_id):
        args = parser.parse_args()
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        for key, value in args.items():
            if value is not None:
                setattr(book, key, value)
        
        db.session.commit()
        return {'message': 'Book updated successfully'}, 200

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404
        
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 200

   
section_fields = {
                'section_id': fields.Integer,
                'name': fields.String,
                'date_created': fields.DateTime,
                'description': fields.String
    
}


class SectionResource(Resource):
    @marshal_with(section_fields)
    def get(self):
            
            all_section = Section.query.all()
            if len(all_section) < 0:
                return {'message': "no records found"}, 404
            return all_section
            
    def post(self):
        args = parse.parse_args()
        section = Section(**args)
        db.session.add(section)
        db.session.commit()
        return {'message': 'section added successfully'}
    

    def put(self, section_id):
        args = parse.parse_args()
        section = Section.query.get(section_id)
        if not section:
            return {'message': 'section not found'}, 404

        for key, value in args.items():
            if value is not None:
                setattr(section, key, value)
        
        db.session.commit()
        return {'message': 'section updated successfully'}, 200
    


    def delete(self, section_id):
        section = Section.query.get(section_id)
        if not section:
            return {'message': 'section not found'}, 404
        
        db.session.delete(section)
        db.session.commit()
        return {'message': 'section deleted successfully'}, 200
    



api.add_resource(BookResource, '/book', '/book/<int:book_id>')
api.add_resource(SectionResource, '/section', '/section/<int:section_id>')


