from flask import Blueprint,request,jsonify,render_template,flash,redirect,url_for
import json
from flask_login import current_user,login_required
from werkzeug.utils import secure_filename
from app.catalogue.models import Book,Publication
from app.catalogue.forms import EditBookForm,CreateBookForm,CreatePublicationForm
from app import db,APP_ROOT_DIR
import os

catalogue = Blueprint('catalogue',__name__)

@catalogue.route("/",methods=['GET'])
def home():
	books =  Book.query.all()
	return render_template('catalogue/catalogue_home.html',books=books)


@catalogue.route('/display/publisher/<publisher_id>')
@login_required
def display_publisher(publisher_id):
	publisher = Publication.query.filter_by(id=publisher_id).first()
	publisher_books = Book.query.filter_by(pub_id=publisher.id).all()
	return render_template('catalogue/publisher.html',
						   publisher=publisher,
						   publisher_books=publisher_books)


@catalogue.route('/book/delete/<book_id>', methods=['GET', 'POST'])
@login_required
def delete_book(book_id):
	book = Book.query.get(book_id)
	if request.method == 'POST':
		db.session.delete(book)
		db.session.commit()
		flash('book delete successfully')
		return redirect(url_for('catalogue.home'))
	return render_template('catalogue/delete_book.html', book=book, book_id=book.id)


@catalogue.route('/create/book', methods=['GET', 'POST'])
@login_required
def create_book():
	form = CreateBookForm()
	if form.validate_on_submit():
		pub_id = form.pub_id.data
		filename = secure_filename(form.img_url.data.filename)
		form.img_url.data.save(os.path.join(APP_ROOT_DIR, 'static', 'img', filename))
		book = Book(title=form.title.data, author=form.author.data, avg_rating=form.avg_rating.data,
					format=form.format.data, image=filename, num_pages=form.num_pages.data,
					pub_id=form.pub_id.data)
		db.session.add(book)
		db.session.commit()
		flash('Book added successfully')
		return redirect(url_for('catalogue.display_publisher', publisher_id=pub_id))
	return render_template('catalogue/create_book.html', form=form)


@catalogue.route('/edit/book/<book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
	book = Book.query.get(book_id)
	book_id = book.id
	form = EditBookForm(obj=book)
	if form.validate_on_submit():
		book.title = form.title.data
		book.format = form.format.data
		book.num_pages = form.num_pages.data
		book.format = form.format.data
		book.pub_id = form.pub_id.data
		book.author = form.author.data
		db.session.add(book)
		db.session.commit()
		flash('Book Edited Successfully')
		return redirect(url_for('catalogue.home'))
	
	return render_template('catalogue/edit_book.html', form=form,book_id=book_id)

@catalogue.route('/create/publication', methods=['GET', 'POST'])
@login_required
def create_publication():
	form = CreatePublicationForm()
	if form.validate_on_submit():
		publication = Publication(name=form.name.data)
		db.session.add(publication)
		db.session.commit()
		flash('Publication added successfully')
		return redirect(url_for('catalogue.home'))
	return render_template('catalogue/create_publication.html', form=form)
