# This script uses the cryptography library to generate an elliptic curve (EC) private key and then creates a self-signed X.509 certificate. 
# The generated private key is saved in the private_key.pem file, and the certificate is saved in the certificate.pem file.
# You can modify the subject and issuer variables to customize the certificate's details according to your requirements. 
# Additionally, you can change the cryptographic algorithm from ec.SECP256R1() to rsa.generate_private_key() to use the RSA algorithm instead.
# Remember to install the cryptography library if you haven't already. You can do so by running pip install cryptography.
# Please note that self-signed certificates are not typically suitable for production use. In real-world scenarios, it is recommended
# to obtain certificates from a trusted certificate authority (CA).

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

# Generate a private key
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# Create a self-signed certificate
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'California'),
    x509.NameAttribute(NameOID.LOCALITY_NAME, 'San Francisco'),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'Example Company'),
    x509.NameAttribute(NameOID.COMMON_NAME, 'example.com')
])
public_key = private_key.public_key()
builder = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
builder = builder.not_valid_before(datetime.datetime.utcnow())
builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
builder = builder.serial_number(x509.random_serial_number())
builder = builder.public_key(public_key)
builder = builder.add_extension(
    x509.BasicConstraints(ca=False, path_length=None), critical=True,
)
certificate = builder.sign(private_key, hashes.SHA256(), default_backend())

# Write the private key and certificate to files
with open('private_key.pem', 'wb') as private_key_file:
    private_key_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open('certificate.pem', 'wb') as certificate_file:
    certificate_file.write(certificate.public_bytes(serialization.Encoding.PEM))
