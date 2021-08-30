Instrusction:
1. git clone https://github.com/Lzimng/Booking.git

2. From the root dir, execute (Windows User):
python run.py

3. The webapp will be hosted on 127.0.0.1:5000


For Docker user:
1. Build image:
docker build . -t booking_webapp  

2. Run image:
docker run -p 5000:5000 booking_webapp

3. The webapp will be hosted on 127.0.0.1:5000


