from flask import Flask, render_template, Response,request,redirect,url_for
from prediction import VideoCamera
import os,glob

app = Flask(__name__)

@app.route('/')
def new():
    return render_template('new.html',result='')

@app.route('/vi.html')
def vi():
    return render_template('vi.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/new.html', methods = ['GET', 'POST'])
def upload_file():
   dir= 'static/video/'
   for v in os.scandir(dir):
    os.remove(v.path)
   if request.method == 'POST':
      f = request.files['file']
      a=f.filename
      if(a==""):
        return render_template('new.html', result="No file uploaded.!")
      else:

        x=a.split('.')[1]
        y='video.'+x
        f.save('static/video/video.'+x)
        return render_template('new.html', result='%s file uploaded successfully'%a)
        
@app.route('/vf.html')
def vf():
    return render_template('vf.html')

@app.route('/video_f')
def video_f():
    path='static/video/'
    w=os.listdir("static/video/")[0]
    return Response(gen(VideoCamera(path+w)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)