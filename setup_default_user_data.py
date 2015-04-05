from biomio.protocol.data_stores.base_data_store import BaseDataStore

__author__ = 'alexchmykhalo'

import os
import random
import shutil
import string
import tempfile
import gnupg

probe_app_id = '88b960b1c9805fb586810f270def7378'
probe_app_type = 'probe'
probe_key = '-----BEGIN RSA PRIVATE KEY-----\n'
'MIICXAIBAAKBgQCwjyQTMxfiP8a5j3i8RE8bC6hYBmCRP5wDfHofQhGI/NMXXdAi\n'
'uNzrV7ob7KBkLZdLiayvOxDFsgUbXEZ3pvsh7JfDIrXsAOqflHJdLz+SR9QfZcYW\n'
'5pL4704wXsXR9TwT4t3hC8m1dRaoIA4/J6aKx+VRxVc3LXHrVziB0gUfiQIDAQAB\n'
'AoGARaFOAtxlkO7B+rBgVy9BW1Mvovdw4heJ+b3/k5BExhefUFnJGch6J75DQXwC\n'
'jT+FqV60Ya8ToEPiy7WKfOm3pDHon72byrvrh0DYorV76Ud2mlnhBmE1Gt1+52t1\n'
'JYoPZ6mZEGnicXhdGgtB+M0zIVDF1eqaXTqF1JZtR8P2H9kCQQC30US9/9+iXVJk\n'
'SLdZXitGC7VLwqcoOFC79QpQKul8cXaV1CaYyX+XKZBP8i04Jeh7uJIJA48g+s/U\n'
'M7miYSYTAkEA9eQ2L1k8m9IRqA0+w8SwzdfZFxuK0jBNpQ7QVk92jfBVsu59bRbM\n'
'v7sHry+U/Arrg9QYD//7cEF4xeW38x+HcwJBALAbakSuFE+2IO27TQ3tzn+5T+RZ\n'
'hVRfP9oTleHgevmiqv441xGiWv8z7vLpDrGwf9+ooSDJrCLoqJyhQcR0VskCQEW3\n'
'B1nTTijLnW/tGW9907b4zLcNewVu5oS2t4DRFMbXbiTGE0+bmD9/8oTL08zF99Iv\n'
'jwbyR8Ki/W/2WnoW5VsCQEFTUHs64gg6Av2F4TlKtSb2MsN4rWW7qSjfNHp3r5tM\n'
'tYPt+HbggPJbSwJ3KwGmKp2+1w6GdgR953ruFHUcs0c=\n'
'-----END RSA PRIVATE KEY-----'

probe_pub_key = '-----BEGIN PUBLIC KEY-----\n'
'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwjyQTMxfiP8a5j3i8RE8bC6hY\n'
'BmCRP5wDfHofQhGI/NMXXdAiuNzrV7ob7KBkLZdLiayvOxDFsgUbXEZ3pvsh7JfD\n'
'IrXsAOqflHJdLz+SR9QfZcYW5pL4704wXsXR9TwT4t3hC8m1dRaoIA4/J6aKx+VR\n'
'xVc3LXHrVziB0gUfiQIDAQAB\n'
'-----END PUBLIC KEY-----'

extension_app_id = '3a9d3f79ecc2c42b9114b4300a248777'
extension_app_type = 'extension'
extension_key = '-----BEGIN RSA PRIVATE KEY-----\n'
'MIICXQIBAAKBgQCrD2qbaFzrq5QNwpucqS3+zECbM5tBnG40GkYPPZvgykHeYmtd\n'
'gkzZH3gJISd8eNfGR4yRMVoP5apuDKeJSnH4lwTFz3IJNFglD95VpleIk8ldRWx0\n'
'8K2EpBi+WodZ5B9CBVpmeSGvrCeaxAICmrh9WcLL4HDeKR4r6M6mGB+SrwIDAQAB\n'
'AoGBAKrQmzEStu8zB4XyFfgLTH3KMp2Im/mZnsZykhE4AUcoUTwjZXkb22dZMEFV\n'
'lRuLhFRgMDLwaDHFsjlwc3/6EfF70eqRelVv1IyCbEwBZceiCFdL/ZRujP00xq35\n'
'm0wiL655U52ZJDrwDIxW/ItwnTwCRcr+tNCA5vEfcQT7O53RAkEAz5qsggneeyMX\n'
'gkWdlusAhuLvzsJeSPLLH4c0uHEB1lT4mPa4y3xrbLu1oV4X15w//REerYah8dbt\n'
'VA1+csvp6QJBANLv4oQcIzBOVWW5bYOl9+K3IPOJk2vsk98gjNX26uWm4+eAUCfp\n'
'2xXwVtxrhdlKn5bfAmZeHhqfY5PPq375INcCQBf2xcT4+KqEIXmTKZ67H8NyPLZE\n'
'L3gCNro79DT6LnkcM9oMWMZ8ZTYW8N9gqiXkTmqa6EylhtoQsjKKoDcGHMkCQDLU\n'
'zgBKC4zLg7bEzYhJCYhf2xf1EkqSszu0y1uQaiC3a/pQqIBF0Z7i0PvDCXlIi1a/\n'
'HQPwME74E/X9uHUbsfcCQQCwkp2dGkN6+qOWZL9h5YbrfX5VctcQ8hTIwP/Yymzt\n'
'tZ5VZ2XehrLoTY6DAi2lH4ToZDMkzwDBGsHzs057tH4O\n'
'-----END RSA PRIVATE KEY-----'

