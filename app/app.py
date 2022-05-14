import simplejson as json

from flask import Flask, request, Response
import mysql.connector
from redis import Redis
from rq import Queue
from rq.job import Job

from sender import send_mail

# initialize redis server
r = Redis(host='redis', port=6379)
queue = Queue(connection=r)

app = Flask(__name__)

def getConn():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'tasksdb'
    }
    connection = mysql.connector.connect(**config)
    return connection

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if request.headers['Content-Type'] == 'application/json':

            taskrabbit = request.get_json()
            id = taskrabbit.get("id")
            taskName = taskrabbit.get("taskName")
            taskStatus = taskrabbit.get("taskStatus")
            notify = taskrabbit.get("notify")
            
            connection = getConn()
            cursor = connection.cursor(dictionary=True)
            query = "INSERT INTO tasks (id, taskName, taskStatus, notify) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, [id, taskName, taskStatus, notify])
            connection.commit()

            cursor.close()
            connection.close()
            
            return {'task': {
                'taskName': taskName,
                'taskStatus': taskStatus,
                'notify': notify
            }, 'message': 'Task inserted with id: '+id}, 201

        else:
            return {'error': 'Invalid JSON body input'}, 400
    else:
        try:
            
            connection = getConn()
            cursor = connection.cursor(dictionary=True)

            cursor.execute('SELECT * FROM tasks')
            
            taskrabbit = cursor.fetchall()

            cursor.close()
            connection.close()

            js = json.dumps(taskrabbit)
            resp = Response(js, status=200, mimetype='application/json')
            return resp

        except:
            return {'error': 'error in get all'}, 400

# 3) Get a specific task by passing ID through URL
@app.route('/tasks/<string:id>/', methods=['GET'])
def getById(id):
    try:
        connection = getConn()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT taskName, taskStatus from tasks where id = %s"
        cursor.execute(query, [id])
        taskrabbit = cursor.fetchall()
        cursor.close()
        connection.close()
        
        js = json.dumps(taskrabbit)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    except:
        return {'error': 'invalid ID'}, 400

# 4) Delete a specific task by passing id through URL
@app.route('/tasks/<string:id>', methods=['DELETE'])
def deleteTask(id):
    try:
        connection = getConn()
        cursor = connection.cursor(dictionary=True)
        
        query = "DELETE FROM tasks where id = %s"
        cursor.execute(query, [id])
        connection.commit()
        cursor.close()
        connection.close()

        return {'Task deleted:': id}, 200

    except:
        return {'error': 'invalid ID'}, 400

# 5) Edit a task
@app.route('/taskupdating', methods=['PUT'])
def updatebyID():
    if request.headers['Content-Type'] == 'application/json':
        taskrabbit = request.get_json()
        id = taskrabbit.get("id")
        taskName = taskrabbit.get("taskName")
        taskStatus = taskrabbit.get("taskStatus")
        notify = taskrabbit.get("notify")
            
        connection = getConn()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute ("""
            UPDATE tasks
            SET taskName=%s, taskStatus=%s, notify=%s
            WHERE id=%s
            """, (taskName, taskStatus, notify, id))

        connection.commit()
        cursor.close()
        connection.close()
        
        if taskStatus == True:
            # second item in parantheses is the argument passed into the function, sender.send_mail
            # send_mail(id, taskName, notify)
            # return {'message': 'notified'}, 200
            
            job = queue.enqueue(send_mail, id, taskName, notify)
            response = {
                "jobId": job.id,
                "timeOfEnqueue": job.enqueued_at,
                "message": f"{job.id} was changed to status completed and has been added to queue at {job.enqueued_at}"
            }
            return response

        else:
            
            return {'task': {
                'taskName': taskName,
                'taskStatus': taskStatus,
                'notify': notify
            }, 'message': 'Task remains uncompleted but Name or Notify were updated: '+id}, 201

    else:
        return {'error': 'Invalid JSON body input'}, 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
