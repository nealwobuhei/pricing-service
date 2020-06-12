from flask import Blueprint, render_template, request, redirect, url_for, session
from models.alert import Alert
from models.item import Item
from models.store import Store
from models.user import requires_login

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@requires_login  # under route decorators
def index():
    """
    show us a list of alerts and present a template with that data
    """
    # print(session['email']) # need restart app, or will get keyerror:email
    alerts = Alert.find_many_by('user_email', session['email'])  # go to database find all alerts that have a property
    return render_template('alerts/index.html',
                           alerts=alerts)  # alerts come from the endpoint which are loaded in database


@alert_blueprint.route('/new', methods=['GET',
                                        'POST'])  # this blueprint now have endpoint inside it, define an endpoint to receive data, access get and post
@requires_login
def new_alert():
    """
    browser make a get request when access endpoint, endpoint will be respond to it with the html be rendered
    if receive a post request which is the form is gonna make, to take the data in form and process it
    """
    if request.method == 'POST':
        alert_name = request.form['name']
        price_limit = float(request.form['price_limit'])
        item_url = request.form['item_url']  # access the url field in the form data that's come in the request
        # such as: http://www.johnlewis.com/item/index.html

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()  # when they go to alerts.index page, item will have a price, don't need call load price on it
        item.save_to_mongo()

        Alert(alert_name, item._id, price_limit, session['email']).save_to_mongo()

    return render_template('alerts/new_alert.html')


@alert_blueprint.route("/edit/<string:alert_id>", methods=["GET", "POST"])  # htttp://www.sasds.com/alerts/edit/_id
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)

    if request.method == "POST":
        price_limit = float(request.form["price_limit"])

        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(
            url_for(".index"))  # it calculates the URL to go to this index method inside the current blueprint

    # What happens if it's a GET request
    return render_template('alerts/edit_alert.html', alert=Alert.get_by_id(alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@requires_login  # this decorator will prevent users from accessing these pages unless they are logged in
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session['email']:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))
