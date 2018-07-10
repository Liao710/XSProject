import time

from XSProject.celery import app



# 声明一个任务
@app.task
def sendMail(to,msg):
    time.sleep(5)
    print('向',to,'发送:',msg,'邮件成功')

    return 'ok'





