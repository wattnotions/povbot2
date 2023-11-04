from flask import Flask, render_template, request, Response
import threading
import io
import picamera
import logging
from flask_cors import CORS
from threading import Condition
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/key', methods=['GET'])
def get_key():
    key = request.args.get('key')
    if key:
        print(f'Key Pressed: {key}')
    return '', 200

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        finally:
            camera.stop_recording()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
