from helloflask import app

if __name__ == '__main__':
    print('TECHIO> open --port 5000 /', flush=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
