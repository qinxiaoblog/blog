from __future__ import absolute_import, division, unicode_literals
import sys
import logging
import threading
import multiprocessing
from logging import Handler, StreamHandler
from logging.handlers import TimedRotatingFileHandler
import traceback
# from flask.logging import default_handler


__all__ = ['init_logger', 'logger']


try:
    import queue
except ImportError:
    # Python 2.0.
    import Queue as queue


def install_mp_handler(logger=None):
    """Wraps the handlers in the given Logger with an MultiProcessingHandler.
    :param logger: whose handlers to wrap. By default, the root logger.
    """
    if logger is None:
        logger = logging.getLogger()
    for i, orig_handler in enumerate(list(logger.handlers)):
        handler = MultiProcessingHandler(
            'mp-handler-{0}'.format(i), sub_handler=orig_handler)
        logger.removeHandler(orig_handler)
        logger.addHandler(handler)


class MultiProcessingHandler(Handler):
    def __init__(self, name, sub_handler=None):
        super(MultiProcessingHandler, self).__init__()
        if sub_handler is None:
            sub_handler = StreamHandler()
        self.sub_handler = sub_handler
        self.setLevel(self.sub_handler.level)
        self.setFormatter(self.sub_handler.formatter)
        self.queue = multiprocessing.Queue(-1)
        self._is_closed = False
        # The thread handles receiving records asynchronously.
        self._receive_thread = threading.Thread(
            target=self._receive, name=name)
        self._receive_thread.daemon = True
        self._receive_thread.start()

    def setFormatter(self, fmt):
        super(MultiProcessingHandler, self).setFormatter(fmt)
        self.sub_handler.setFormatter(fmt)

    def _receive(self):
        while not (self._is_closed and self.queue.empty()):
            try:
                record = self.queue.get(timeout=0.2)
                self.sub_handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except queue.Empty:
                pass  # This periodically checks if the logger is closed.
            except:
                traceback.print_exc(file=sys.stderr)
        self.queue.close()
        self.queue.join_thread()

    def _send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified. Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe.
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            self.format(record)
            record.exc_info = None
        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self._send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        if not self._is_closed:
            self._is_closed = True
            self._receive_thread.join(5.0)  # Waits for receive queue to empty.
            self.sub_handler.close()
            super(MultiProcessingHandler, self).close()


def init_logger(logfile="/tmp/test.log", loglevel=logging.INFO,
                file=True, console=True):
    # 此变量作为导出的 logger 实例
    _logger = logging.getLogger('blog.log')

    _logger.setLevel(loglevel)
    fmt = logging.Formatter(
        f'%(asctime)s %(filename)s[line:%(lineno)d] '
        f'%(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 根据时间来切分日志文件，when可选值：M H D midnight
    file_handler = TimedRotatingFileHandler(
        logfile, when="midnight", interval=1, backupCount=3)
    file_handler.setFormatter(fmt)

    # 控制台 handler
    stream_handler = StreamHandler(sys.stderr)
    stream_handler.setFormatter(fmt)

    # _logger.addHandler(default_handler)
    if file:
        _logger.addHandler(file_handler)
    if console:
        _logger.addHandler(stream_handler)

    if not file and not console:
        raise Exception('file=True or console=True!')

    # 如果是多进程、多线程则打开此注释
    install_mp_handler(_logger)

    return _logger


logger = logging.getLogger('blog.log')


if __name__ == '__main__':
    init_logger(logfile='/tmp/ycs.log', loglevel=logging.DEBUG)
    logger.debug('debug.')
    logger.info('info.')
    logger.warning('warning.')
    logger.error('error.')
    logger.critical('critical.')
