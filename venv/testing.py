from ecapture import ecapture as ec
import datetime

x = datetime.datetime.now()
y = "img-" + x.strftime("%f") + ".jpg"

ec.capture(0, False, y)
