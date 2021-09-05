from bson.objectid import ObjectId
from project import mongo
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self,email,name,username,password):
        self.name=name
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.email
    

class UsersDB(UserMixin):
    
    def getUser(self,email):
        return mongo.db.users.find_one({'Email':email})
    def getPass(self,email):
        return mongo.db.users.find_one({'Email':email})['password']
    def checkPass(self,hash_paas,paas):
        return check_password_hash(hash_paas,paas)
            
    def saveUser(self,f_name,email,username,password):
        self.user_details={'Full Name':f_name,
                        'Email':email,
                        'username':username,
                        'password':generate_password_hash(password)
                    }
        mongo.db.users.insert(self.user_details)

class Theatre:
    #_id,Name,Movie Name, MOvie Duration, Movie slots, Ticket Available, Ticket Booked
    theatre=mongo.db.theatres
    def getAllTheatreDetails(self):
        return list(self.theatre.find())
    
    def getTheatreDetails(self,id):
        return self.theatre.find_one({'_id':ObjectId(id)})
    
    def getAvailableSeats(self,id):
        return int(self.theatre.find_one({'_id':ObjectId(id)})['Seats Available'])

    def bookTicket(self,id,ticketCount):
        filterquery={'_id':ObjectId(id)}
        updatequery={"$inc":{'Seats Available':-ticketCount,
                                'Seats Booked':ticketCount }}
        self.theatre.update_one(filterquery,updatequery)


class Ticket:
    ticket=mongo.db.tickets
    def generateTicket(self,id,current_user,person_name,ticket_count):
        theatre_details=Theatre().getTheatreDetails(id)

        ticket_details={
                            'email': current_user.email,
                            'username':current_user.username,
                            'person name':person_name,
                            'person count':ticket_count,
                            'theatre name':theatre_details['Name'],
                            'movie name':theatre_details['Movie Name'],
                            'movie duration':theatre_details['Movie Duration'],
                            'movie timing':theatre_details['Movie Timing']
                            }

        ticketGenerated=self.ticket.insert_one(ticket_details)
        return ticketGenerated
    
    def getTicketDetails(self,id):
        return self.ticket.find_one({'_id':ObjectId(id)})
    
    def getBookedTicketByEmail(self,email):
        return self.ticket.find({'email':email})
