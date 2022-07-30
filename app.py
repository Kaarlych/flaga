from flask import Flask, render_template, redirect, url_for
import flask_wtf
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import random
import os
import wikipedia
import requests
from lxml import html

from moje_programy.character import character


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static'
app.secret_key = ':)'

@app.route('/')
def index():
    text = open('dane/xd.txt').read()
    return render_template("index.html", text=text)

@app.route('/xd')
def xd():
    return render_template("xd.html")

@app.route('/kubus_puchatek')
def kubus_puchatek():
	return render_template('kubus_puchatek.html')

@app.route('/flaga_dla_ukrainy')
def flaga_dla_ukrainy():
    return render_template("flaga_dla_ukrainy.html")

@app.route('/zajecia_programowania')
def zajecia_programowania():
    return render_template("zajecia_programowania.html")

@app.route('/brudnopis')
def brudnopis():
    super_heroes = ['Bruce Lee', 'Kubuś Puchatek', 'Kopernik', 'Małysz']
    chosen_hero = random.choice( super_heroes)
    description = character( chosen_hero).encode('utf-8').decode()
    return render_template("brudnopis.html", description=description)

@app.route('/postacie')
def ciekawe_postacie():
    lista_ciekawych_postaci = [
        'Pudzianowski',         # 0
        'Małysz',               # 1
        'Kopernik',             # 2
        'Maria Skłodowska',     # 3
        'Kościuszko',           # 4
        'Donald',               # 5
        'Myszka Miki',          # 6
    ]
    
    opisy_postaci = []
    for i in range(3):
        postac = random.choice(lista_ciekawych_postaci)
        indeks = lista_ciekawych_postaci.index(postac)
        lista_ciekawych_postaci.pop(indeks)

        opis_postaci = character(postac)
        dlugosc_opisu = len(opis_postaci)
        ilosc_slow = opis_postaci.split()
        ilosc_slow = len(ilosc_slow)
        info = [postac, opis_postaci, dlugosc_opisu, ilosc_slow]
        opisy_postaci.append(info)


    

    return render_template("postacie.html", opisy_postaci=opisy_postaci)



@app.route('/form_a', methods=["GET", "POST"])
def form_a():

    form = X()
    if form.validate_on_submit():
        
        github = form.github.data
        my_github_state = form.my_github_state.data
        follow_me = form.follow_me.data

        string = '{}\n{}\n{}\n\n'.format(github, my_github_state, follow_me)
        save_data(string)

        return redirect( url_for('form_result'))

    return render_template("form_a.html", form=form)

@app.route('/form_b', methods=["GET", "POST"])
def form_b():

    form_2= Y()
    if form_2.validate_on_submit():

        link_muzyka = form_2.link_muzyka.data

        string_1 = '\n{}\n'.format(link_muzyka)
        save_linki(string_1)

        return redirect( url_for('form_result'))
    return render_template("form_b.html", form=form_2)

@app.route('/form_result')
def form_result():
    return render_template("form_result.html")


# Helpers

def save_linki(string_1):
    
    if not 'dane' in os.listdir():
        os.mkdir('dane')
        if not 'linki_muzyczne.txt' in os.listdir('dane'):
             os.system('touch linki_muzyczne.txt')
            
    with open('dane/linki_muzyczne.txt', "a+") as f:
        f.write(string_1)


def save_data(string):
    
    if not 'dane' in os.listdir():
        os.mkdir('dane')
        if not 'notatnik.txt' in os.listdir('dane'):
             os.system('touch notatnik.txt')
            
    with open('dane/notatnik.txt', "a+") as f:
        f.write(string)


# Errors

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500


# Form

class Y(FlaskForm):
    

    link_muzyka = StringField('Twoja piosenka:', validators=[DataRequired()])

    button = SubmitField('ok')
    



class X(FlaskForm):
    x_options = [
            ('a','a'),
            ('a','b'),
            ('c','c'),
            ('d','d'),
    ]

    github = StringField('Twój github:', validators=[DataRequired()])
    my_github_state = SelectField('Ogarniam githuba na:', choices=x_options)
    follow_me = BooleanField('Followuj mnie na gitubie :)')

    button = SubmitField('ok')


@app.route('/flaga', methods=["GET", "POST"])
def flaga():
	create_folders()

	# Flag.
	ta_flaga = os.path.join(app.config['UPLOAD_FOLDER'], 'flag_image/Polska_Flaga__11.jpg')
	
	# Gather heroes.
	heroes = gather_heroes()
	random.shuffle(heroes)

	return render_template("flaga.html", flaga=ta_flaga, heroes=heroes)

