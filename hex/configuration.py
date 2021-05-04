import os

import inject

from hex.adapters.database.postgres import PostgresAdapter
from hex.domain.database_interface import DatabaseInterface


def configure_inject() -> None:
    def config(binder: inject.Binder) -> None:
        binder.bind(DatabaseInterface, PostgresAdapter(os.getenv('DATABASE_URI')))

    inject.configure(config)
