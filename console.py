import sqlalchemy
import config

db_uri = config.db_dialect + "://"+ config.db_user + ':' + config.db_password + '@' + config.db_host +":"+ config.db_port + '/'+ config.db_name
print(db_uri)