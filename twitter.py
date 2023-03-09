from flask import Flask, render_template, request, session, url_for, redirect, send_file
from kimin.core_server import Kimin_Core

import subprocess, time

server = Flask(__name__)
server.jinja_env.auto_reload = True
server.config['TEMPLATES_AUTO_RELOAD'] = True

@server.route("/Api", methods=['GET'])
def Api_Tabel():
	sin = Kimin_Core()
	data = sin.GetData()
	data = {"data":data}
	return data

@server.route("/Download")
def Download():
	path = "Twitter.csv"
	sin = Kimin_Core()
	sin.Download_File()
	return send_file(path, as_attachment=True)
@server.route("/Tabel-Api", methods=['GET'])
def Api():
	sin = Kimin_Core()
	data = sin.GetData()
	return render_template('Api-Tabel.html', total=len(data), data=data)

@server.route("/Data", methods=['GET'])
def Tabel():
	sin = Kimin_Core()
	data = sin.GetData()
	return render_template('tabel.html', judul="Hasil Scraping", total=len(data), data=data)

@server.route("/", methods=['POST','GET'])
def Main():
	if request.method == "GET":
		return render_template("main.html", judul="Twitter Scraping", h1="Twitter Scraping Program")
	
	elif request.method == "POST":
		query = request.form.get('query')
		mulai = request.form.get('mulai')
		sampai = request.form.get('sampai')
		
		subprocess.Popen(["python.exe", "kimin/core_scraping.py", f"--query={query.replace(' ','_')}", f"--awal={mulai}", f"--akhir={sampai}"], creationflags=subprocess.CREATE_NEW_CONSOLE)
		time.sleep(10)
		return redirect(url_for('Tabel'))

if __name__ == "__main__":
	server.run(debug=True, port=80)