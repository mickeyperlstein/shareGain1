from flask import Flask, jsonify, request
import os
from repositories.repository import Repository
from adapters.price_calculator import PriceCalculator, TimePriceCalculator, SquareMetersPriceCalculator
import dateparser

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
repo = Repository()
calculators = {TimePriceCalculator(), SquareMetersPriceCalculator()}

def list_routes():
    import urllib
    output = []
    rules = list(app.url_map.iter_rules())
    rules.extend(['/api/prices/4/7/11-08-2022', '/api/prices/4/7/9-08-2022'])

    for rule in rules:
        if str(rule).find('static') == -1:
            line = urllib.parse.unquote(f'<BR> <a href="{request.base_url[:-1]}{rule}"> {request.base_url[:-1]}{rule} </a>')
            output.append(line)


    return output

@app.route('/')
def health():
    return '<HR><h2>Welcome to the server' + '<HR></BR>' + str(list_routes())


@app.route('/api/services/')
def get_services():
    try:
        return jsonify(repo.get_services())
    except Exception as e:
        return f'Error: {str(e)}'


@app.route('/api/services/<id>', methods=['GET'])
def get_service(id):
    x = repo.get_service_by_id(id)
    return jsonify(x)


@app.route('/api/prices/<offering_id>/<amount>/<start_date>')
def price_service(offering_id, start_date, amount):
    try:

        dt_obj = dateparser.parse(start_date)
        pricings = repo.calculate_price(offering_id, dt_obj, int(amount))
        return jsonify(pricings)
    except ValueError as ve:
        return jsonify(str(ve))
    except Exception as e:
        return jsonify(str(e))



if __name__ == '__main__':
    app.run(debug=True)
