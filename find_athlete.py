
# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class User(Base):
    """
    Описывает структуру таблицы user для хранения данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # рост пользователя
    height = sa.Column(sa.Integer)

class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения данных атлетов
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост атлета
    height = sa.Column(sa.REAL)
    # имя атлета
    name = sa.Column(sa.Text)
    # вес атлета
    weight = sa.Column(sa.Integer)
    # количество золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # количество серебряных медалей
    silver_medals = sa.Column(sa.Integer)
    # количество бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # всего медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def find_user(id, session):
    """
    Производит поиск пользователя в таблице user по заданному индексу
    """
    # находим все записи в таблице user, у которых поле user.id совпадает с параметром id
    query = session.query(User).filter(User.id == id)
    # составляем список данных роста и даты рождения пользователя
    user_heights_dates = [(user.height, user.birthdate) for user in query.all()]

    # находим рост пользователя по его id
    for user_height, user_birthdate in user_heights_dates:
        return (user_height, user_birthdate)


def find_athelete(user_value, session):
    """
    Производит поиск атлетов в таблице athelete по заданным условиям
    """
    # находим атлета, у которого поле height наиболее близко к user_height
    atl_height = session.query(Athelete).filter(Athelete.height > 0).order_by(sa.func.abs(Athelete.height - user_value[0]))
    result_atl_height = [(athelete.id, athelete.name, athelete.height, athelete.birthdate) for athelete in atl_height]
    # находим атлета, у которого поле birthdate наиболее близко к user_birthdate
    atl_birthdate = session.query(Athelete).filter(Athelete.birthdate > 0).order_by(
        sa.func.abs(sa.func.julianday(Athelete.birthdate) - sa.func.julianday(user_value[1])))
    result_atl_birthdate = [(athelete.id, athelete.name, athelete.height, athelete.birthdate) for athelete in
                            atl_birthdate]
    return (result_atl_height[0], result_atl_birthdate[0])

if __name__ == "__main__":
    session = connect_db()
    # запускаем режим поиска
    id = input("Введи индекс пользователя для поиска: ")
    # Ищем пользователя по индексу
    user_value = find_user(id, session)
    # Если пользователя нашли
    if user_value:
        # Выведем данные о пользователе
        print("Рост и дата рождения пользователя с индексом '%s': " % id, user_value)
        # Ищем ближайшего атлета
        atl_value = find_athelete(user_value, session)
        print(
            "Данные атлета, близкие к пользователю по росту: (№ п/п: {}, имя: {}, рост: {}, дата рождения: {})".format(
                atl_value[0][0], atl_value[0][1], atl_value[0][2], atl_value[0][3]))
        print(
            "Данные атлета, близкие к пользователю по дате рождения: (№ п/п: {}, имя: {}, рост: {}, дата рождения: {})".format(
                atl_value[1][0], atl_value[1][1], atl_value[1][2], atl_value[1][3]))
    else:
        print("Пользователя с таким индексом нет в списке.")

