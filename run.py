import os
from apmcs import app

port = int(os.getenv('VCAP_APP_PORT', 8080))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=port)
