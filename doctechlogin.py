from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.floatlayout import FloatLayout
import certifi
from json import dumps

email_not_found = BooleanProperty(False)
require_email_verification = BooleanProperty(True)
class Doctechlogin(FloatLayout, EventDispatcher):

    web_api_key = "AIzaSyDLdBkSysTsUAe0wTpm99ekeVt6V-Xqpkk"    
    def Login(self, email, password):
        print("I am logged in")    
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.sign_in_success,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where(),verify=True)

    def sign_in_failure(self, urlrequest, failure_data):
        
        self.email_not_found = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()        
        if msg == "Email not found":
            self.email_not_found = True
            
            self.dialog = MDDialog(
                    title = "SIGN IN FAILURE",
                    text = "PLEASE SIGN UP, EMAIL NOT FOUND",
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
            self.dialog.open()
        
        # print("this is login", self.root.ids.page2.ids.user.text)
        # conn = sqlite3.connect('doctechpat.db')       
        # c = conn.cursor()                      
        # c.execute("SELECT person_name, password FROM 'doctortech' where person_name = ? AND password = ? ", (self.root.ids.page2.ids.user.text,self.root.ids.page2.ids.password.text))

        # usr_data = c.fetchall()
        # loginName = self.root.ids.page2.ids.user.text
        # loginPassword = self.root.ids.page2.ids.password.text
        # # print("this is usr_data", usr_data[0],loginName)  

        # #when username or password is empty
        # if(loginName.split() == [] and loginPassword.split() == []):
        #     self.dialog = MDDialog(
        #             title = 'Invalid Input !',
        #             text = 'Please enter all the fields',
        #             size_hint = (0.7,0.2),
        #             buttons = [MDFlatButton(text='Retry',on_release = self.close)]
        #             )
        #     self.dialog.open()      
        # elif (len(usr_data) == 0):         
                
        #     # print("I am inside login usr_Data len",len(usr_data))
        #     self.dialog = MDDialog(
        #         title="Sign up notice",
        #         text=f"Please Sign up! or provide a valid username and password",
        #         buttons=[
        #             MDFlatButton(
        #                 text="Ok", text_color=self.theme_cls.primary_color, 
        #                 on_release=self.close
        #             ),
        #         ],
        #     )
        #     self.dialog.open()        

        # elif(usr_data[0][0] == self.root.ids.page2.ids.user.text and usr_data[0][1] == self.root.ids.page2.ids.password.text):
        #     # print("I am elif usr",usr_data, usr_data[0][1], usr_data[0][0] == self.root.ids.page2.ids.user.text, usr_data[0][1] == int(self.root.ids.page2.ids.password.text))
        #     print("checking manager", self.root.current)
        #     print("this is page4 ibia", self.root)
        #     self.root.current = 'sixth_page' 

                        
        # #self.root.ids.word_label.text = f'{self.root.ids.user_signup.text} Added'       
        # #self.root.ids.word_input.text = ''
        # # ibia.............. self.root.manager.current is used whereas outside this function in testApp it is not
        # conn.commit()
        # conn.close()
    def sign_in_success(self, urlrequest, log_in_data):
        
        self.refresh_token = log_in_data['refreshToken']
        self.localId = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        if self.require_email_verification:
            self.check_if_user_verified_email()

    def check_if_user_verified_email(self):       
        
        check_email_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.web_api_key
        check_email_verification_data = dumps({"idToken": self.idToken})

        UrlRequest(check_email_verification_url, req_body=check_email_verification_data,
                   on_success=self.got_verification_info,
                   on_failure=self.could_not_get_verification_info,
                   on_error=self.could_not_get_verification_info,
                   ca_file=certifi.where())
        self.parent.parent.current = 'third_page'
    
    def could_not_get_verification_info(self, request, result):        
        
        self.dialog = MDDialog(
                    title = "Error",
                    text = "Failed to check email verification status.",
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()
        



    def got_verification_info(self, request, result):        
        if result['users'][0]['emailVerified']:
            self.login_state = 'in'
            self.login_success = True
        else:
            self.dialog = MDDialog(
                    title = "Error",
                    text = "Your email is not verified yet.\n Please check your email.",
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
            self.dialog.open()

    def reset_password(self, email):     
        # print("Attempting to send a password reset email to: ", email)
        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.web_api_key
        reset_pw_data = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(reset_pw_url, req_body=reset_pw_data,
                   on_success=self.successful_reset,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def successful_reset(self,urlrequest, reset_data):
        self.dialog = MDDialog(
                    title = "RESET NOTICE",
                    text = 'Password Reset: A reset email is sent to your registered address',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()

    def sign_in_failure(self, request, result):
        # print("what is the result for reset", result["error"]["message"])
        message= 'Unsuccessful attempt'+ result["error"]["message"]
        self.dialog = MDDialog(
                    title = "SIGN IN FAILURE",
                    text = str(message),
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()
    def sign_in_error(self, *args):
        print('There is an error in resetting email')    

    def close(self, instance):
        # close dialog
        self.dialog.dismiss()    