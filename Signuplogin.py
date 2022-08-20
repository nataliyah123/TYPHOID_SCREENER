from kivy.event import EventDispatcher
from kivy.uix.floatlayout import FloatLayout
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import certifi
from json import dumps
from firebase import firebase

class Signuplogin(FloatLayout, EventDispatcher):    
    web_api_key = "AIzaSyDLdBkSysTsUAe0wTpm99ekeVt6V-Xqpkk"  
    refresh_token = ""
    localId = ""
    idToken = ""  
    def generate_doc_tech_id(self,occupation,response):
        ourkeys = response.keys()
        lastdoctecid = response[list(ourkeys)[-1]]['personnel_id']
        number = ''
        alpha = ''
        for i in range(len(lastdoctecid)):
            if lastdoctecid[i].isdigit():
                number = number + lastdoctecid[i]
            else:
                alpha = alpha + lastdoctecid[i]
        number = str(int(number) + 1)
        if (occupation == 'Docter'):
            doctecid = 'Doc' + number
        else:
            doctecid =  'Tec' + number
        return doctecid         
    
    def Sign_Up_doctech(self, email, password):        

        signupUsername = self.ids.user_signup.text
        signupEmail = self.ids.signup_email.text
        occupation = self.ids.occupation.text
        organization = self.ids.organization.text
        signupPassword = self.ids.password.text
        if(signupUsername.split() == [] or signupEmail.split() == [] or occupation.split() == [] or organization.split() == [] or signupPassword.split() == []):
            
            self.dialog = MDDialog(title = 'Invalid Input !',
                    text = 'Please enter all the required fields.',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
            self.dialog.open()
        elif(signupUsername.split() == [] and signupEmail.split() == [] and occupation.split() == [] and organization.split() == [] and signupPassword.split() == []):
            self.dialog = MDDialog(title = 'Invalid Input !',
                    text = 'Please enter all the required fields.',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
            self.dialog.open()      
        else:            
            signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + self.web_api_key
            signup_payload = dumps(
                {"email": email, "password": password, "returnSecureToken": "true"})
            try: {
                UrlRequest(signup_url, req_body=signup_payload,
                           on_success=self.successful_sign_up,
                           on_failure=self.sign_up_failure,
                           on_error=self.sign_up_error, ca_file=certifi.where())
            }
            except:{
                print("wht is th error ibia",Error)
            }      
            # firebase = firebase.FirebaseApplication('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/', None)
            # result = firebase.get('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/doctertech', '') 
            print("whta is teh value of firebase if internet is off")
                # }
            # except on_error:{
            # self.dialog = MDDialog(title = 'Error !',
            #     text = on_error,
            #     size_hint = (0.7,0.2),
            #     buttons = [MDFlatButton(text='Ok',on_release = self.close)]
            #     )
            # self.dialog.open()
            # # }    
            # doctertech = {
            #     "person_name":self.ids.user_signup.text,
            #     "personnel_id": self.generate_doc_tech_id(self.ids.occupation.text,result),
            #     "occupation": self.ids.occupation.text,
            #     "organization": self.ids.organization.text,
            #     "email": self.ids.signup_email.text,
            # }
            # firebase.post('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/doctertech', doctertech)

        # signupUsername = self.ids.user_signup.text
        # signupEmail = self.ids.signup_email.text
        # occupation = self.ids.occupation.text
        # organization = self.ids.organization.text
        # signupPassword = self.ids.password.text 
        
        # if(signupUsername.split() == [] or signupEmail.split() == [] or occupation.split() == [] or organization.split() == [] or signupPassword.split() == []):
            
        #     self.dialog = MDDialog(title = 'Invalid Input !',
        #             text = 'Please enter all the required fields.',
        #             size_hint = (0.7,0.2),
        #             buttons = [MDFlatButton(text='Ok',on_release = self.move)]
        #             )
        #     self.dialog.open()         

    def successful_sign_up(self, request,result):
        from firebase import firebase        
        # print("Successfully signed up a user: ")
        # self.hide_loading_screen()
        self.refresh_token = result['refreshToken']
        self.localId = result['localId']
        self.idToken = result['idToken'] 
        firebase = firebase.FirebaseApplication('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/', None)
        result = firebase.get('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/doctertech', '')        
        print("I am printing results", result)
        doctertech = {
                "person_name":self.ids.user_signup.text,
                "personnel_id": self.generate_doc_tech_id(self.ids.occupation.text,result),
                "occupation": self.ids.occupation.text,
                "organization": self.ids.organization.text,
                "email": self.ids.signup_email.text,
            }

        firebase.post('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/doctertech', doctertech)
        self.send_verification_email(self.ids.signup_email.text)
        
    def send_verification_email(self, email):
        
        verify_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + self.web_api_key + "&lang=fr"
        verify_email_data = dumps(
            {"idToken": self.idToken, "requestType": "VERIFY_EMAIL"})

        UrlRequest(verify_email_url, req_body=verify_email_data,
                   on_success=self.successful_verify_email_sent,
                   on_failure=self.unsuccessful_verify_email_sent,
                   on_error=self.unsuccessful_verify_email_sent,
                   ca_file=certifi.where())
        
        self.dialog = MDDialog(title = 'Congratulations!',
                    text = 'You have successfully signed up to Mboalab.\nPlease click "Ok" to land on the image and data option page.',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.move)]
                    )
        self.dialog.open()
        self.parent.parent.current = 'second_page'
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()
    def move(self,*args):
        # print("I am testing parent ibia")
        self.parent.parent.current = 'second_page'
        # self.dialog.dismiss()  

    def unsuccessful_verify_email_sent(self, *args):
        print("Couldn't send email verification email*************")
        self.dialog = MDDialog(title = 'Email dispatch failure!',
                    text = "Couldn't send verification email",
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()

    def successful_verify_email_sent(self, *args):
        # print("A verification email has been sent. \nPlease check your email.")
        self.dialog = MDDialog(title = 'Verification email!',
                    text = "A verification email has been sent. \nPlease check your email.",
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()

    def sign_up_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to log in was
        invalid.
        """        
        self.email_exists = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        # print("I am testin failure_Data",msg, failure_data)
        #the dialog box below is not working
        self.dialog = MDDialog(title = 'Sign up failure!',
                    text = str(msg),
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()
        
    def sign_up_error(self,  *args):
        
        self.dialog = MDDialog(title = 'Sign up failure!',
                    text = str(args[1]),
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Ok',on_release = self.close)]
                    )
        self.dialog.open()
        # print("Sign up Error)))))))))))))))))))): ", args[1], args)

    # def successful_sign_up(self, request, result):
        
    #     # print("Successfully signed up a user: ", result)        
    #     self.refresh_token = result['refreshToken']
    #     self.localId = result['localId']
    #     self.idToken = result['idToken']
    #     self.send_verification_email(result['email'])  
    # 