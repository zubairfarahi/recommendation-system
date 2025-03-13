import traceback
import sys


class CustomException(Exception):

    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

        self.error_message = self.get_detailed_error_message(error_message, error_details)
    
    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        
        _, _, exec_tb = traceback.sys.exc_info()
        file_name = exec_tb.tb_frame.f_code.co_filename
        line_number = exec_tb.tb_lineno

        return f'Error in {file_name}, line {line_number} : {error_message}'

    def __str__(self):
        return self.error_message