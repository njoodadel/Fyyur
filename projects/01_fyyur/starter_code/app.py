#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    def __repr__(self):
      return f'<{self.name} {self.id} {self.state}>'
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer,primary_key=True)
  start_time = db.Column(db.String(120))
  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"),nullable=False)
  artist = db.relationship("Artist", backref=("artist"))
  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"),nullable=False)
  venue = db.relationship("Venue", backref=("venue"))



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  # return babel.dates.format_datetime(date, format)
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
 
  data = []
  AllCityState =db.session.query(Venue.city, Venue.state).distinct()
  for cityState in AllCityState:
    venues = db.session.query(Venue.id, Venue.name).filter(Venue.city == cityState[0]).filter(Venue.state == cityState[1])
    data.append({
       "city": cityState[0],
        "state": cityState[1],
        "venues": venues
    })
  return render_template('pages/venues.html', areas=data)
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
 
  data = []
  search_term=request.form.get('search_term', '')
  venues = db.session.query(Venue).filter(Venue.name.ilike("%"+search_term+"%")).all()
  for venue in venues:
    data.append({
      "id": venue.id,
      "name":venue.name})
  
  response = {
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response,search_term=search_term )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
 
  venue = Venue.query.filter_by(id=venue_id).first()
  data={
    "id":venue.id,
    "name": venue.name,
    "city": venue.city,
    "state":venue.state ,
    "phone":venue.phone ,
    "facebook_link": venue.facebook_link,
    "address": venue.address,
    "image_link":venue.image_link ,
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  address = request.form.get('address')
  phone = request.form.get('phone')
  facebook_link = request.form.get('facebook_link')


  try:
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone,facebook_link=facebook_link)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
   db.session.rollback()
   flash('An error occurred. Venue ' + data.name + ' could not be listed.')

  finally:
   db.session.close()


  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  
  try:
    Todo.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  

  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data= []
  artists = db.session.query(Artist.id, Artist.name).all()
  for artist in artists:
    data.append ({
      "id": artist.id,
      "name":artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
 
  data = []
  search_term=request.form.get('search_term', '')
  artists = db.session.query(Artist).filter(Artist.name.ilike("%"+search_term+"%")).all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name":artist.name})
  
  response = {
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.filter_by(id=artist_id).first()
  print("the id:::::",artist.id)
  data = {
    "id":artist.id,
    "name": artist.name,
    "city": artist.city,
    "state":artist.state ,
    "phone":artist.phone ,
    "facebook_link": artist.facebook_link,
    "image_link":artist.image_link ,
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  data = {
    "id":artist.id,
    "name": artist.name,
    "city": artist.city,
    "state":artist.state ,
    "phone":artist.phone ,
    "facebook_link": artist.facebook_link,
    "image_link":artist.image_link ,
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    artist = db.session.query(Artist).filter(Artist.id==artist_id).first()
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.facebook_link = request.form.get('facebook_link')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # Artist.query.filter_by(id=artist_id).update({id:artist_id,name:name,city:city,state:state, phone:phone,facebook_link:facebook_link})

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  data={
    "id":venue.id,
    "name": venue.name,
    "city": venue.city,
    "state":venue.state ,
    "phone":venue.phone ,
    "facebook_link": venue.facebook_link,
    "address": venue.address,
    "image_link":venue.image_link ,
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = db.session.query(Venue).filter(Venue.id==venue_id).first()
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.address = request.form.get('address')
    venue.facebook_link = request.form.get('facebook_link')
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  facebook_link = request.form.get('facebook_link')


  try:
    artist = Artist(name=name, city=city, state=state, phone=phone,facebook_link=facebook_link)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + name + ' was successfully listed!')

  except:
   db.session.rollback()
   flash('An error occurred. Artist ' + name + ' could not be listed.')
  finally:
   db.session.close()
 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
 
  data= []
  shows = db.session.query(Show, Artist,Venue).filter(Show.venue_id == Venue.id).filter(Show.artist_id == Artist.id).all()
  
  print("shoows",shows)
  for show in shows:
    print(show[2].name)
    data.append ({
      "venue_id": show[2].id,
      "venue_name":show[2].name,
      "artist_id": show[1].id,
      "artist_name": show[1].name,
      "start_time":show[0].start_time
    })
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  artist_id = request.form.get('artist_id')
  venue_id = request.form.get('venue_id')
  start_time = request.form.get('start_time')

  try:
    show = Show(artist_id = artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
