import contextlib
from sqlalchemy import create_engine
from parameters import USER, PASSWORD, SERVICE_NAME


@contextlib.contextmanager
def get_oracle_conn():
    """
    Context manager to automatically close DB connection.
    :return: None
    """
    engine = create_engine(f'oracle://{USER}:{PASSWORD}@{SERVICE_NAME}')
    connection = engine.connect()

    try:
        yield connection
    finally:
        connection.close()
