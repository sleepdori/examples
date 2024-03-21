from crypto.CryptoUtil import CryptoUtil


crypto_util = CryptoUtil('/work/python/private', 'my_key.key')

database_server_uri = "mongodb://localhost:27017/"
database_name = "aaaa"
database_user = "bbb"
database_passwd = "dddd"
telegram_bot_token = "12345:ddddddddddddddddddddddddddd"

encrypted_message = crypto_util.encrypt(telegram_bot_token)
print(encrypted_message)
decrypted_message = crypto_util.decrypt(encrypted_message)
print(decrypted_message)
