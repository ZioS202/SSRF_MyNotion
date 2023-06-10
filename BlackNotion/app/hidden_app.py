from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    infor_mess = "Admin backend"
    return render_template('infor.html',title='Information',infor_mess=infor_mess,logo_path=logo_path,bg_path=bg_path)
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
@app.route('/admin')
def get_flag():
    logo_path = url_for ('static', filename= 'images/logo.png')
    bg_path = url_for ('static', filename= 'images/bg.webp')
    return render_template('admin.html',title='Admin note',logo_path=logo_path,bg_path=bg_path)

if __name__ == '__main__':
	app.run(host = "0.0.0.0", port = 2002)