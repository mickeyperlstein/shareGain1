from random import random

DAY_OF_WEEK = 'DayOfWeek'
RANGE = 'range'
METER_SQUARED = 'MeterSquared'
TIME = 'time'
BULK = 'bulk'


class Entity:

    def __init__(self, id, name):
        if id is None:
            self.id = random.Random().randint(0, 1000000)
        else:
            self.id = id

        self.name = name

    def as_dict(self):
        # return {c.name: getattr(self, c.name)
        #         for c in self.__table__.columns}
        return self.__dict__

    def __repr__(self):
        return f'<{str(type(self).__name__)} id={self.id}|name={self.name}|unit_of_measure={self.unit}>'


class Rule(Entity):
    """
    >>> Rule.load({'id': 100, 'name': 'Cheaper on Thursdays', 'service_id': 1, 'unit': DAY_OF_WEEK, 'value': 'Thursday', 'multiplier': 0.9},)
    <Rule id=100|name=Cheaper on Thursdays|unit_of_measure=DayOfWeek>
    """

    def __init__(self, id, name, service_id, unit, value, multiplier):
        super().__init__(id, name)
        self.service_id = service_id
        self.unit = unit
        self.value = value
        self.multiplier = multiplier

    def load(dic):
        svc = Rule(**dic)
        return svc


class Service(Entity):
    """

    >>> s = Service(id= 2, name= 'House cleaning', unit=METER_SQUARED)
    >>> s.as_dict()
    {'id': 2, 'name': 'House cleaning', 'unit': 'MeterSquared'}

    """

    def load(dic):
        svc = Service(**dic)
        return svc

    def __init__(self, id, name, unit):
        super().__init__(id, name)
        self.name = name
        self.unit = unit


class Offering(Entity):
    """
        >>> Offering.load({"id": 4, 'service_id': 1, "name": "30 min private lesson", "unit": TIME, "price": 20})
        <Offering id=4|name=30 min private lesson|price=20>

        >>> Offering.load( {'id': 7, 'price_id': 4, 'amount': 5, "name": "pack of 5 - 30 minute private lessons", "unit": BULK, "price": 35})
        <Offering id=7|name=pack of 5 - 30 minute private lessons|price=35>
    """

    def load(dic):
        # if dic.get('')
        svc = Offering(**dic)
        return svc

    def __init__(self, id, name,  price, unit, unit_size=0, amount=1, service_id=None, price_id=None, value=None):
        super().__init__(id, name)
        self.price = price
        self.service_id = service_id
        self.unit = unit
        self.price_id = price_id
        self.amount = amount
        self.value = value
        self.unit_size = unit_size

    # criterion_date = db.Column(db.String(60), nullable=False)

    # percent_change = db.Column(db.Integer, nullable=False)
    #
    # service_id = db.Column(db.Integer, db.ForeignKey('service_base.id'), nullable=False)
    # service = db.relationship('service_base', backref=db.backref('discounts', lazy=True))

    def __repr__(self):
        return f'<Offering id={self.id}|name={self.name}|price={self.price}>'


class RangeOffering(Offering):
    def __init__(self, id, name, price, unit, unit_size=0, amount=1, service_id=None, price_id=None, value=None):
        super().__init__(id, name, price, unit, unit_size)

