import psutil
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/system_info')
def system_info():
    return jsonify({
        'cpu': {
            'usage': psutil.cpu_percent(interval=1),
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True)
        },
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'used': psutil.virtual_memory().used,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        },
        'network': {
            'sent': psutil.net_io_counters().bytes_sent,
            'recv': psutil.net_io_counters().bytes_recv
        }
    })

if __name__ == '__main__':
    app.run(port=5000)