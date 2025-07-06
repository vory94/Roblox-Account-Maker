from curl_cffi import requests
from base64 import b64encode
from time import time
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

class AuthIntent:
    @staticmethod
    def string_to_bytes(raw_string) -> bytes:
        return bytes(raw_string, 'utf-8')

    @staticmethod
    def export_public_key_as_spki(public_key) -> str:
        spki_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return b64encode(spki_bytes).decode('utf-8')

    @staticmethod
    def generate_signing_key_pair_unextractable() -> tuple:
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def sign(private_key, data) -> str:
        signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
        return b64encode(signature).decode('utf-8')

    @staticmethod
    def get_auth_intent(session: requests.Session) -> dict:
        try:
            key_pair = AuthIntent.generate_signing_key_pair_unextractable()
            private_key, public_key = key_pair

            client_public_key = AuthIntent.export_public_key_as_spki(public_key)
            client_epoch_timestamp = str(int(time()))

            response = session.get("https://apis.roblox.com/hba-service/v1/getServerNonce")

            server_nonce = response.text.strip('"')
            payload = f"{client_public_key}|{client_epoch_timestamp}|{server_nonce}"
            sai_signature = AuthIntent.sign(private_key, AuthIntent.string_to_bytes(payload))

            result = {
                "clientEpochTimestamp": client_epoch_timestamp,
                "clientPublicKey": client_public_key,
                "saiSignature": sai_signature,
                "serverNonce": server_nonce
            }

            return result
        except:
            return None
