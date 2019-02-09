from flaskblog import create_app

app = create_app('flaskblog.settings.ProdConfig')


if __name__ == "__main__":
    app.run()