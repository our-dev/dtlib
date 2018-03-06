import logging
import sys

urllib_log_tag = 'requests.packages.urllib3.connectionpool'  # 所有的requests里面的logger的标识
urllib_log_tag_old = 'urllib3.connectionpool'  # 旧的requests里面的logger标识

# just for debug time
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="[%(asctime)s] (%(name)s):%(filename)s:%(funcName)s-(%(lineno)d)%(levelname)s: %(message)s",
    # format="[%(asctime)s] (%(name)s):%(pathname)s:%(filename)s:%(funcName)s-(%(lineno)d)%(levelname)s: %(message)s"
)


def init_logging():
    """
    初始化logging信息
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')
    sh.setFormatter(formatter)

    logger.addHandler(sh)
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


dlog = logging.getLogger('dlog')

if __name__ == "__main__":
    dlog.debug("hello world")
