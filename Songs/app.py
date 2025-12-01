from backend import app

if __name__ == '__main__':  # Script executed directly?
    print("songs application.")

    # Launches built-in web server and run this Flask webapp
    app.run(host="0.0.0.0", port=8000, debug=True, use_reloader=True)
