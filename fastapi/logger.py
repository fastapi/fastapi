import logging

logger = logging.getLogger("fastapi")

if platform.system() == "Windows":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
