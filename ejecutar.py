from cx_Freeze import setup, Executable

setup( name = "CifrarPDF",
           version = "0.1" ,
           description = "CifrarPDF" ,
           executables = [Executable("cifrarpdf.py")] , )