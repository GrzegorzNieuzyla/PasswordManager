from OpenSSL import crypto


def generate_certificate(cert_file: str, key_file: str) -> None:
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = "PL"
    cert.get_subject().ST = " "
    cert.get_subject().L = " "
    cert.get_subject().O = "Password Manager"
    cert.get_subject().OU = "Password Manager"
    cert.get_subject().CN = "Password Manager"
    cert.get_subject().emailAddress = "@"
    cert.set_serial_number(0)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(cert_file, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(key_file, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
