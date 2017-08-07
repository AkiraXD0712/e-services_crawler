import logging

'''
Create logger
'''
logger = logging.getLogger("e-services_crawler")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('crawler_log')
fh.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s -%(levelname)s -%(message)s")
fh.setFormatter(formatter)
sh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(sh)


def setDebug():
    logger.removeHandler(sh)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)