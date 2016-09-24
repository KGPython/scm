__author__ = 'admin'
import base.utils.MethodUtil as mth
def index(req):
    numbers = 49962.01
    upp = mth.rmbupper(numbers)
    print(upp)
    return upp
