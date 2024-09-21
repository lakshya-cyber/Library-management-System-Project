import os
from flask_restful import Resource , Api
from flask import request, jsonify, session
from datetime import datetime
from db import *
from werkzeug.utils import secure_filename

api = Api()

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            return jsonify({
                'book_id': book.book_id,
                'book_name': book.name,
                'book_content': book.content,
                'book_author': book.authors,
                'section_id': book.section_id,
            })
        else:
            return jsonify({'message': 'book not found'})
        
    def put(self, book_id):
        book = Book.query.filter_by(book_id=book_id).first()
        if book:
            data = request.get_json()
            book.name = data.get('book_name', book.name)
            book.authors = data.get('book_author', book.authors)
            book.content = data.get('book_content', book.content)

            db.session.commit()

            return jsonify({'message': 'book updated successfully'})
        else:
            return jsonify({'message': 'book not found'})
        
    def delete(self, book_id):
        song = Book.query.filter_by(book_id=book_id).first()
        if song:
            db.session.commit()
            return jsonify({'message': 'book deleted successfully'})
        else:
            return jsonify({'message': 'book not found'})
        


class SectionResource(Resource):
    def get(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()

        if section:

            return jsonify({
                'section_name':section.name,
                'section_description':section.description
            })
        else:
            return jsonify({'message': 'Album not found'})

    def put(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        if section:
            data = request.get_json()
            section.name = data.get('section_name', section.name)
            section.description = data.get('section_description', section.description)
            db.session.commit()
            return jsonify({'message': 'section updated successfully'})
        else:
            return jsonify({'message': 'section not found'})

    def delete(self, section_id):
        section = Section.query.filter_by(section_id=section_id).first()
        if section:
            db.session.delete()
            db.session.commit()
            return jsonify({'message': 'section deleted successfully'})
        else:
            return jsonify({'message': 'section not found'})
        



api.add_resource(BookResource, '/api/book/<int:book_id>')
api.add_resource(SectionResource, '/api/section/<int:section_id>')