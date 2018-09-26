import os, time
import logging, logging.handlers
from flask import Flask,render_template,request
from sample_script import run_notepad

app = Flask(__name__)

handler = logging.FileHandler(os.path.join(os.getcwd(),"event.log"))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("App started")

@app.route("/", methods=['POST', 'GET'])
def show_main():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        time.sleep(3)
        log_lines = []
        with open(os.path.join(os.getcwd(),"event.log"),'r') as f:
            for line in f:
                log_lines.append(line)
        f.close()
        data = [log_lines, len(log_lines),str.split(request.form['orders'])]
        # Get checkBox states
        if request.form.get('chb1'):
            if request.form.get('chb2'):
                chb_state = [True,True]
            else:
                 chb_state = [True,False]
        elif request.form.get('chb2'):
            if request.form.get('chb1'):
                chb_state = [True,True]
            else:
                 chb_state = [False, True]

        return render_template("index.html",log=data,chb=chb_state)

@app.route("/log")
def hello():
    log_lines = []
    logger.info("App refreshed. With auto-restart ON")
    with open(os.path.join(os.getcwd(),"event.log"),'r') as f:
        for line in f:
            log_lines.append(line)
    f.close()
    return render_template("log.html",log=log_lines)

@app.route("/dash")
def show_dash():
    return render_template("dash_main.html")

@app.route("/powners")
def ap_cjowners():
    return render_template("ap_chowner.html")

if __name__ == '__main__':
   app.run(debug=True)