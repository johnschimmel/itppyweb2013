from app import app
from admin import admin_pages

app.register_blueprint(admin_pages)

if __name__ == "__main__":
	app.run()