from flask import Flask, request, jsonify, render_template, session, redirect, flash, url_for
from sqlalchemy import or_, exists
import time, os
from models.models import *
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'tfinal.db')
print("Ruta de la base de datos:", app.config['SQLALCHEMY_DATABASE_URI'])
db.init_app(app)

with app.app_context():
      db.create_all()

isLogin = False
secret_key = Fernet.generate_key()
app.secret_key = secret_key

#--------------------------------------------LOGIN/OUT--------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
      if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # get el usuario de la base de datos por nombre de usuario
            usuario = User.query.filter_by(username=username).first()

            # Verificar si el usuario existe y la contraseña es correcta
            if usuario and check_password_hash(usuario.password, password):
                  # Establecer una sesión para el usuario autenticado
                  session['username'] = username
                  return redirect('/index')  # Redirigir a la página principal después del inicio de sesión

            # Si las credenciales no coinciden, mostrar un mensaje de error
            return render_template('login.html', mensaje='Credenciales inválidas. Inténtalo de nuevo.')

      return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout', methods=['GET', 'POST'])
def logout():
      session.pop('username', None)
      return redirect('/login')

@app.route('/')
def pagina_principal():
      if 'username' in session:
            return render_template('index.html', username=session['username'])
      else:
            return redirect('/login')
      
#--------------------------------------------INDEX--------------------------------------------
@app.route('/index')
def index():
      if 'username' in session:
            user = User.query.filter_by(username=session['username']).first()
            return render_template('index.html', fullname=user.fullname)
      else:
            return redirect('/login')

@app.route('/index/busqueda', methods=['POST'])
def buscar_artistas_con_albumes():
      search_query = request.form['search_query']
      artistas_con_albumes = Artist.query.filter(
            Artist.name.ilike(f"%{search_query}%"),
            exists().where(Album.artistid == Artist.artistid)
      ).all()
      resultados = []
      for artista in artistas_con_albumes:
            resultados.append({'artistid': artista.artistid, 'name': artista.name})
      return render_template('index.html', artistas=artistas_con_albumes, search_query=search_query)

#--------------------------------------------USUARIO--------------------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
      if request.method == 'POST':
            username = request.form['username']
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                  flash('El nombre de usuario ya está en uso. Por favor, elige otro.', 'error')
                  return redirect('/registro')

            fullname = request.form['fullname']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                  flash('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.', 'error')
                  return redirect('/registro')
            hashed_password = generate_password_hash(password)

            nuevo_usuario = User(username=username, fullname=fullname, password=hashed_password)

            try:
                  db.session.add(nuevo_usuario)
                  db.session.commit()
                  flash('Registro exitoso', 'success')
                  return redirect('/login')
            except Exception as e:
                  flash(f'Error al registrar usuario: {str(e)}', 'error')
                  db.session.rollback() 
      return render_template('registro.html')

@app.route('/usuarios/<usuarioid>', methods=['GET'])
def get_usuario(usuarioid):
      usuario = User.query.get(usuarioid)
      if usuario:
            return jsonify({'id': usuario.id, 'username': usuario.username, 'fullname': usuario.fullname, 'isAdmin': usuario.isAdmin}), 200
      else:
            return jsonify({'message': 'Usuario no encontrado'}), 404

#--------------------------------------------ARTISTA--------------------------------------------
@app.route('/artistas/nuevo', methods=['GET'])
def nuevo_artista():
      return render_template('nuevoartista.html')

@app.route('/artistas/nuevo', methods=['POST'])
def crear_artista():
      if request.method == "POST":
            name = request.form["name"]
            nuevo_artista = Artist(name=name)
            db.session.add(nuevo_artista)
            db.session.commit()
            flash('Artista agregado correctamente', 'success')
            return redirect('/artistas')
      return render_template('nuevoartista.html')

@app.route('/artistas', methods=['GET'])
def get_artistas():
      artistas = Artist.query.all()
      resultados = []
      for artista in artistas:
            resultados.append({'artistid': artista.artistid, 'name': artista.name})            
      return render_template('artistas.html', artistas=artistas)

@app.route('/artistas/<artistid>', methods=['GET'])
def get_artista(artistid):
      artista = Artist.query.get(artistid)
      if artista:
            return jsonify({'artistid': artista.artistid, 'name': artista.name}), 200
      else:
            return jsonify({'message': 'Artista no encontrado'}), 404

