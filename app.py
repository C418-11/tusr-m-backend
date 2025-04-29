# -*- coding: utf-8 -*-


import os

from app import create_app


def main():
    app = create_app()
    ssl_context = (
        app.config['SSL_CERTIFICATE'],
        app.config['SSL_PRIVATE_KEY']
    ) if os.path.exists(app.config['SSL_CERTIFICATE']) else None
    app.run(host='0.0.0.0', ssl_context=ssl_context)


if __name__ == "__main__":
    main()

__all__ = ("main",)
