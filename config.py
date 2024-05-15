class Config:
    SECRET_KEY = 'your_secret_key'
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'mysql://root:your_MySQL_password@your_host_name/your_database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
#please fill in your_MySQL_password, your_host_name and your_database_name
#example: mysql://root:xiaomingumich1099@127.0.0.1:3306/flaskdb
