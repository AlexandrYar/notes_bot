from sqlalchemy import create_engine, MetaData, ForeignKey, Column, Integer, String, select
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

engine = create_engine('postgresql://postgres:psql10Unibos.@localhost:5432/task_db')

metadata = MetaData()
Base=declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__='users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    role = Column(String(100))
    tg_id = Column(String(100))

    user = relationship('Task', back_populates='task')

    def __repr__(self):
        return "{}, {}, {}, {}".format(self.user_id, self.name, self.role, self.tg_id)
    
    @classmethod
    def create_user(self, user_name, user_role, user_tg_id):
        print(self)
        user = User(name=user_name, role=user_role, tg_id=user_tg_id)
        session.add(user)
        session.commit()

    def get_all_users_task(self, tg_id):
        print(tg_id)
        stmt = select(Task).join(Task.task).where(User.tg_id == str(tg_id))
        print(stmt)
        task_id = 0
        task_dict = {}
        for task in session.execute(stmt).all():
            task_id +=1
            print(task)
            dict ={
                'task_id' : task.Task.task_id,
                'date_of_creation' : task.Task.date_of_creation,
                'execution_date' : task.Task.execution_date,
                'description' : task.Task.description,
                'executor_id' : self.user_id
            }
            task_dict[task_id] = dict
        return task_dict

    @classmethod
    def get_all_users(self):
        result = {}
        index = 0
        for u in session.query(User).all():
            index += 1
            dict = u.__dict__
            dict.pop('_sa_instance_state', None)
            result[index] = dict
        return result
    
    def user_is_register(self, tg_id):
        stmt = select(User.user_id).where(User.tg_id == str(tg_id))
        print(stmt)
        user_tg_id = session.execute(stmt).all()
        print(self.name, self.role, self.tg_id)
        if user_tg_id == []:
            name=self.name
            role=self.role
            self.create_user(str(name), str(role), str(tg_id))

    def get_id_by_tg_id(self, tg_id):
        stmt = select(User.user_id).where(User.tg_id == str(tg_id))
        user_tg_id = session.execute(stmt).all()[0][0]
        return int(user_tg_id)


class Task(Base):
    __tablename__='tasks'

    task_id = Column(Integer, primary_key=True)
    date_of_creation = Column(String(100), nullable=False)
    execution_date = Column(String(100))
    description = Column(String(250), nullable=False)
    executor_id = Column(Integer, ForeignKey('users.user_id'))

    task = relationship('User', back_populates='user')

    def __repr__(self):
        return '{}, {}, {}, {}, {}'.format(self.task_id, self.executor_id, self.date_of_creation, self.execution_date, self.description)
    
    def create_task(self):
        date_of_creation = self.date_of_creation
        execution_date = self.execution_date
        description = self.description
        task = Task(date_of_creation = date_of_creation, execution_date =execution_date, description = description, executor_id=self.executor_id)
        session.add(task)
        session.commit()

    
def create_all_db():
    Base.metadata.create_all(engine)