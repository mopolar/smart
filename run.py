from flask import Flask
from smartshorter import config
from smartshorter.shortner import shortner
from smartshorter.errors import errors



app = Flask(__name__)


app.register_blueprint(shortner)
app.register_blueprint(errors)

if __name__ == '__main__':
	app.run(debug=True, port=config.PORT)