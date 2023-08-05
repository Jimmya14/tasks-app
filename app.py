from flask import Flask, jsonify, request
from sqlalchemy import Boolean, CheckConstraint, asc, create_engine, Column, Integer, String, Date, desc, or_
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database, database_exists
from config import Config
config = Config()

DATABASE_URI = f"postgresql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

if not database_exists(engine.url):
    create_database(engine.url)

class Task(Base):
    __tablename__ = 'tasks'
    query: Query = db_session.query_property()
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, index=True)
    description = Column(String(120), index=True)
    isCompleted = Column(Boolean, index=True)
    dueDate = Column(Date, index=True)
    priority = Column(Integer, nullable=False, default=3, index=True)
    
    # Add a check constraint to ensure priority is between 1 and 5
    __table_args__ = (
        CheckConstraint('priority >= 1 AND priority <= 5'),
    )

    def __init__(self, title=None, description=None, isCompleted=False, dueDate=None, priority=None):
        self.title = title
        self.description = description
        self.isCompleted = isCompleted
        self.dueDate = dueDate
        self.priority = priority

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'isCompleted': self.isCompleted,
            'dueDate': self.dueDate,
            'priority': self.priority
        }

Base.metadata.create_all(bind=engine)
app = Flask(__name__)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    newTask = Task(
        title=data['title'],
        description=data['description'],
        isCompleted=data['isCompleted'],
        dueDate=data['dueDate'],
        priority=data['priority']
    )
    db_session.add(newTask)
    db_session.commit()
    return jsonify(newTask.to_dict()), 201

@app.route('/task', methods=['GET'])
def get_tasks():
    pageIndex = request.args.get('pageIndex', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', '', type=str)
    isCompleted = request.args.get('isCompleted', None, type=bool)
    sortField = request.args.get('sortField', '', type=str)
    sortOrder = request.args.get('sortOrder', '', type=str)
    
    # Calculate offset
    offset = (pageIndex - 1) * limit
    
    if search:
        search = "%" + search + "%" # if you want to search anywhere in the string
        query = Task.query.filter(
            or_(
                Task.title.ilike(search),
                Task.description.ilike(search)
            )
        )
    else:
        query = Task.query
        
    if isCompleted is not None:
        query = query.filter(Task.isCompleted == isCompleted)
        
    if sortField:
        order_func = desc if sortOrder == 'desc' else asc
        print(sortOrder)
        query = query.order_by(order_func(getattr(Task, sortField)))
    else:
        query = query.order_by(desc(Task.dueDate))
    
    tasks = query.offset(offset).limit(limit).all()
    total = query.count()
    return jsonify({
        'data': [task.to_dict() for task in tasks],
        'pageCount': (total // limit) + (1 if total % limit > 0 else 0),
        'totalCount': total
    })

@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return 'Not Found', 404
    return jsonify(task.to_dict())

@app.route('/task/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return 'Not Found', 404
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.isCompleted = data['isCompleted']
    task.dueDate = data['dueDate']
    task.priority = data['priority']
    Task.query.commit()
    return jsonify(task.to_dict())

@app.route('/task/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task is None:
        return 'Not Found', 404
    Task.query.delete(task)
    Task.query.commit()
    return '', 200


if __name__ == '__main__':
    app.run()