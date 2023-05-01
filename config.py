db_info = {'host': 'dpg-ch7ojto2qv26p1e78deg-a.oregon-postgres.render.com',
           'database': 'task_system',
           'psw': 'eSeyarA0mgw9TakUboTdZDj3TcSfT2il',
           'user': 'admin',
           'port': ''}


class Config:
	SECRET_KEY = 'lNKHKcggvsuIOlUprbzqOvXPXXhsgliAekKJcMLxhwXsLbTefbMsiPGOitwnWBoVwkcflcfZTGYFLMCtjqsIBDFkfJuzaOtwKOeNZQmoiLWWbhUUJMMkgyRXoYdTfOcEiXlGKbxEDRQZmtJPExOrOQFHOpqtBnBeIZIAzzdabSVPtEpoIYjwpkBLDMrbiclunqrfnVCnUieCxoQSUkVTbnJuHIbigRmyPXGCQKBiXgLWJTZhlUlJLSFhffxkpJqj'
	SQLALCHEMY_DATABASE_URI = f"postgresql://{db_info['user']}:{db_info['psw']}@{db_info['host']}/{db_info['database']}"
