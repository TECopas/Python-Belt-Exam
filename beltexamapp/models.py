from django.db import models
import bcrypt
import datetime
# Create your models here.
class UserManager(models.Manager):
    def regvalidator(self, postData):
        errors = {}

        if len(postData["Name"]) <3:
            errors["name"] = "Name requires an entry of 3 or more characters."

        if len(postData["Username"]) <3:
            errors["usernamename"] = " Username requires an entry of 3 or more characters."

        usernamecheck = User.objects.filter(username = postData["Username"])
        if len(usernamecheck) >0:
            errors["taken"] = "Username is already taken - please create a different Username"

        if len(postData["Password"]) < 8:
            errors["passwordlen"] = "Password requires an entry of 8 or more characters."
 
        if postData["Password"] != postData["Confirmation"]:
            errors["passwordregmatch"] = "Password and Confirmation entries must match."

        return errors

    def loginvalidator(self, postData):
        errors = {}

        if len(postData["Username"]) < 3:
            errors["invalidusernamelen"] = "Please enter a valid Username with 3 characters and a valid Password with 8 characters"
            return errors

        usernamecheck = User.objects.filter(username = postData["Username"])
        if len(usernamecheck) == 0:
            errors["nonexistantuser"] = "Username does not exist. Register for use."
            return errors
        logged_user = usernamecheck[0]

        if len(postData["Password"]) < 8:
            errors["invalidpasswordlen"] = "Please enter a valid Username with 3 characters and a valid Password with 8 characters"
            return errors

        if bcrypt.checkpw(postData["Password"].encode(), logged_user.password.encode()):
            print("*****STARS*****STARS*****STARS*****")
            print("PASSWORD MATCH")
            print("*****STARS*****STARS*****STARS*****")
        else:
            print("*****STARS*****STARS*****STARS*****")
            print("NO MATCH")
            print("*****STARS*****STARS*****STARS*****")
            errors["passwordmatch"] = "Password was not a match for a User."

        return errors

class TripManager(models.Manager):
    def tripvalidator(self, postData):
        errors = {}

        if len(postData["Destination"]) <1:
            errors["invaliddest"] = "Destination must be selected"

        if len(postData["Description"]) <1:
            errors["invaliddesc"] = "Description is required"

        if len(postData["TravelDateFrom"]) <1:
            errors["invalidFrom"] = "Trip Start Date must be selected"

        if len(postData["TravelDateTo"]) <1:
            errors["invalidTo"] = "Trip End Date must be selected"

        if postData["TravelDateFrom"] > postData["TravelDateTo"]:
            errors["negativetrip"] = "Travel Start Date must be before Travel End Date"

        if postData["TravelDateFrom"] < str(datetime.date.today()):
            errors["postdate"] = "Trips must be future dated."

        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    planner = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    description = models.TextField()
    TDFrom = models.DateField()
    TDTo = models.DateField()
    attendee = models.ManyToManyField(User, related_name="attendees")
    objects = TripManager()