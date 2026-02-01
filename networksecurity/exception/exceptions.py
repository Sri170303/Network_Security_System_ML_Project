import sys
from networksecurity.logging import logger

class NetworkSecurityError(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,exec_tb = error_details.exc_info()

        self.lineno = exec_tb.tb_lineno
        self.filename = exec_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in python script name [{self.filename}] line number [{self.lineno}] error message [{self.error_message}]"
    

if __name__ == "__main__":
    try:
        logger.logging.info("Entered in try block")
        a = 1 / 0
    except Exception as e:
        raise NetworkSecurityError(e, sys)