from authlib.integrations.flask_oauth2 import current_token
from flask import request
from flask_restx import Resource, abort
from espresso.api.report import report_api, report_dto
from espresso.api.report.service import create_report, update_report, get_report_by_id, delete_report, \
    get_latest_report_by_user, get_reports_by_user_id
from espresso.api.auth import require_oauth


@report_api.route('/')
class ReportListResource(Resource):

    @require_oauth('profile reports')
    @report_api.marshal_with(report_dto)
    def get(self):
        return get_reports_by_user_id(current_token['sub'])

    @require_oauth('profile reports')
    @report_api.expect(report_dto, validate=True)
    @report_api.marshal_with(report_dto)
    def post(self):
        new_report = request.json

        if new_report['user_id'] != current_token['sub']:
            report_api.abort(401, "User is not authorized to execute this operation")

        create_report(new_report)

    @require_oauth('profile reports')
    @report_api.expect(report_dto, validate=True)
    def put(self):
        modified_report = request.json

        if modified_report['user_id'] != current_token['sub']:
            report_api.abort(401, "User is not authorized to execute this operation")

        update_report(modified_report)


@report_api.route('/<report_id>')
@report_api.param('report_id', 'identifier of report')
class ReportResource(Resource):

    @require_oauth('profile reports')
    @report_api.marshal_with(report_dto)
    def get(self, report_id):
        report = get_report_by_id(report_id)
        if report['user_id'] != current_token['sub']:
            report_api.abort(401, "User is not authorized to execute this operation")
        return report

    @require_oauth('profile reports')
    def delete(self, report_id):
        report = get_report_by_id(report_id)
        if report['user_id'] != current_token['sub']:
            report_api.abort(401, "User is not authorized to execute this operation")

        delete_report(report_id)


@report_api.route('/latest')
class LatestReportResource(Resource):

    @require_oauth('profile reports')
    @report_api.marshal_with(report_dto)
    def get(self):
        user_id = current_token['sub']
        latest_report = get_latest_report_by_user(user_id)
        if latest_report:
            return latest_report, 200
        else:
            abort(404, 'Report not found.')
