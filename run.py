from app import create_app, db
from app.models import Owner

app = create_app()


@app.cli.command("create-owner")
def create_owner():
    """Create an owner account: flask --app run.py create-owner"""
    import getpass

    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    with app.app_context():
        if Owner.query.filter_by(username=username).first():
            print("That username already exists.")
            return
        owner = Owner(username=username)
        owner.set_password(password)
        db.session.add(owner)
        db.session.commit()
        print(f"Owner '{username}' created.")


if __name__ == "__main__":
    app.run(debug=True)
