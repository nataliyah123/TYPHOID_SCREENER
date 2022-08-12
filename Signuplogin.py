from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.floatlayout import FloatLayout
import certifi
from json import dumps
# import os.path
import sqlite3

#folder = os.path.dirname(os.path.realpath(__file__))


class Signuplogin(FloatLayout, EventDispatcher):
    
    # web_api_key = StringProperty()
    web_api_key = "AIzaSyDLdBkSysTsUAe0wTpm99ekeVt6V-Xqpkk"  
    refresh_token = ""
    localId = ""
    idToken = ""   
    def checkbutton(self):
        print('checking button', self.parent.parent.ids)
    def Sign_Up_doctech(self, email, password):
        # print("this is testin", self.root.ids.page3.ids.user_signup.text)
        loginpage = self.parent.parent.ids
        checkcurrent = self.parent.parent.current
        # print("I am testing email", email,checkcurrent)
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
        signup_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": "true"})

        UrlRequest(signup_url, req_body=signup_payload,
                   on_success=self.successful_sign_up,
                   on_failure=self.sign_up_failure,
                   on_error=self.sign_up_error, ca_file=certifi.where())

        conn = sqlite3.connect('doctechpat.db')       
        c = conn.cursor()        

        c.execute("INSERT INTO doctortech (person_name, email, occupation, organization,password) values(?,?,?,?,?)",

            [
                 self.ids.user_signup.text,
                 self.ids.signup_email.text,
                 self.ids.occupation.text,
                 self.ids.organization.text,
                 self.ids.password.text                
            ])
        conn.commit()
        conn.close()

        signupUsername = self.ids.user_signup.text
        signupEmail = self.ids.signup_email.text
        occupation = self.ids.occupation.text
        organization = self.ids.organization.text
        signupPassword = self.ids.password.text 
        
        if(signupUsername.split() == [] or signupEmail.split() == [] or occupation.split() == [] or organization.split() == [] or signupPassword.split() == []):
            # self.dialog = MDDialog(
            #         title = 'Invalid Input !',
            #         text = 'Please enter all the required fields.',
            #         size_hint = (0.7,0.2),
            #         buttons = [MDFlatButton(text='Retry',on_release = self.close)]
            #         )
            # self.dialog.open()
            title = 'Invalid Input !'
            text = 'Please enter all the required fields.'
            custom_release = self.close
            adialogbox(self,title, text, custom_release)   

        # else:
            # self.dialog = MDDialog(
            #         title = 'Congratulations!',
            #         text = 'You have successfully signed up to Mboalab.\nPlease click "Ok" to land on the image and data option page.',
            #         size_hint = (0.7,0.2),
            #         buttons = [MDFlatButton(text='Ok',on_release = self.move)]
            #         )
            # self.dialog.open()
            

    def adialogbox(self,title, text, custom_release):
        self.dialog = MDDialog(
                    title = title,
                    text = text,
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = custom_release)]
                    )
        return self.dialog.open()


    def successful_sign_up(self, request):        
        print("Successfully signed up a user: ")
        # self.hide_loading_screen()
        self.refresh_token = result['refreshToken']
        self.localId = result['localId']
        self.idToken = result['idToken']        
        self.send_verification_email(result['email'])
        title = 'Congratulations!',
        text = 'You have successfully signed up to Mboalab.\nPlease click "Ok" to land on the image and data option page.',
        custom_release = self.close
        adialogbox(self,title, text, custom_release)
        self.parent.parent.current = 'second_page'   #this refers to login.kv ids 

    def send_verification_email(self, email):
        verify_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + self.web_api_key + "&lang=fr"
        verify_email_data = dumps(
            {"idToken": self.idToken, "requestType": "VERIFY_EMAIL"})

        UrlRequest(verify_email_url, req_body=verify_email_data,
                   on_success=self.successful_verify_email_sent,
                   on_failure=self.unsuccessful_verify_email_sent,
                   on_error=self.unsuccessful_verify_email_sent,
                   ca_file=certifi.where())    

        
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()

    def move(self, instance):
        self.root.current = 'sixth_page'
        self.dialog.dismiss()  

    def unsuccessful_verify_email_sent(self, *args):
        print("Couldn't send email verification email")

    def successful_verify_email_sent(self, *args):
        print("A verification email has been sent. \nPlease check your email.")

    def sign_up_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to log in was
        invalid.
        """
        self.hide_loading_screen()
        self.email_exists = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        print("I am testin failure_Data",msg, failure_data)
        
    def sign_up_error(self, *args):
        print("Sign up Error: ", args)

    def successful_sign_up(self, request, result):
        
        print("Successfully signed up a user: ", result)        
        self.refresh_token = result['refreshToken']
        self.localId = result['localId']
        self.idToken = result['idToken']
        self.send_verification_email(result['email'])



    