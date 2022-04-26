import logging

handler = logging.FileHandler(filename="bot.log")

handler.setLevel(logging.INFO)

strfmt = '[%(asctime)s] [%(name)s] [%(levelname)s] >\n%(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=strfmt, datefmt=datefmt)

handler.setFormatter(fmt=formatter)