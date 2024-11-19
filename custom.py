from unittest import TestLoader, TextTestResult, TextTestRunner
from colorama import init, Fore, Style
import sys
import os
from itertools import cycle
from io import StringIO

init(autoreset=True)

class CustomResult(TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.current_class = None
        self._stdout_original = sys.stdout
        self._stdout_capture = StringIO()

    def startTest(self, test):
        test_class_name = test.__class__.__name__
        if self.current_class != test_class_name:
            self.current_class = test_class_name
            self.stream.write(f"\n{Fore.YELLOW}[{test_class_name} Tests]{Style.RESET_ALL}\n")

        # Redirect stdout to capture print statements
        sys.stdout = self._stdout_capture

        # Display spinner for visual indication
        sys.stdout.flush() 
   
    def stopTest(self, test):
    # Custom success message without '... ok', with captured output if any
        captured_output = self._stdout_capture.getvalue().strip()
        message = f"{Fore.LIGHTMAGENTA_EX}{test.id().split('.')[-1]}{Fore.LIGHTBLUE_EX} PASSED"
        if captured_output:
            message += f"{Fore.CYAN} - {captured_output}{Style.RESET_ALL}"
        else:
            message += Style.RESET_ALL  # Reset color if no output

        self.stream.write(message + '\n')
        self.stream.flush()

        # Restore original stdout
        sys.stdout = self._stdout_original

        # Clear the capture buffer
        self._stdout_capture.truncate(0)
        self._stdout_capture.seek(0)

    def addSuccess(self, test):
        # Custom success message without '... ok' 
        self.stream.flush()

if __name__ == '__main__':
    print(f"Running in directory: {os.getcwd()}")  # Check your current working directory
    loader = TestLoader()
    suite = loader.discover('src', pattern='test*.py')  # Make sure your tests match this pattern
    runner = TextTestRunner(resultclass=CustomResult, verbosity=2)
    result = runner.run(suite)