def gather_heroes():
	
	heroes = [
 		'Mikołaj Kopernik', 
 		'Rotmistrz Pilecki',
 		'Maria Skłodowska',
 		'Fryderyk Chopin',
		
 		#'Józef Piłsudski'
 		#'Tadeusz Kościuszko',
 		#'Adam Mickiewicz',
 		
		#'Jan Henryk Dąbrowski',
 		# 'Józef Haller',
 		# 'Władysław Sikorski',
		# 'Wojciech Korfanty',
 		# 'Mieczysław Paluch',
		
	]

	greetings = [
		'pozdrawia',
		'/wave',
		'/wink',
		'wita',
	]

	wikipedia.set_lang("pl")

	saved_heroes = os.listdir('saved_heroes')
	saved_heroes = [h.split('.')[0] for h in saved_heroes]

	for hero in heroes:
		if hero not in saved_heroes:

			# Get some info and link.
			some_info = wikipedia.page(hero)
			info_intro = some_info.content.split('\n\n')[0]
			url = '<a href="'+some_info.url+'">Poszukaj więcej info o: '+hero+"</a>"
			
			# Get what hero thinks.
			hero_think(hero)
			
			# Get & save images.
			# images = some_info.images
			# n_photos = 0
			# for i, image_url in enumerate(images):
			# 	if i < 3:
			# 		hero_str = '11'.join(hero.split())
			# 		image_name = '{}_{}.legend'.format(hero_str, i)
			# 		save_image(image_url, image_name)
			# 		n_photos += 1

			# Save all.
			with open('saved_heroes/'+hero+".hero", "w+") as f:
				f.write(hero + '\n')
				f.write('\n') #str(n_photos) + '\n')
				f.write(info_intro + '\n')
				f.write(url)

		else:
			greeting = random.choice(greetings)
			print(hero, greeting)

	heroes = []
	for hero_file in os.listdir('saved_heroes'):
		hero = {}
		some_info = open('saved_heroes/'+hero_file).readlines()
		hero['name'] = some_info[0]
		#photo_nr = random.choice(range(int(some_info[1])))
		#hero_str = '11'.join(hero['name'][:-1].split())
		#hero['image'] = '{}_{}.legend'.format(hero_str, photo_nr)
		hero_quotes = open('hero_think/' + hero['name'][:-1] + ".hero").readlines()
		hero['quote'] = random.choice(hero_quotes)
		hero['description'] = '\n'.join(some_info[2:-1])
		hero['description'] = bold(hero['description'])
		hero['url'] = some_info[-1]
		heroes.append(hero)

	return heroes

# def save_image(image_url, image_name):
# 	image = requests.get(image_url).content
# 	save_as = 'static/hero_image/{}'.format(image_name)
# 	with open(save_as, 'wb') as ap:
# 		ap.write(image)
# 	return save_as

def bold(hero_info):

	nice = [
		'nauk',
		'gen',
		'zwy',
		'odk',
		'zał',
		'rod',
		'organizator',
		'astronom',
		'inżynier',
		'herbu',
		'wojska',
		'uczona',
		'nobla',
		'wybitniej',
		'romantyczny',
		'fizyk',
		'filozof',
		'kocha',
		'woli',
		'kawalerii',
		'skazany',
	]

	right_desc = []
	words = [w.lower() for w in hero_info.split()]
	for w in words:
		for woah in nice:
			if w.startswith(woah):
				w = '<b>'+w+'</b>'
		right_desc.append(w)
	right_desc = " ".join(right_desc)
	return right_desc

def hero_think(name):
	url_name = name.replace(' ', '_')
	url = 'https://pl.wikiquote.org/wiki/{}'.format(url_name)
	hero_wikiquotes = requests.get(url)
	with open('hero_think/'+name+".hero", "w+") as f:
		
		for line in hero_wikiquotes.text.split('\n'):
			if line.startswith('<h2>O'):
				continue
			if line.startswith('<ul><li>'):
				
				tree = html.fromstring(line)
				quote = tree.text_content().strip()
				
				if not quote.startswith('Opis') and not quote.startswith('Autor') and not quote.startswith('Źródło'): 
					f.write(quote + '\n')
					print('-', quote)

def create_folders():
	os.system("mkdir static/hero_image")
	os.system("mkdir static/flag_image")
	os.system("mkdir saved_heroes")
	os.system("mkdir hero_think")


if __name__ == "__main__":
	app.run(debug=True)

