from .incident_report import IncidentReport
from data.common.base import db_session


def create_people():
	bruno = IncidentReport("Bruno Krebs")
	john = IncidentReport("John Doe")
	bruno.save()
	john.save()


def get_people():
	session = db_session()
	people_query = session.query(IncidentReport)
	session.close()
	return people_query.all()


def main():
	people = get_people()
	if len(people) == 0:
		create_people()
	people = get_people()

	for person in people:
		print('{0} was born'.format(person.name))


if __name__ == "__main__":
	main()
