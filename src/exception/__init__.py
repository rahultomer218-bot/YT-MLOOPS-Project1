import sys

class MyException(Exception):
    """
    Custom Exception class jo error ki 
    detail file name aur line number ke saath deti hai.
    """

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)

        self.error_message = self.get_detailed_error_message(
            error_message=error_message,
            error_detail=error_detail
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys) -> str:
        """
        Error ki poori detail nikalta hai —
        konsi file mein, konsi line par error aaya.
        """
        _, _, exc_tb = error_detail.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        error_message = (
            f"\n\nError occurred in Python script:"
            f"\n👉 File Name : [{file_name}]"
            f"\n👉 Line Number: [{line_number}]"
            f"\n👉 Error Message: [{error_message}]"
        )

        return error_message

    def __str__(self):
        return self.error_message

# ✅ Yeh line add karo — demo.py ka import fix ho jayega
CustomException = MyException
CustomException = MyException
VehicleException = MyException