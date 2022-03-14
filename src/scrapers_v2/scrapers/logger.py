import logging

LOG_FILE_PATH ='/home/$USER/big_dump.log'
logger_name = ""


def get_logger(name):
    log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s %(module)s'    #formatting the log output
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        filename='Output.log',
                        filemode="w")

    console = logging.StreamHandler()
    #console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)     #Handlers are used for management purposes over the log file

    #handler = TimedRotatingFileHandler(LOG_FILE_PATH, when="m",
    # #Log file is cleared and renewed on further running to keep log file relevant ie every hour
    #                                   interval=1, backupCount=5)
    #logging.getLogger(name).addHandler(handler)

    return logging.getLogger(name)
