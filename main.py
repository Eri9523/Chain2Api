from launcher import create_app
from di import global_injector

app = create_app(global_injector)
