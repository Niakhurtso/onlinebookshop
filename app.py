from ext import app, login_manager

login_manager.init_app(app)

if __name__ == "__main__":
    from routes import *
    app.run(debug=True)
