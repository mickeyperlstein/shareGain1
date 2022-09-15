import math
from datetime import date

from models.models import *

DAY_OF_WEEK = 'DayOfWeek'
RANGE = 'range'
METER_SQUARED = 'MeterSquared'
TIME = 'time'
BULK = 'bulk'


class Repository:
    db = {
        'services': [{'id': 1, 'name': 'private lesson', 'unit': TIME},
                     {'id': 2, 'name': 'House cleaning', 'unit': METER_SQUARED}
                     ],
        'pricing': [{"id": 4, 'service_id': 1, "name": "30 min private lesson", "unit": TIME, "price": 20},
                    {'id': 6, 'service_id': 1, "name": "60 min private lesson", "unit": TIME, "price": 35},
                    {'id': 7, 'price_id': 4, 'amount': 5,
                     "name": "pack of 5 - 30 minute private lessons", "unit": BULK, "price": 35},

                    {'id': 70, "service_id": 2, "name": "Appartment cleaning - up to 50 meters squared",
                     'unit': METER_SQUARED, "price": 50},

                    {'id': 71, "price_id": 70, 'unit': RANGE, 'value': (50, 100),
                     'unit_size': 10, 'price': 10, 'name': 'range 50 - 100 Sqm'},

                    {'id': 72, "price_id": 70, 'unit': RANGE, 'value': (100, 200),
                     'unit_size': 10, 'price': 15, 'name': 'range 100 - 200 Sqm'},
                    ],
        'rules': [{'id': 100, 'service_id': 1, 'name': 'Cheaper on Thursdays',  'unit': DAY_OF_WEEK, 'value': 'Thursday', 'multiplier': 0.9},
                  {'id': 101, 'service_id': 2, 'name': 'Cheaper on Saturdays', 'unit': DAY_OF_WEEK, 'value': 'Saturday', 'multiplier': 1.2},
                  ]

    }

    def __init__(self):
        self.services = [
            Service.load(x) for x in self.db['services']
        ]

        self.rules = [
            Rule.load(x) for x in self.db['rules']
        ]

        self.offerings = [
            Offering.load(x) for x in self.db['pricing']
        ]


    def get_all_rules_for_service(self, service_id):
        """
        >>> repo = Repository()
        >>> repo.get_all_rules_for_service(1)
        [{'id': 100, 'service_id': 1, 'criterion': 'DayOfWeek', 'value': 'Thursday', 'multiplier': 0.1}]
        """
        rules = list(
            filter(lambda x: str(service_id) == str(x.service_id),
                   self.rules))


        return rules

    def get_offerings_for_service(self, service_id):
        """
        >>> repo = Repository()
        >>> repo.get_offerings_for_service(2)
        [{'id': 70, 'service_id': 2, 'name': 'Appartment cleaning - up to 50 meters squared', 'unit': 'MeterSquared', 'price': 50.0}, {'id': 71, 'price_id': 70, 'criterion': 'range', 'criterion_value': (50, 100), 'unit_size': 10, 'price': 10}, {'id': 72, 'price_id': 70, 'criterion': 'range', 'criterion_value': (100, 200), 'unit_size': 10, 'price': 15}]

        """
        pricings = list(
            map(lambda f: f
                , filter(lambda x: str(x.get('service_id')) == str(service_id),
                         self.db['pricing'])
                )
        )
        all_bulks = []
        for price_item in pricings:
            bulks = list(
                map(lambda f: f
                    , filter(lambda x: str(x.get('price_id')) == str(price_item.get('id')),
                             self.db['pricing'])
                    )
            )
            all_bulks.extend(bulks)
        pricings.extend(all_bulks)
        return pricings

    def get_offerings(self, offering_id):
        """
        >>> repo = Repository()
        >>> repo.get_offerings(70)
        [{'id': 70, 'service_id': 2, 'name': 'Appartment cleaning - up to 50 meters squared', 'unit': 'MeterSquared', 'price': 50.0}, {'id': 71, 'price_id': 70, 'criterion': 'range', 'criterion_value': (50, 100), 'unit_size': 10, 'price': 10}, {'id': 72, 'price_id': 70, 'criterion': 'range', 'criterion_value': (100, 200), 'unit_size': 10, 'price': 15}]

        """
        pricings = list(
            map(lambda f: f
                , filter(lambda x: str(x.get('id')) == str(offering_id),
                         self.db['pricing'])
                )
        )
        all_bulks = []
        for price_item in pricings:
            bulks = list(
                map(lambda f: f
                    , filter(lambda x: str(x.get('price_id')) == str(price_item.get('id')),
                             self.db['pricing'])
                    )
            )
            all_bulks.extend(bulks)

        all_bulks.extend(pricings)
        return all_bulks

    def get_service_id_from_offerings(self, offerings):

        pricings = filter(lambda x: len(str(x.get('service_id', ''))) > 0, offerings)

        return list(pricings)[0].get('service_id')

    def get_discount(self, start_date, service_id, default=1):
        """
        >>> repo = Repository()
        >>> repo.get_discount(date(2021,12,18), 2, default=1)
        1.2
        >>> repo.get_discount(date(2021,12,16), 1, default=1)
        0.9
        """

        rules = self.get_all_rules_for_service(service_id)
        dow = str(start_date.strftime("%A"))

        for rule in rules:
            if rule.unit == DAY_OF_WEEK:
                if dow == rule.value:
                    return float(rule.multiplier)
        return default

    def calculate_price(self, offering_id, start_date, amount=3):
        """

        >>> mydate = date(2021,12,18)
        >>> repo = Repository()
        >>> repo.calculate_price(4, mydate, 7 )
        75

        >>> mydate = date(2021,12,16) # Thursday
        >>> repo.calculate_price(offering_id=4, start_date=mydate, amount=7 )
        67.5

        # >>> repo.calculate_price(71, mydate, 100)
        # 40
        """

        offerings = self.get_offerings(offering_id)
        regular_left = calcd_price = 0
        bulk_size = 1

        for regular_offer in filter(lambda x: x.get('unit') in {BULK, RANGE}, offerings):
            if regular_offer.get('unit') == BULK:
                bulk_size = int(regular_offer.get('amount'))
                number_of_bulks = math.floor(amount / bulk_size)
                bulk_price = regular_offer.get('price')

                calcd_price = number_of_bulks * bulk_price

            elif regular_offer.get('unit') == RANGE:
                start = regular_offer.get('value')[0]
                end = regular_offer.get('value')[1]

                if amount >= start  < end:
                    # range
                    pass

            regular_left = amount % bulk_size
            offerings.remove(regular_offer)
        service_id = self.get_service_id_from_offerings(offerings)
        if regular_left > 0:
            regular_offer = offerings[0]
            unit_price = regular_offer.get('price')
            calcd_price += unit_price * regular_left

        multiplier = self.get_discount(start_date, service_id=service_id)
        return calcd_price * multiplier

    def get_services(self):
        return [service for service in self.db['services']]

    def get_service_by_id(self, id):
        f1 = filter(lambda x: str(x.get('id')) == str(id), self.db['services'])
        return list(f1)
