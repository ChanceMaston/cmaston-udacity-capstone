import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .models import db_drop_and_create_all, setup_db, Movie, Actor

MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10


def paginate_movies(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE

    movies = [movie.long() for movie in selection]
    current_movies = movies[start:end]

    return current_movies


def paginate_actors(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * ACTORS_PER_PAGE
    end = start + ACTORS_PER_PAGE

    actors = [actor.format() for actor in selection]
    current_actors = actors[start:end]

    return current_actors

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES
    # GET Routes
    @app.route('/movies')
    def get_movies():
        selection = Movie.query.order_by(Movie.id).all()
        selection_long = []
        if len(selection) == 0:
            abort(404)

        for movie in selection:
            selection_long.append(movie.long())

        return jsonify({'success': True,
                        'movies': selection_long
                        })

    # GET Routes
    @app.route('/actors')
    def get_actors():
        selection = Actor.query.order_by(Actor.id).all()
        selection_long = []
        if len(selection) == 0:
            abort(404)

        for actor in selection:
            selection_long.append(actor.long())

        return jsonify({'success': True,
                        'actors': selection_long
                        })

    # DELETE Routes
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()
            selection = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_movies(request, selection)

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': current_movies,
                'total_movies': len(Movie.query.all())
            })
        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()
            selection = actor.query.order_by(Actor.id).all()
            current_actors = paginate_actors(request, selection)

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': current_actors,
                'total_actors': len(Actor.query.all())
            })
        except:
            abort(422)

    @app.route('/movies', methods=['POST', 'PUT'])
    def create_movie():
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Movie.query.order_by(Movie.id).filter(Movie.title.ilike('%{}%'.format(search)))
                current_movies = paginate_movies(request, selection)
                print(current_movies)

                return jsonify({
                    'success': True,
                    'movies': current_movies,
                    'total_movies': len(selection.all()),
                    'current_movie': 'ALL'
                })
            else:
                movie = Movie(title=new_title,
                              release_date=new_release_date)
                movie.insert()

                selection = Movie.query.order_by(Movie.id).all()
                current_movies = paginate_movies(request, selection)

                return jsonify({
                    'success': True,
                    'created': movie.id,
                    'movies': current_movies,
                    'total_movies': len(Movie.query.all())
                })
        except:
            abort(422)

    @app.route('/actors', methods=['POST', 'PUT'])
    def create_actors():
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Actor.query.order_by(Actor.id).filter(Actor.name.ilike('%{}%'.format(search)))
                current_actors = paginate_actors(request, selection)
                print(current_actors)

                return jsonify({
                    'success': True,
                    'actors': current_actors,
                    'total_actors': len(selection.all()),
                    'current_actors': 'ALL'
                })
            else:
                actor = Actor(name=new_name,
                              age=new_age,
                              gender=new_gender)
                actor.insert()

                selection = Actor.query.order_by(Actor.id).all()
                current_actors = paginate_actors(request, selection)

                return jsonify({
                    'success': True,
                    'created': actor.id,
                    'actors': current_actors,
                    'total_actors': len(Actor.query.all())
                })
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(movie_id):

        selected_movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if not selected_movie:
            abort(404, "Specified Movie not found")

        body = request.get_json()
        try:
            if 'title' in body:
                selected_movie.title = body.get('title')

            if 'release_date' in body:
                selected_movie.release_date = json.dumps(body.get('release_date'))

            selected_movie.update()

            selection = Movie.query.order_by(Movie.id).all()
            selection_long = []
            for movie in selection:
                selection_long.append(movie.long())

            return jsonify({
                'success': True,
                'movies': selection_long
            })
        except:
            abort(422)

    @app.route('/movies/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(actor_id):

        selected_actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if not selected_actor:
            abort(404, "Specified Actor not found")

        body = request.get_json()
        try:
            if 'name' in body:
                selected_actor.name = body.get('name')

            if 'age' in body:
                selected_actor.age = json.dumps(body.get('age'))

            if 'gender' in body:
                selected_actor.gender = json.dumps(body.get('gender'))

            selected_actor.update()

            selection = Actor.query.order_by(Actor.id).all()
            selection_long = []
            for actor in selection:
                selection_long.append(actor.long())

            return jsonify({
                'success': True,
                'actors': selection_long
            })
        except:
            abort(422)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
