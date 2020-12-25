#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask, render_template, request, Response, flash, redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from flask import Flask
from models import app, db, Venue, Artist, Show   
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
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
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ).\
    all()
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ).\
    all()

  data={
    "id":venue.id,
    "name": venue.name,
    "city": venue.city,
    "state":venue.state ,
    "phone":venue.phone ,
    "facebook_link": venue.facebook_link,
    "address": venue.address,
    "image_link":venue.image_link ,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    'past_shows': [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
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
  form = VenueForm(request.form)
 
  try:
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
   db.session.rollback()
   flash('An error occurred. Venue ' + data.name + ' could not be listed.')

  finally:
   db.session.close()


  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
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
  past_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time < datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ).\
    all()
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time > datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ).\
    all()
  data = {
    "id":artist.id,
    "name": artist.name,
    "city": artist.city,
    "state":artist.state ,
    "phone":artist.phone ,
    "geners":artist.genres,
    "facebook_link": artist.facebook_link,
    "image_link":artist.image_link ,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    'past_shows': [{
            'venue_id': venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time
        } for venue, show in past_shows],
        'upcoming_shows': [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time
        } for venue, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
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
    "image_link":artist.image_link,
    "website":artist.website,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
 
  form = ArtistForm(request.form)

  try:
    
    artist = db.session.query(Artist).filter(Artist.id==artist_id).first()
    form.populate_obj(artist)

    
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()


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
    "website":venue.website,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)

  try:

    venue = db.session.query(Venue).filter(Venue.id==venue_id).first()
    form.populate_obj(venue)

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
  form = ArtistForm(request.form)

  name = request.form.get('name')



  try:
    artist = Artist()
    form.populate_obj(artist)
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
  form = ShowForm(request.form)

  # artist_id = request.form.get('artist_id')
  # venue_id = request.form.get('venue_id')
  # start_time = request.form.get('start_time')

  try:
    #show = Show(artist_id = artist_id, venue_id=venue_id, start_time=start_time)
    show = Show()
    form.populate_obj(show)
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
