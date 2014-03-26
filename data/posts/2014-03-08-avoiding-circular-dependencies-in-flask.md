title: Avoiding circular Dependencies in Flask
date: 2014-03-08

`flask` is a compact python web framework that combines simplicity and speed of
development with a design that can scale when complexity grows.

`flask` documentation, however, is a little too eager to show off this
simplicity, and all the basic examples introduce practices that won't work when
your application grows from _tiny_ to _small_.


## Circularity

In its most basic form, a `flask` application lives inside a single file, a file
that looks like this:
    
    :::python
    app = Flask(__name__)
    db = SQLAlchemy(app)

    class Thing(db.Model):
        id = db.Column(db.Integer, primary_key = True)

    @app.route('/')
    def index():
        return 'Hello World!'

Note that both views and models (via `db` and `route()`) depend on the `app`
object.

When you attempt to move them into their own, separate files, you'll discover
that there's a circular dependency in both cases: `views` will need to import
`app` to use `route()`, and `app` will want to import `views` to set up those
routes. The same will happen with `models`, `app` and `db` objects needing each
other.


## Breaking the cycle

The `db` mutual dependency is easily solved by postponing the initialization
of the `db` object:

    :::python
    # models.py
    db = SQLAlchemy() # no `app` paramater

    # app.py
    from models import db
    db.init_app(app) # delayed initialization

Easy enough, no hacks involved. Same goes for the `route` dependency:

    :::python
    # views.py
    blueprint = Blueprint('views', __name__)

    @blueprint.route('/')
    def index():
        return 'Hello World!'

    # app.py
    from views import blueprint
    app.register_blueprint(blueprint)


## Closing thoughts

The `flask` documentation should be very clear about the right design pattern
for these cases. It's not. The amount of work required to do it right is so
minimal that I don't really see _why_ this is not mentioned early on.

As I said above, I think `flask` is _too proud_ of its simplicity. Too proud to
show you even the slightest level of complexity as you learn the framework.