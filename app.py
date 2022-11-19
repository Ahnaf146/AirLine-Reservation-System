from flask import Flask, render_template




app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('HomePage.html')

if __name__ == "__main__": 
    app.run('127.0.0.1', 5000, debug= True )

