from app import app
from admin import admin_pages

app.register_blueprint(admin_pages, url_prefix='/admin')

if __name__ == "__main__":
	app.run()