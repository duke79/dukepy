from .person import Person
from data.common.base import db_session


def create_people():
	bruno = Person("Bruno Krebs")
	john = Person("John Doe")

	session = db_session()
	session.add(bruno)
	session.add(john)
	session.commit()
	session.close()


def get_people():
	session = db_session()
	people_query = session.query(Person)
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
