"""
contain the endpoint(blueprint), link with the store_index.html
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for
from models.store import Store
from models.user import requires_admin, requires_login

store_blueprint = Blueprint('stores', __name__)  # flask blueprint, just so it can be uniquely identified by flask


@store_blueprint.route('/')  # the index
@requires_login
def index():
    stores = Store.all()  # get all stores
    return render_template('stores/store_index.html', stores=stores)  # give the stores variable inside the template


@store_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def create_store():
    if request.method == 'POST':  # deal with form data, get variables, create a store and save them
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])  # take in string and turn it into a python dictionary

        Store(name, url_prefix, tag_name, query).save_to_mongo()

    # What happens if it's a GET request
    return render_template('stores/new_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    print(type(store))
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()

        return redirect(url_for('.index'))

    # What happens if it's a GET request
    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.index'))



