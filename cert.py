import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def get_certificate_details(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        domain = urlparse(url).netloc
        if not domain:
            domain = url.split('/')[0]
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(10)
        conn.connect((domain, 443))

        context = ssl.create_default_context()
        connection = context.wrap_socket(conn, server_hostname=domain)

        cert = connection.getpeercert()
        pem_cert = ssl.DER_cert_to_PEM_cert(connection.getpeercert(binary_form=True))

        not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
        not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        today = datetime.now()
        days_remaining = (not_after - today).days
        
        status = "Valid" if days_remaining > 0 else "Expired"
        
        issuer = dict(x[0] for x in cert['issuer']) if 'issuer' in cert else {}
        issuer_org = issuer.get('organizationName', 'Unknown') if isinstance(issuer, dict) else 'Unknown'
        
        connection.close()
        
        return {
            'not_before': not_before.strftime('%Y-%m-%d'),
            'not_after': not_after.strftime('%Y-%m-%d'),
            'status': status,
            'issuer': issuer_org,
            'days_remaining': days_remaining,
            'error': None
        }
    except Exception as e:
        return {
            'not_before': 'N/A',
            'not_after': 'N/A',
            'status': 'Error',
            'issuer': 'N/A',
            'days_remaining': 'N/A',
            'error': str(e)
        }