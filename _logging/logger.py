# http://uran198.github.io/en/python/2016/07/12/colorful-python-logging.html
import logging
import copy

import ansi

LOG_COLORS = {
    logging.ERROR: ansi.Fore.RED,
    logging.WARNING: ansi.Fore.YELLOW,
    logging.INFO: ansi.Fore.GREEN,
    logging.DEBUG: ansi.Fore.BLUE
}


class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        # if the corresponding logger has children, they may receive modified
        # record, so we want to keep it intact
        new_record = copy.copy(record)

        # we want levelname to be in different color, so let's modify it
        new_record.levelname = "{color_begin}{level}{color_end}".format(
            level=new_record.levelname,
            color_begin=LOG_COLORS[new_record.levelno],
            color_end=ansi.Style.RESET_ALL,
        )

        if new_record.threadName != "MainThread":
            new_record.msg = "{} {}".format(
                new_record.threadName, new_record.msg
            )
        # now we can let standart formatting take care of the rest
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)


def setup_logger(level_no=logging.DEBUG,
                 format_string="%(levelname)s %(message)s"):
    # we want to display only levelname and message
    formatter = ColorFormatter(format_string)

    # this handler will write to sys.stderr by default
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # adding handler to our logger
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(level_no)
    return logger
