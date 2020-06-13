from flask import Flask, render_template, request, jsonify, make_response, json
from flask_cors import CORS
from pusher import pusher
import simplejson
import model

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher_client = pusher.Pusher(
  app_id='992139',
  key='31afc53fcb301efea29e',
  secret='5c0e949cc67e54f5c2bf',
  cluster='ap4',
  ssl=True
)

pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login/page')
def login():
    return render_template('log_in_page.html')

@app.route('/registration/page')
def registration():
    return render_template('registration_page.html')

@app.route('/registration/login/page')
def login_page():
    return render_template('log_in_page.html')

@app.route('/registration/login/login_page')
def login_login_page():
    return render_template('index.html')

@app.route('/new/guest', methods=['POST'])
def guestUser():
    data = request.json
    pusher.trigger(u'general-channel', u'new-guest-details', { 
        'name' : data['name'], 
        'email' : data['email']
            })
    return json.dumps(data)

@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
    return json.dumps(auth)

if __name__ == '__main__':
    app.run(port=5007)