import http.server
import ssl
import os
import subprocess

# 1. Generate a temporary self-signed SSL certificate
certfile = "cert.pem"
keyfile = "key.pem"

if not os.path.exists(certfile):
    print("[-] Creating Secure SSL Certificates for your Mobile Sync...")
    try:
        # We use openssl command line which is usually bundled with Git Bash on Windows
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-keyout', keyfile, '-out', certfile, '-days', '365', '-nodes', '-subj', '/CN=localhost'], check=True)
    except:
        # Fallback if OpenSSL command is missing: Tell user, but Python ssl setup below will fail safely
        print("[ERROR] OpenSSL command not found in path. Please install Git or utilize Chrome Flags workaround.")

# 2. Boot standard HTTPS Server
server_address = ('0.0.0.0', 8443)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Wrap server socket in SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile, keyfile)
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("\n" + "="*50)
print(f"🔒 SECURE TACTICAL SERVER ACTIVE ON PORT 8443")
print("Go to your Mobile Browser and type this exactly:")
print("👉 https://192.168.12.159:8443")
print("\n(Note: Your phone will say 'Connection Not Private' - Tap 'ADVANCED' and 'PROCEED' to enter!)")
print("="*50)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[!] Shutting down secure server.")
