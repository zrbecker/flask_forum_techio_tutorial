from helloflask import app
import sys

if __name__ == '__main__':
    print('HELLO 1', file=sys.stderr, flush=True)
    print('TECHIO> open -p 5000 /')
    print('HELLO 2', file=sys.stderr, flush=True)
    app.run(port=5000)
