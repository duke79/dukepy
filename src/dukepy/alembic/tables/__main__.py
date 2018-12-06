from my_table import MyTable
from data.common.base import db_session


def create_people():
	bruno = MyTable("Bruno Krebs", "abc")
	john = MyTable("John Doe", "bcd")
	bruno.save()
	john.save()


def get_people():
	session = db_session()
	people_query = session.query(MyTable)
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
