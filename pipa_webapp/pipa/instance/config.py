# instance/config.py

SECRET_KEY = 'p9Bv<3Eid9%$i01'

# use for local development
# SQLALCHEMY_DATABASE_URI = 'mysql://pipa_admin:pipa2017@localhost/pipa_db'

# use for when running on pythonanywhere.com 
SQLALCHEMY_DATABASE_URI = 'mysql://pipa:piparoot@pipa.mysql.pythonanywhere-services.com/pipa$pipa_db'