@app.route('/artistas/<artistid>', methods=['POST'])
def actualizar_artista(artistid):
      artista = Artist.query.get(artistid)
      if artista:
            nuevo_nombre = request.form['name']
            artista.name = nuevo_nombre
            db.session.commit()
            flash('Artista actualizado correctamente', 'success')
            return redirect('/artistas')
      else:
            flash('Artista no encontrado', 'error')
            return redirect('/artistas')

@app.route('/artistas/<artistid>/editar', methods=['GET', 'POST'])
def editar_artista(artistid):
      artista = Artist.query.get(artistid)
      if artista:
            if request.method == 'GET':
                  return render_template('editarartista.html', artista=artista)
            elif request.method == 'POST':
                  nuevo_nombre = request.form['name']
                  artista.name = nuevo_nombre
                  db.session.commit()
                  flash('Artista actualizado correctamente', 'success')
                  return redirect('/artistas')
      else:
            flash('Artista no encontrado', 'error')
            return redirect('/artistas')
      
@app.route('/artistas/<artistid>', methods=['DELETE'])
def eliminar_artista(artistid):
      artista = Artist.query.get(artistid)
      if artista:
            db.session.delete(artista)
            db.session.commit()
            return jsonify({'message': 'Artista eliminado correctamente'}), 200
      else:
            return jsonify({'message': 'Artista no encontrado'}), 404

@app.route('/artistas/buscar', methods=['POST'])
def buscar_artistas():
      search_query = request.form['search_query']
      artistas = Artist.query.filter(Artist.name.ilike(f"%{search_query}%")).all()
      return render_template('artistas.html', artistas=artistas, search_query=search_query)
#--------------------------------------------ALBUM--------------------------------------------
@app.route('/albums/nuevo', methods=['GET'])
def nuevo_album():
      return render_template('nuevoalbum.html')

@app.route('/albums/nuevo', methods=['POST'])
def crear_album():
      if request.method == "POST":
            title = request.form["title"]
            artistid = request.form["artistid"]
            nuevo_album = Album(title=title, artistid=artistid)
            db.session.add(nuevo_album)
            db.session.commit()
            flash('Álbum agregado correctamente', 'success')
            return redirect('/albums')
      return render_template('nuevoalbum.html')

# Operación para get todos los álbumes
@app.route('/albums', methods=['GET'])
def get_albumes():
      albums = Album.query.all()
      resultados = []
      for album in albums:
            resultados.append({'albumid': album.albumid, 'title': album.title, 'artistid': album.artistid})
      return render_template('albums.html', albums=albums)

# Operación para get un álbum por su ID
@app.route('/albums/<albumid>', methods=['GET'])
def get_album(albumid):
      album = Album.query.get(albumid)
      if album:
            return jsonify({'albumid': album.albumid, 'title': album.title, 'artistid': album.artistid}), 200
      else:
            return jsonify({'message': 'Álbum no encontrado'}), 404

# Operación para actualizar un álbum por su ID
@app.route('/albums/<albumid>/editar', methods=['GET'])
def editar_album(albumid):
      album = Album.query.get(albumid)
      if album:
            return render_template('editaralbum.html', album=album)
      else:
            flash('Álbum no encontrado', 'error')
            return redirect('/albums')

@app.route('/albums/<albumid>', methods=['POST'])
def actualizar_album(albumid):
      if request.form['_method'] == 'PUT':
            album = Album.query.get(albumid)
            if album:
                  title = request.form['title']
                  artistid = request.form['artistid']
                  
                  album.title = title
                  album.artistid = artistid
                  
                  db.session.commit()
                  flash('Álbum actualizado correctamente', 'success')
                  return redirect('/albums')
            else:
                  return jsonify({'message': 'Álbum no encontrado'}), 404
      else:
            return jsonify({'message': 'Método no permitido'}), 405

@app.route('/albums/<albumid>', methods=['DELETE'])
def eliminar_album(albumid):
      album = Album.query.get(albumid)
      if album:
            db.session.delete(album)
            db.session.commit()
            return jsonify({'message': 'Álbum eliminado correctamente'}), 200
      else:
            return jsonify({'message': 'Álbum no encontrado'}), 404

@app.route('/albums/buscar', methods=['POST'])
def buscar_albumes():
      search_query = request.form['search_query']
      albumes = Album.query.filter(Album.title.ilike(f"%{search_query}%")).all()
      return render_template('albums.html', albums=albumes)

