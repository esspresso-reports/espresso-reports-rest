from datetime import timedelta, datetime
from operator import or_, and_

from sqlalchemy import exists
from sqlalchemy.orm.attributes import flag_modified

from espresso.api.exceptions import EntityAlreadyExistsException
from espresso.api.report.model import Report
from espresso.extensions import db
from espresso.api.user.model import User


def create_user(user_dict: dict):
    user = get_user_by_email(user_dict['email'])

    if user:
        raise EntityAlreadyExistsException()

    user_model = User(id=user_dict['id'], email=user_dict['email'], email_verified=user_dict['email_verified'])

    db.session.add(user_model)
    db.session.commit()


def get_all_users(report_overdue=False):
    q = User.query

    if report_overdue:
        q = User.query.filter(~exists().where(or_(and_(Report.user_id == User.id,
                                                       Report.check_in + timedelta(days=1) > datetime.now()),
                                                  Report.next_working_day > datetime.now())))
    return q.all()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def update_user(user_dict: dict):
    user = get_user_by_id(user_dict['id'])

    if user:
        user.email = user_dict['email']
        user.is_disabled = user_dict['is_disabled']
        db.session.commit()

    else:
        create_user(user_dict)


def update_user_settings(user_id, settings):
    db.session.begin()
    user = get_user_by_id(user_id)
    user.settings.update(settings)
    db.session.commit()


def delete_user(user_id):
    db.session.begin()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
