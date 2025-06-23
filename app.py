from flask import Flask, render_template, request, redirect, flash, send_from_directory
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'secret123'

DOWNLOADS_DIR = 'downloads'
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        download_type = request.form['type']
        if url:
            try:
                if download_type == 'audio':
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }]
                    }
                else:
                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if download_type == 'audio':
                        filename = os.path.splitext(filename)[0] + '.mp3'
                filename_only = os.path.basename(filename)
                flash(f"{'Audio' if download_type == 'audio' else 'Video'} downloaded successfully! "
                      f"<a href='/downloads/{filename_only}' class='alert-link' download>Click here to download</a>", "success")
            except Exception as e:
                flash(f"Error: {str(e)}", "danger")
        else:
            flash("Please enter a valid URL.", "warning")
        return redirect('/')
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
