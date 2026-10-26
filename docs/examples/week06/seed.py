from getpass import getpass

from pwdlib import PasswordHash

from database import connect_db


def seed_users():
    password = getpass('Choose a dummy password (12+ characters): ')
    if len(password) < 12:
        raise ValueError('Use at least 12 characters for this exercise')
    hasher = PasswordHash.recommended()
    with connect_db() as conn:
        for name, email in [('Ada', 'ada@example.com'),
                            ('Lin', 'lin@example.com'),
                            ('Grace', 'grace@example.com')]:
            conn.execute(
                '''INSERT INTO users (name, email, password_hash)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (email) DO NOTHING''',
                (name, email, hasher.hash(password)),
            )
    print('Dummy users are ready. Existing emails were left unchanged.')


if __name__ == '__main__':
    seed_users()