#--------------------------------------------TRACK--------------------------------------------

@app.route('/tracks/nuevo', methods=['GET'])
def nuevo_track():
      return render_template('nuevotrack.html')

@app.route('/tracks/nuevo', methods=['POST'])
def crear_cancion():
      if request.method == "POST":
            name = request.form["name"]
            albumid = request.form["albumid"]
            composer = request.form["composer"]
            milliseconds = request.form["milliseconds"]
            bytes = request.form["bytes"]
            unitprice = request.form["unitprice"]
            nueva_cancion = Track(
                  name=name,
                  albumid=albumid,
                  composer=composer,
                  milliseconds=milliseconds,
                  bytes=bytes,
                  unitprice=unitprice
            )
            db.session.add(nueva_cancion)
            db.session.commit()
            flash('Canción agregada correctamente', 'success')
            return redirect('/tracks')
      return render_template('nuevotrack.html')

@app.route('/tracks', methods=['GET'])
def get_tracks():
      tracks = Track.query.all()
      resultados = []
      for cancion in tracks:
            resultados.append({
                  'trackid': cancion.trackid,
                  'name': cancion.name,
                  'composer': cancion.composer,
                  'milliseconds': cancion.milliseconds,
                  'bytes': cancion.bytes,
                  'unitprice': cancion.unitprice,
                  'albumid': cancion.albumid
            })
      return render_template('tracks.html', tracks=tracks)

@app.route('/tracks/<trackid>', methods=['GET'])
def get_cancion(trackid):
      cancion = Track.query.get(trackid)
      if cancion:
            return jsonify({
                  'trackid': cancion.trackid,
                  'name': cancion.name,
                  'composer': cancion.composer,
                  'milliseconds': cancion.milliseconds,
                  'bytes': cancion.bytes,
                  'unitprice': cancion.unitprice,
                  'albumid': cancion.albumid
            }), 200
      else:
            return jsonify({'message': 'Canción no encontrada'}), 404

@app.route('/tracks/<trackid>', methods=['POST', 'PUT'])
def actualizar_cancion(trackid):
      if request.method == 'POST' or request.form.get('_method') == 'PUT':
            cancion = Track.query.get(trackid)
            if cancion:
                  name =  request.form['name']
                  composer =  request.form['composer']
                  milliseconds =  request.form['milliseconds']
                  bytes =  request.form['bytes']
                  unitprice =  request.form['unitprice']
                  albumid =  request.form['albumid']

                  cancion.name = name
                  cancion.composer = composer
                  cancion.albumid = albumid
                  cancion.milliseconds = milliseconds
                  cancion.bytes =  bytes
                  cancion.unitprice =  unitprice                  

                  db.session.commit()
                  flash('Canción actualizada correctamente', 'success')
                  return redirect('/tracks')
            else:
                  flash('Canción no encontrada', 'error')
                  return redirect('/tracks')
      else:
            return jsonify({'message': 'Método no permitido'}), 405
                  
@app.route('/tracks/<trackid>/editar', methods=['GET'])
def obtener_detalle_cancion(trackid):
      cancion = Track.query.get(trackid)
      if cancion:
            return render_template('editartrack.html', track=cancion)
      else:
            flash('Canción no encontrada', 'error')
            return redirect('/tracks')

@app.route('/tracks/<trackid>', methods=['DELETE'])
def eliminar_cancion(trackid):
      if request.form.get('name') == 'delete_track':
            track = Track.query.get(trackid)
            if track:
                  db.session.delete(track)
                  db.session.commit()
                  return jsonify({'message': 'Canción eliminada correctamente'}), 200
            else:
                  return jsonify({'message': 'Canción no encontrada'}), 404

@app.route('/tracks/filtrar', methods=['POST'])
def filtrar_canciones():
      nombre = request.form.get('nombre')
      compositor = request.form.get('compositor')
      id_album = request.form.get('id_album')
      query = Track.query
      if nombre:
            query = query.filter(Track.name.ilike(f"%{nombre}%"))
      if compositor:
            query = query.filter(Track.composer.ilike(f"%{compositor}%"))
      if id_album:
            query = query.filter(Track.albumid == id_album)
      canciones_filtradas = query.all()
      return render_template('tracks.html', tracks=canciones_filtradas)

if __name__ == '__main__':
      app.secret_key = 'super_secret_key'
      app.run(debug=True)
