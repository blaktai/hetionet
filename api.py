import os
from api.hetionet import app
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('API_PORT'))