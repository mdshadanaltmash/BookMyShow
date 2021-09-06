from project import app,login_manager,mongo
from flask.helpers import flash, url_for
from project.forms import BookTicketForm, LoginForm,RegistrationForm
from flask import redirect,url_for,flash,request
from flask.templating import render_template
from flask_login import login_user,logout_user,login_required,current_user
import project.models
from bson.objectid import ObjectId

@app.route('/')
def home():
    return  render_template('home.html')

@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('home'))


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    msg=''
    if form.validate_on_submit():
        user_info=project.models.UsersDB()
        user=user_info.getUser(email=form.email.data)
        if user:
            passInDb=user['password']
            if user_info.checkPass(passInDb,paas=form.password.data):
                login_user(project.models.User(user['Email'],user['Full Name'],user['username'],user['password']))
                flash('You have been Logged In!')
                next=request.args.get('next')
                if next is None or next[0]=='/':
                    next=url_for('welcome_user')
                return(redirect(next))
            else:
                msg='Invalid Username/Password'
                redirect(url_for('login'))
        else:
            msg='Invalid Username/Password'
            redirect(url_for('login'))
    return render_template('login.html',form=form,msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegistrationForm()

    if form.validate_on_submit():
        user=project.models.UsersDB()
        user_details=user.saveUser(f_name=form.f_name.data,
                            email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)

        flash('You have been registered!')
        return redirect(url_for('login'))
        
    return render_template('register.html',form=form)

@app.route('/theatres')
@login_required
def theatres():
    theatre=project.models.Theatre()
    theatreDetails=theatre.getAllTheatreDetails()
    return render_template('theatres.html',theatreDetails=theatreDetails)


@app.route('/book/<id>',methods=['GET','POST'])
@login_required
def book(id):
    msg=''
    theatre=project.models.Theatre()
    theatreDetails=theatre.getTheatreDetails(id)
    seat_available=theatre.getAvailableSeats(id)
    form=BookTicketForm()
    if form.validate_on_submit():
        ticket_count=int(request.form['ticket_count'])
        if seat_available>=ticket_count:
            ticket=project.models.Ticket()
            ticketGenerated=ticket.generateTicket(id,current_user,form.name.data,ticket_count)
            bookTicketStatus=theatre.bookTicket(id,ticket_count)
            #print(type(ticketGenerated),ObjectId(ticketGenerated.inserted_id))

            return redirect(url_for('ticketConfirmation',id=ObjectId(ticketGenerated.inserted_id)))
        else:
            msg="Cannot book more than available "+str(seat_available)+" seats"
            #return redirect(url_for('book',id=id))


    return render_template('book_ticket.html',theatreDetails=theatreDetails,msg=msg,form=form,current_user=current_user)

@app.route('/book/ticketconfirmation/<id>')
@login_required
def ticketConfirmation(id):
    ticket=project.models.Ticket()
    ticketDetails=ticket.getTicketDetails(id)

    return render_template('ticket_booked.html',id=id,ticketDetails=ticketDetails)

@app.route('/about')
@login_required
def about():
    email=current_user.email
    ticket=project.models.Ticket()
    allTickets=ticket.getBookedTicketByEmail(email)
    allTicketsCounts=allTickets.count()
    return render_template('about.html',allTickets=allTickets,allTicketsCounts=allTicketsCounts)


@login_manager.user_loader
def load_user(email):
    u= mongo.db.users.find_one({'Email':email})
    if not u:
        return None
    return project.models.User(u['Email'],u['Full Name'],u['username'],u['password'])

if __name__=='__main__':
    app.run(debug=True)
