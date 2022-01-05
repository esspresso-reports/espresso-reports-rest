from flask_restx import Namespace, fields

report_api = Namespace('report', description='report related operations')

report_dto = report_api.model('report', {
    'id': fields.Integer(required=False),
    'check_in': fields.DateTime(required=False),
    'next_working_day': fields.Date,
    'accomplished_tasks': fields.String,
    'planned_tasks': fields.String,
    'general_notes': fields.String,
    'user_id': fields.String
})

