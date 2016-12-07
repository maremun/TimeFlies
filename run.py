#!/usr/bin/env python3
#   encoding: utf8
#   run.py

from timeflies.app import app
from timeflies.settings import DEBUG

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=DEBUG)
    
