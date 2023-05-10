@echo on
for %%i in (50061,50063,50065,50067,50059) do ( 
    start cmd /k  "cd /d C:\Users\Karloz\Desktop\dipdl-master_2 && python C:\Users\Karloz\Desktop\dipdl-master_2\main.py 127.0.0.1:%%i %%i"
)