from app import db, secret_key, encrypt
from utils import *
import datetime 
from datetime import timezone
from models.User import User
from models.Role import Role as RoleModel
from models.User import User as UserModel
from models.UserRoleMapping import UserRoleMapping as UserRoleMappingModel


def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    status = 401
    message = 'Incorrect username or password'
    user = None
    try:
        user = (
            db.session.query(User)
            .filter(User.user_name == user_name)
            .first()
        )
        if user:
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            if entered_password_enc == user.password:
                status = 200
                message = 'User successfully authenticated'
                user = {
                    'user_name': user.user_name, 'first_name': user.first_name,
                    'last_name': user.last_name, 'user_email': user.user_email,
                    'roles': [role.role_name for role in user.roles],
                    'entities': [entity.entity_name for entity in user.entities],
                    "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=1),
                    "iat": datetime.datetime.now(tz=timezone.utc)
                }
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, user


def check_and_add_user_details(user_name: str, user_email: str, password: str, first_name: str, last_name: str) -> (int, str, dict):
    """
    Check and add user details function
    Checks if the user is present in database else adds the details
    :param user_name: user_name entered by user
    :type user_name: str
    :param user_email: User email entered by user
    :type user_email: str
    :param password: password entered by user
    :type password: str
    :param first_name: first_name entered by user
    :type first_name: str
    :param last_name: last_nameUser email entered by user
    :type last_name: str
    """
    try:
        user = (
            db.session.query(User)
            .filter(User.user_name == user_name)
            .first()
        )

        if not user:
            print ("user doesnt exist, creating user")
            status, message, data = add_user(user_name, user_email, password, first_name, last_name)

        else:
            print ("user already exists")
            status = 409
            message = 'User already exists'
            data = {"user_name": user.user_name}


    except Exception as e:
        message = str(e)
        status = 500
    return status, message, data


def add_user(user_name: str, user_email: str, password: str, first_name: str, last_name: str):
        data = {"user_name": None}
        print('Adding User')
        role_names: [str] = ['SUPERADMIN', 'ADMIN', 'USER']
        try:
            user_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            non_admin_user = UserModel(user_name=user_name, user_email=user_email,
                                    password=user_password_enc, first_name=first_name, last_name=last_name)
            db.session.add(non_admin_user)
            db.session.commit()
             
            non_admin_role: RoleModel = RoleModel.get_role_by_name(role_name=role_names[2])
            non_admin_user_role_mapping = UserRoleMappingModel(user_name=non_admin_user.user_name,
                                                            role_id=non_admin_role.role_id)

            db.session.add(non_admin_user_role_mapping)
            db.session.commit()

            status = 201
            message = f"User {non_admin_user.user_name} created in database"
            data = {"user_name": non_admin_user.user_name}

        except Exception as e:
            message = str(e)
            status = 500

        return status, message, data