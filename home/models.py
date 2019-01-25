from application import db


class report_yearly(db.Document):
    stock_id = db.StringField(db_field="sid", max_length=10, required=True)
    data = db.DictField()
    report_name = db.StringField(db_field="rn", max_length=4, required=True)
    companyName = db.StringField(db_field="cn", max_length=160, required=True)
    companyNameEng = db.StringField(db_field="cne", max_length=160, required=True)
    industryName = db.StringField(db_field="indn", max_length=100, required=True)
    floor = db.StringField(db_field="floor", max_length=5, required=True)
    shares = db.LongField(db_field="share", max_value=10000000000, required=True)
    meta = {
        'indexes': ['stock_id', ('stock_id', 'report_name')]
    }


class report_quaterly(db.Document):
    stock_id = db.StringField(max_length=10, required=True)
    data = db.DictField()
    report_name = db.StringField(max_length=4, required=True)
    meta = {
        'indexes': ['stock_id', ('stock_id', 'report_name')]
    }


class stock_price(db.Document):
    stock_id = db.StringField(max_length=20, required=True, unique=True)
    data = db.DictField()
    meta = {
        'indexes': ['stock_id']
    }
