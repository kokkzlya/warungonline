class CLI:
    def run_dev(self):
        from warungonline.app import create_app
        _app = create_app()
        _app.run(debug=True, port=5000)
