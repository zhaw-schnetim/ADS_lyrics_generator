import os.path
from threading import Thread

from flask import Flask, jsonify, request
import json
import services.spleeter as sp
import services.file_uploader as fu
import services.wav2vec as wv
import services.initial_setup as init
import services.scraper as sc

app = Flask(__name__)


# ----------------------------------------------------------------------------------------------------------
# Each call needs to be called separately


@app.route('/folders', methods=['GET'])
def folders():
    init.create_folders()
    return jsonify({'status': 'done'})


@app.route('/upload', methods=['GET'])
def upload_file():
    fu.download_and_save_file(request.args)
    return jsonify({'status': 'done'})


@app.route('/extract-voice', methods=['GET'])
def start_generate():
    args = request.args
    sp.extract_voice(args)
    return jsonify({'status': 'done'})


@app.route('/transcribe', methods=['GET'])
def transcribe():
    args = request.args
    wv.transcribe(args.get("name"))
    return jsonify({'status': 'done'})


@app.route('/scrape', methods=['GET'])
def scrape_song_artist():
    args = request.args
    sc.scrape_song_artist(args)
    return jsonify({'status': 'done'})


# ----------------------------------------------------------------------------------------------------------
# Everything will be called by one endpoint -
# example req: /start?url=https://youtu.be/RgKAFK5djSk&name=wiz_khalifa_see_you_again&start_time=11

@app.route('/start', methods=['GET'])
def start():
    p = Thread(target=do_everything, args=(request.args,))
    p.daemon = True
    p.start()

    return jsonify({'status': 'started lyrics generation for ' + request.args.get("name")})


# example req: /result?name=wiz_khalifa_see_you_again

@app.route('/result', methods=['GET'])
def result():
    args = request.args

    is_exist = os.path.exists('results/information/' + args.get("name") + '/result.json')

    if is_exist:
        f = open('results/information/' + args.get("name") + '/result.json')
        data = json.load(f)

        return jsonify(data)
    else:
        return jsonify({"status": "Not found, please trigger via /start",
                        "example": "/start?url=https://youtu.be/RgKAFK5djSk&name=wiz_khalifa_see_you_again&start_time=11"})


def do_everything(args):
    init.create_folders()
    fu.download_and_save_file(args)
    sp.extract_voice(args)
    wv.transcribe(args.get("name"))
    sc.scrape_song_artist(args)
    print("Done")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)
