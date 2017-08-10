from django.core.cache import cache

class User:
    def __init__(self,userid,username,password,email,phone):
        self.userid = userid
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

    def SetPassword(self,newpwd):
        self.password = newpwd

    def GetPassword(self):
        self.password = newpwd 
