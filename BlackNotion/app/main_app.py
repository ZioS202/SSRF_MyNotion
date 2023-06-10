from flask import Flask, render_template, url_for, request
import urllib.request
from urllib.parse import urlparse


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
	logo_path = url_for ('static', filename= 'images/logo.png')
	bg_path = url_for ('static', filename= 'images/bg.webp')
	return render_template('index.html', title='Home',logo_path=logo_path,bg_path=bg_path)
@app.route('/', methods=['POST'])
@app.route('/home', methods=['POST'])
def go_to():
	url = request.form.get('text')
	parsed_url = urlparse(url)
	# scheme://netloc/path;parameters?query#fragment
	netloc = parsed_url.netloc
	if('localhost:80' in netloc  and parsed_url.path in ['/note1', '/note2', '/note3', '/note4']):
		return urllib.request.urlopen(url).read()
	elif(netloc.split('.')[0] == '127' and len(netloc.split('.')) == 4) or 'localhost' in netloc :
		logo_path = url_for ('static', filename= 'images/logo.png')
		bg_path = url_for ('static', filename= 'images/bg.webp')
		infor_mess = "Bạn không thể truy cập vào localhost !!!"
		return render_template('infor.html', title='Information', infor_mess=infor_mess,logo_path=logo_path,bg_path=bg_path)
	elif netloc.split('.')[0] == '127':
		logo_path = url_for ('static', filename= 'images/logo.png')
		bg_path = url_for ('static', filename= 'images/bg.webp')
		infor_mess = "Bạn không thể truy cập vào localhost !!!"
		return render_template('infor.html', title='Information', infor_mess=infor_mess,logo_path=logo_path,bg_path=bg_path)
	elif 'admin' in parsed_url.path:
		logo_path = url_for ('static', filename= 'images/logo.png')
		bg_path = url_for ('static', filename= 'images/bg.webp')
		infor_mess = "Bạn không thể truy cập vào admin note !!!"
		return render_template('infor.html', title='Information', infor_mess=infor_mess,logo_path=logo_path,bg_path=bg_path)
	else:
		return urllib.request.urlopen(url).read()
@app.route('/about')
def about():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('about.html',title='About',logo_path=logo_path,bg_path=bg_path)
@app.route('/contact')
def contact():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('contact.html',title='Contact',logo_path=logo_path,bg_path=bg_path)

@app.route('/note1')
def getNote1():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('note1.html', title='Note 1',logo_path=logo_path,bg_path=bg_path)
@app.route('/note2')
def getNote2():
	m1 = url_for('static', filename='images/meme/meme1.jpg')
	m2 = url_for('static', filename='images/meme/meme2.jpg')
	m3 = url_for('static', filename='images/meme/meme3.jpg')
	m4 = url_for('static', filename='images/meme/meme4.jpg')
	m5 = url_for('static', filename='images/meme/meme5.jpg')
	m6 = url_for('static', filename='images/meme/meme6.jpg')
	m7 = url_for('static', filename='images/meme/meme7.jpg')
	m8 = url_for('static', filename='images/meme/meme8.jpg')
	m9 = url_for('static', filename='images/meme/meme9.jpg')
	m10 = url_for('static', filename='images/meme/meme10.jpg')
	m11 = url_for('static', filename='images/meme/meme11.jpg')
	m12= url_for('static', filename='images/meme/meme12.jpg')
 
	logo_path = url_for ('static', filename= 'images/logo.png')
	bg_path = url_for ('static', filename= 'images/bg.webp')
	return render_template('note2.html', title='Note 2',logo_path=logo_path,bg_path=bg_path,m1=m1,m2=m2,m3=m3,m4=m4,m5=m5,m6=m6,m7=m7,m8=m8,m9=m9,m10=m10,m11=m11,m12=m12)
@app.route('/note3')
def getNote3():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('note3.html', title='Note 3',logo_path=logo_path,bg_path=bg_path)
@app.route('/note4')
def getNote4():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('note4.html', title='Note 4',logo_path=logo_path,bg_path=bg_path)
if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 80)
 
# http://2130706433:2002/%25%36%31dmin