from flask import Flask, render_template
import pymsql.cursor



app = Flask(__name__)

conn = pymsql.connect(host = 'localhost',
                       user = 'root', 
                       password= 'root',
                       db='meetup',
                       charset='utf8mb4',
                       cursorclass=pymsql.cursors.DictCursor)
                        )

@app.route('/')
def hello():
    return render_template('HomePage.html')

if __name__ == "__main__": 
    app.run('127.0.0.1', 5000, debug= True )

