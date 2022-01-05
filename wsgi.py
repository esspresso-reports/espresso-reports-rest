from espresso import create_app
from espresso.extensions import db

app = create_app("dev")

if __name__ == "__main__":
    app.run()

reports = [
    {
        'accomplished_tasks': [
            ''],
        'planned_tasks': ['continue writing project proposal'],
        'general_notes': ['still no reply from michael, maybe i have to call him tomorrow!'],
        'checkin': '9:31',
        'next_working_day': '15.12.2021'
    },
    {
        'accomplished_tasks': [
            'read paper “A differentiated picture of student performance in introductory courses to theory of computation” ',
            'give feedback on student assignments'],
        'planned_tasks': ['give feedback on student assignments'],
        'general_notes': ['Did not finish review of student assignments yet (3 more to go)'],
        'checkin': '10:11',
        'next_working_day': '11.12.2021'
    },
    {
        'accomplished_tasks': ['replied to mails from barbara and michael'],
        'planned_tasks': [
            'read paper “A differentiated picture of student performance in introductory courses to theory of computation” ',
            'give feedback on student assignments'],
        'general_notes': ['no notes added to this report!'],
        'checkin': '8:53',
        'next_working_day': '10.12.2021'
    }
]


@app.cli.command()
def init_db():
    db.create_all()


@app.cli.command()
def drop_db():
    db.drop_all()
