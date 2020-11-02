import os
from api.hetionet import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=os.getenv('API_PORT'))