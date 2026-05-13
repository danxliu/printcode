App runs on 15010 inside container, which gets forwarded to 127.0.0.1 on you host machine.
Nginx config exposes 15011 to OCF subnet and forward requests to 127.0.0.1:15010