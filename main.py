from database.engine import Session
from database.entities import Account, Profile

session = Session()
profiles = session.query(Profile).all()

for profile in profiles:
    for account in profile.accounts:
        print(f"account: {account.user} -> profile{account.profile}")
