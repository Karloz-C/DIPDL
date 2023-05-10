import hashlib
import re
pat = r'[A-Z0-9]{64}'
from subprocess import run
def signing(data):
    p1 = run(['./ringsign.exe', '4', '50061', '0', hashlib.md5(data).hexdigest()], capture_output=True,check=True)
    sign = re.findall(r'[A-Z0-9]{64}',str(p1.stdout))
    sign = [int(i,16) for i in sign]
    return sign

signing('hello'.encode())