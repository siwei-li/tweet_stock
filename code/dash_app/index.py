from app import app

from tabs.tab2_callbacks import *
from tabs.tab1_callbacks import *


if __name__ == '__main__':
    app.config.suppress_callback_exceptions = True
    app.run_server(debug=True, port=8080)
    # code.run_server(debug=False, port=8080)