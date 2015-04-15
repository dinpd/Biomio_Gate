import os
import random
import shutil
import string
import tempfile
import gnupg


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
