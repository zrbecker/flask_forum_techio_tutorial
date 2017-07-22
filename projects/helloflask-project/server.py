from helloflask import app
import sys

if __name__ == '__main__':
    print('HELLO 1', file=sys.stderr, flush=True)
    print('TECHIO> open --port 8080 /', flush=True)
    print('HELLO 2', file=sys.stderr, flush=True)
    app.run(port=5000)
