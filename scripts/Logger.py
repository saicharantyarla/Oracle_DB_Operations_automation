
"""A module contains all the common classes 
   used for logging
"""

import logging
import sys
import os
from datetime import date
#from Singleton import Singleton

#@Singleton
class Logger(object):

    """
     Rapper class implements logger functional to keep some more
     information such as module/function name and default logger name
    """

    def __init__(self,log_dir=None,log_name=None):

        log_file = self. __get_logfile(log_dir,log_name)
        logging.basicConfig(filename=log_file, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode = 'a', level=logging.DEBUG)
        logging.getLogger("paramiko").setLevel(logging.INFO)
        if not log_name:
            self.name = os.path.basename(sys.argv[0]).split('.')[0]
        else:
            self.name = log_name

    def add_new_logger(self, logger_name):
        """
        adds new loger name by default it is MSAT-LDAP
        """
        self.name = logger_name

    def _whoami(self):
        """
        detects name of the caller function for more
        eassy for the debugging
        """
        f_name = sys._getframe(2).f_code.co_name
        if self.name is not None:
            cls_name = self.name
        else:

            if 'self' in sys._getframe(2).f_locals:
                cls_name = sys._getframe(2).f_locals['self'].__class__.__name__
            else:
                cls_name = None
        return '{0}.{1}'.format(cls_name, f_name)


        return str(cls_name) +':'+ str(f_name)

    def __get_logfile(self,logdir,log_name):
        if not logdir.endswith('/'):
            logdir = logdir + '/'

        logdir = logdir + str( date.today())
        if not os.path.exists(logdir):
            try:
                os.makedirs(logdir)
            except OSError, e:
                raise ADLOGError("ADLOGError: Could not create Log directory %s-%s" %(logdir,e))

        #logfile = os.path.basename(sys.argv[0]).split('.')[0] + '.log'
        logfile = log_name
        file_path=logdir + '/' + logfile
        return file_path

    def info(self, msg):

        """
        function writes info to logfile
        """
        logging.info('{0}: {1}'.format(self._whoami(),str(msg)))

    def debug(self, msg):

        """
        function writes debug to logfile
        """
        logging.debug('{0}: {1}'.format(self._whoami(),str(msg)))

    def warning(self, msg):

        """
        function writes warning to logfile
        """
        logging.warning('{0}: {1}'.format(self._whoami(),str(msg)))

    def error(self, msg):

        """
        function writes error to logfile
        """
        logging.error('{0}: {1}'.format(self._whoami(),str(msg)))

    def exception(self, msg):

        """
        function writes exception  to logfile
        """
        logging.critical('{0}: {1}'.format(self._whoami(),str(msg)))
