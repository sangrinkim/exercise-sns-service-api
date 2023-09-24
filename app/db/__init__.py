from app.db.fake_repository import FakeRepository


def create_database():
    instance = FakeRepository()

    return instance


# DB 인스턴스 생성
db_instance = create_database()