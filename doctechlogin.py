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

class Doctechlogin(FloatLayout, EventDispatcher):
    def Login(self):
        print("I am login")
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