extension_pub_key = '-----BEGIN PUBLIC KEY-----\n'
'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCrD2qbaFzrq5QNwpucqS3+zECb\n'
'M5tBnG40GkYPPZvgykHeYmtdgkzZH3gJISd8eNfGR4yRMVoP5apuDKeJSnH4lwTF\n'
'z3IJNFglD95VpleIk8ldRWx08K2EpBi+WodZ5B9CBVpmeSGvrCeaxAICmrh9WcLL\n'
'4HDeKR4r6M6mGB+SrwIDAQAB\n'
'-----END PUBLIC KEY-----'

mails = ['alex.chmykhalo@vakoms.com.ua', 'alex.chmykhalo@vakoms.com.ua',
         'andriy.lobashchuk@vakoms.com', 'andriy.lobashchuk@vakoms.com.ua',
         'boris.itkis@gmail.com', 'ditkis@gmail.com']

def generate_pgp_key_pair(email):
    pass_phrase = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(16))
    home = tempfile.mkdtemp()
    fd, keyring = tempfile.mkstemp(dir=home)
    ascii_armored_public_key = None
    ascii_armored_private_key = None
    os.close(fd)
    if os.environ.get('USERNAME', None) is None:
        os.environ['USERNAME'] = email.split('@')[0]
    try:
        gpg = gnupg.GPG(gnupghome=home, keyring=keyring, options=['--no-default-keyring', '--no-version',
                                                                  '--no-use-agent'])
        input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_comment="", name_real="BioMio",
                                       name_email=email, passphrase=pass_phrase)
        key = gpg.gen_key(input_data)
        ascii_armored_public_key = gpg.export_keys(key.fingerprint)
        ascii_armored_private_key = gpg.export_keys(key.fingerprint, True)
    except Exception, e:
        print e
    finally:
        shutil.rmtree(home)
    return ascii_armored_public_key, ascii_armored_private_key, pass_phrase


def register_for_handshake(user_id, mails, extension_app_id, extension_pub_key, probe_app_id, probe_pub_key):
    from biomio.protocol.data_stores.user_data_store import UserDataStore
    from biomio.protocol.data_stores.application_data_store import ApplicationDataStore
    from biomio.protocol.data_stores.email_data_store import EmailDataStore

    BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key(extension_app_id))
    BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key(probe_app_id))
    for mail in mails:
        BaseDataStore.instance().delete_custom_lru_redis_data(EmailDataStore.get_data_key(mail))

    UserDataStore.instance().store_data(user_id)
    store_keywords = {ApplicationDataStore.APP_TYPE_ATTR: 'extension',
                      ApplicationDataStore.PUBLIC_KEY_ATTR: str(extension_pub_key),
                      ApplicationDataStore.USER_ATTR: 1}

    ApplicationDataStore.instance().store_data(extension_app_id, **store_keywords)
    BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key(extension_app_id))

    # UserDataStore.instance().store_data(1)
    store_keywords = {ApplicationDataStore.APP_TYPE_ATTR: 'probe',
                      ApplicationDataStore.PUBLIC_KEY_ATTR: str(probe_pub_key),
                      ApplicationDataStore.USER_ATTR: user_id}

    ApplicationDataStore.instance().store_data(probe_app_id, **store_keywords)
    BaseDataStore.instance().delete_custom_lru_redis_data(ApplicationDataStore.get_data_key(probe_app_id))

    for mail in mails:
        public, private, pass_phrase = generate_pgp_key_pair(mail)
        store_keywords = {
            EmailDataStore.PASS_PHRASE_ATTR: pass_phrase,
            EmailDataStore.PUBLIC_PGP_KEY_ATTR: public,
            EmailDataStore.PRIVATE_PGP_KEY_ATTR: private,
            EmailDataStore.USER_ATTR: user_id
        }
        EmailDataStore.instance().store_data(mail, **store_keywords)
        BaseDataStore.instance().delete_custom_lru_redis_data(EmailDataStore.get_data_key(mail))


def main():
    register_for_handshake(user_id=1, mails=mails, extension_app_id=extension_app_id, extension_pub_key=extension_pub_key,
                           probe_app_id=probe_app_id, probe_pub_key=probe_pub_key)

if __name__=='__main__':
    main()