from datetime import datetime

from sqlalchemy import func, desc

from espresso.api.helper import string_to_date
from espresso.extensions import db
from espresso.api.exceptions import EntityAlreadyExistsException
from espresso.api.report.model import Report


def create_report(report_dict: dict):
    user_id = report_dict['user_id']
    check_in = datetime.now()
    report = get_report_by_user_and_day(user_id, check_in.date())

    if not report:
        new_report = Report(check_in=check_in, user_id=user_id,
                            next_working_day=string_to_date(report_dict['next_working_day']),
                            accomplished_tasks=report_dict['accomplished_tasks'],
                            planned_tasks=report_dict['planned_tasks'],
                            general_notes=report_dict['general_notes'])

        db.session.add(new_report)
        db.session.commit()
    else:
        raise EntityAlreadyExistsException()


def get_reports_by_user_id(user_id):
    return Report.query.filter_by(user_id=user_id).order_by(desc(Report.check_in)).all()


def get_report_by_id(report_id):
    return Report.query.filter_by(id=report_id).first()


def get_report_by_user_and_day(user_id, check_in_date):
    return Report.query.filter(Report.user_id == user_id, func.date(Report.check_in) == check_in_date).first()


def get_latest_report_by_user(user_id):
    return Report.query.filter(Report.user_id == user_id).order_by(desc(Report.check_in)).first()


def update_report(report_dict: dict):
    report = get_report_by_id(report_dict['id'])

    if report:
        report.next_working_day = string_to_date(report_dict['next_working_day'])
        report.accomplished_tasks = report_dict['accomplished_tasks']
        report.planned_tasks = report_dict['planned_tasks']
        report.general_notes = report_dict['general_notes']
        db.session.commit()
    else:
        create_report(report_dict)


def delete_report(report_id):
    Report.query.filter_by(id=report_id).delete()
    db.session.commit()
