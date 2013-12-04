from flask import render_template, redirect, flash, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from app import app, login_manager, db
from models import User
from forms import LoginForm, ProfileForm, RecLoginForm, ShortanswerForm, RecommendationsForm, TechskillsForm, RecommendApplicantForm, ChecklistForm
from emails import recommendation_request

applicant = {'email':'aliya@codeforprogress.org','firstname':'Aliya','lastname':'Rahman','password':'P@ssw0rd123','phone': '513-827-8299','address': '4141 Elbern Ave','city': 'Columbus','state': 'OH','zipcode': '43213'}
recommender =  {'email':'aliya@codeforprogress.org','firstname':'Someone','lastname':'Else','password':'autogenerated'}

@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

@app.route('/', methods= ['GET'])
@login_required
def index():
	return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = form.get_user()
		flash('Welcome, ' + user.firstname + '.')
		login_user(user)
		return redirect('/')
	return render_template('login.html',
		form=form)
		
@app.route('/checklist', methods = ['GET', 'POST'])
@login_required
def checklist():
	form = ChecklistForm()
	if form.validate_on_submit():
		return redirect('/')
	return render_template('checklist.html',
		form=form)

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
	if current_user.is_authenticated():
		user = current_user
	else:
		user = None

	form = ProfileForm(obj=user)

	if not form.password or form.password == '':
		del form.password

	if form.validate_on_submit():
		if user:
			flash('Successfully updated your profile.')
		else:
			user = User()

			flash('Congratulations, you just created an account!')

		form.populate_obj(user)
		db.session.add(user)
		db.session.commit()

		if not current_user.is_authenticated():
			login_user(user)

		return redirect('/checklist')

	return render_template('demographic.html', form=form)

#@app.route('/demographic', methods = ['GET', 'POST'])
#def demographic():
#	form = ProfileForm()
#	if form.validate_on_submit():
#		flash("We've updated your profile.")
#		return redirect('/demographic')
#	return render_template('demographic.html',
#		form=form)

@app.route('/shortanswers', methods = ['GET', 'POST'])
@login_required
def shortanswers():
	form = ShortanswerForm(obj=current_user)

	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash("Thanks, we've saved your responses to the short answer section.")
		return redirect('/')
	return render_template('shortanswers.html',
		form=form)

@app.route('/techskills', methods = ['GET', 'POST'])
@login_required
def techskills():
	form = TechskillsForm(obj=current_user)

	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash("Thanks, we've saved your responses to the tech survey.")

		return redirect('/')

	return render_template('techskills.html',
		form=form)

@app.route('/recommendations', methods = ['GET', 'POST'])
@login_required
def recommendations():
	form = RecommendationsForm(obj=current_user)
	
	if form.validate_on_submit():
		form.populate_obj(current_user)

		db.session.add(current_user)
		db.session.commit()

		flash('Your recommendation info has been saved.')
		return redirect('/')

	return render_template('recommendations.html',
		form=form)

@app.route('/finalsubmission')
def finalsubmission():
        return render_template("finalsubmission.html")

@app.route('/help')
def help():
        return render_template("help.html")

@app.route('/received')
def received():
#	def email_recommender():
		#email to notify recommenders that they have been asked to provide a recommendation
		#pass in object for current_user (applicant) and object for recommender
#		recommendation_request(recommender, applicant)
		return render_template("received.html")

@app.route('/recreceived')
def recreceived():
#	We could do an email function here too, to notify applicants that recommendations are in.
		return render_template("recreceived.html")

@app.route('/forgot')
def forgot():
        return render_template("forgot.html")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect("/")

@app.route('/reclogin', methods = ['GET', 'POST'])
def reclogin():
	form = RecLoginForm()
	if form.validate_on_submit():
		flash('Welcome, ' + form.username.data + '.')
		return redirect('/recindex')
	return render_template('reclogin.html',
		form=form)

@app.route('/recindex')
def recindex():
	return render_template("recindex.html")
	
@app.route('/recforgot')
def recforgot():
	return render_template("recforgot.html")
	
@app.route('/recform', methods = ['GET', 'POST'])
def recform():
	form = RecommendApplicantForm()
	if form.validate_on_submit():
		recommendation_request(recommender, applicant)
		flash('Your recommendation has been recorded.')
		return redirect('/recindex')
	return render_template('recform.html',
		form=form)

@app.route('/finalrecsubmission')
def finalrecsubmission():
	return render_template("finalrecsubmission.html")
	
@app.route('/reclogout')
def reclogout():
	return render_template("reclogin.html")

@app.route('/rechelp')
def rechelp():
        return render_template("rechelp.html")
