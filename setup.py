from cx_Freeze import setup, Executable

setup(
        name = "Pinp",
        version = "0.6",
        description = "PINP Is Not P2P",
        executables = [Executable("main.py")])
