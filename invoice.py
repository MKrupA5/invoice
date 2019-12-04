
from flask import Flask
import logging
import os

app = Flask(__name__)

logformat = '%(levelname)s %(module)s:%(lineno)d - %(message)s'
logfile = '/var/log/invoice/invoice.log'
logging.basicConfig(level=logging.DEBUG, filename=logfile, format=logformat)

@app.route('/')
def get_invoice():
    ver="1.0"
    res='{"Service":"Invoice", "Version":' + ver + '}\n'
    logging.info("Executed invoice with version %s", ver)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
