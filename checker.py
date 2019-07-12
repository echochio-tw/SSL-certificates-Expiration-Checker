#!/usr/bin/python3
import socket
import ssl
import datetime

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
def ssl_valid_time_remaining(hostname):
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.utcnow()

def ssl_expires_in(hostname, buffer_days=20):
    remaining = ssl_valid_time_remaining(hostname)
    if remaining < datetime.timedelta(days=0):
        raise AlreadyExpired("Cert expired %s days ago" % remaining.days)
    elif remaining < datetime.timedelta(days=buffer_days):
        return True
    else:
        return False
print (ssl_expires_in(google.com))
print (ssl_expires_in(google.com), buffer_days=10)
