from datetime import datetime
from pytz import timezone

def tprint(s):
        ist = timezone('Asia/Kolkata')
        print datetime.now(ist).strftime("[ %Y-%m-%d %H:%M:%S.%f ]"),
        print s
