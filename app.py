from project import app

print(app.config['SQLALCHEMY_DATABASE_URI'], "here is the local database info")

if __name__ == "__main__":
    app.run(debug = True)