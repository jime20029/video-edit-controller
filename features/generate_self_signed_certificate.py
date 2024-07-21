from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
from Crypto.Hash import SHA256

# 自己署名証明書の生成
def generate_self_signed_certificate(private_key):
    # 秘密鍵から公開鍵を取得
    public_key = private_key.public_key()

    # 証明書のsubjectとissuerを設定
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"JP"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Osaka"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Osaka"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"xxxxx"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"xxxxx.com"),
    ])

    # 自己署名証明書を生成
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # 証明書の有効期限を1年後に設定
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        # Subject Alternative Nameを追加
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(private_key, SHA256())

    return cert
