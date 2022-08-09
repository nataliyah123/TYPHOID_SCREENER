from kivy.config import Config
from kivy.lang import Builder
from kivy.app import App
# from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.picker import MDDatePicker
from kivy.properties import ObjectProperty
import kivy
# try:
#     import cv2
# except:
#     from cv import cv2
# import numpy as np

#from kivy.uix.camera import Camera   ## uncomment for android
from kivy.graphics.texture import Texture
import time
import sqlite3
from predict import Predict 
import time
import sqlite3
import os
from uploader import Uploader
from uploader import LoadDialog

folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/predict.kv")
features = []
textval = ""
print("I need to know what is your platform ibia", platform)
if platform == 'android':
  #from android.permissions import request_permissions, Permission   ibia uncomment this line
  def callback(permission, callbacks):
    if all([res for res in results]):
      print("All premissions are granted")
    else:
      print("Not all permissions are granted")
    # request_permissions([
    #   Permission.CAMERA,
    #   Permission.WRITE_EXTERNAL_STORAGE,
    #   Permission.READ_EXTERNAL_STORAGE
    # ])

Config.set('graphics','resizable',True)

class ScreenManagement(ScreenManager):
    pass

class FirstPage(Screen):
    pass    

class SecondPage(Screen):
    pass

class ThirdPage(Screen): 
    pass

class FourthPage(Screen): 
    pass

class Features(Screen):
    pass
    
class FifthPage(Screen):
    pass 

class SixthPage(Screen):
    pass 

class SeventhPage(Screen):
    pass   

class EightPage(Screen):
    pass    

class NinthPage(Screen):
    pass

# class Camera2(Camera):
#     firstFrame=None
#     def _camera_loaded(self, *largs):
#         if kivy.platform=='android':
#             self.texture = Texture.create(size=self.resolution,colorfmt='rgb')
#             self.texture_size = list(self.texture.size)
#         else:
#             super(Camera2, self)._camera_loaded()

#     def on_tex(self, *l):
#         if kivy.platform=='android':
#             buf = self._camera.grab_frame()
#             if not buf:
#                 return
#             frame = self._camera.decode_frame(buf)
#             self.image = frame = self.process_frame(frame)
#             buf = frame.tostring()
#             self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
#         super(Camera2, self).on_tex(*l)

    # def process_frame(self,frame):
    #     r,g,b=cv2.split(frame)
    #     frame=cv2.merge((b,g,r))        
    #     rows,cols,channel=frame.shape
    #     M=cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    #     dst=cv2.warpAffine(frame,M,(cols,rows))
    #     frame=cv2.flip(dst,1)
    #     if self.index==1:
    #         frame=cv2.flip(dst,-1)
    #     return frame 
    # pass

class Camera2(Screen):
    pass

class EleventhPage(Screen): 
    pass

class TwelvethPage(Screen):
    pass
  

class TestApp(MDApp):
    title = "Mboalab Typoid Diagnostics"
    dialog = None
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.accent_palette = "Blue"

        #app icon
        self.icon = "images/logo.png"
        
        # # Create Database Or Connect To One
        # conn = sqlite3.connect('doctechpat.db')
        # c = conn.cursor()

        # c.execute("SELECT * FROM 'doctortech' LIMIT 0,1")
        # records = c.fetchall()
        # print("salam ibia", records[0])    
        Builder.load_file('login.kv')  
        Builder.load_file(folder + "/uploader.kv")      
        return ScreenManagement()

    def Sign_Up_doctech(self):
        print("this is testin", self.root.ids.page3.ids.user_signup.text)
        conn = sqlite3.connect('doctechpat.db')       
        c = conn.cursor()        

        c.execute("INSERT INTO doctortech (person_name, email, occupation, organization,password) values(?,?,?,?,?)",

            [
                 self.root.ids.page3.ids.user_signup.text,
                 self.root.ids.page3.ids.signup_email.text,
                 self.root.ids.page3.ids.occupation.text,
                 self.root.ids.page3.ids.organization.text,
                 self.root.ids.page3.ids.password.text                
            ])
        conn.commit()
        conn.close()
        self.dialog = MDDialog(
                title = 'Congratulations!',
                text = 'You have successfully signed in to Mboalab.\nPlease click "Ok" to land on the image and data option page.',
                size_hint = (0.7,0.2),
                buttons = [MDFlatButton(text='Ok',on_release = self.move)]
                )
        self.dialog.open()

    def submit_pat_info(self):
        # this should have some sort of checks for the fields to comply with the format
        print("this is testin", self.root.ids.page4.ids.date.text)
        conn = sqlite3.connect('doctechpat.db')       
        c = conn.cursor()        
        c.execute("INSERT INTO Patientinfo (patientname,country, city, state,phone,email,GENDER,ETHNICITY,recordentrydate ) values(?,?,?,?,?,?,?,?,?)",
            [
                 self.root.ids.page4.ids.patient_name.text,
                 self.root.ids.page4.ids.country.text,
                 self.root.ids.page4.ids.city.text,
                 self.root.ids.page4.ids.state.text,
                 self.root.ids.page4.ids.phone.text,
                 self.root.ids.page4.ids.signup_email.text,
                 self.root.ids.page4.ids.gender.text,
                 self.root.ids.page4.ids.ethnicity.text,
                 self.root.ids.page4.ids.date.text               
                
            ])
        conn.commit()
        conn.close()

    def checkbox_func_arr(self, instance, value, feat_value):
        # conn = sqlite3.connect('doctechpat.db')       
        # c = conn.cursor()        
        #print("checking personnel name and patient name",self.root.ids.page4.ids.date.text,self.root.ids.page4.ids.date.text )
        if value == True:  
             if(feat_value=="High"):
                features.append(2)
             elif(feat_value=="Low"):
                features.append(1)
             else:
                features.append(0)   

    def for_checking(self):
        features.insert(0,self.root.ids.features.ids.patient_name_features.text)
        features.insert(1,self.root.ids.features.ids.personnel_id_features.text)
        features.insert(21,self.root.ids.features.ids.date_features.text)
        print("checkboxes check", self.checkbox_func_arr, features) 

    def submit_pat_features(self):
        # a dialog should be added to check whether the patient is in db or not
        
        self.checkbox_func_arr
        if(len(features) < 18):
            self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter all the fields',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
            self.dialog.open()
        else:
           features.insert(0,self.root.ids.features.ids.patient_name_features.text)
           features.insert(1,self.root.ids.features.ids.personnel_id_features.text)
           features.insert(20,self.root.ids.features.ids.date_features.text) 
           print("checking the feature arr", features)
           conn = sqlite3.connect('doctechpat.db')       
           c = conn.cursor()        
           c.execute("INSERT INTO Patientfeatures(patientid,personnel_id,Fever,Abdominal_Pain,Cough,Diarrheoa,Constipation,Rose_spots,Muscle_Weakness,Anorexia,Headache,Skin_Rash,Wieghtless,Stomach_distention,Malaise,Occult_blood_in_stool,Haemorrahages,Derilium,Abdominal_rigidity,Epistaxis,recordentrydate) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", features)
           conn.commit()
           conn.close()  

    def Login(self):
        print("this is login", self.root.ids.page2.ids.user.text)
        conn = sqlite3.connect('doctechpat.db')       
        c = conn.cursor()                      
        c.execute("SELECT person_name, password FROM 'doctortech' where person_name = ? AND password = ? ", (self.root.ids.page2.ids.user.text,self.root.ids.page2.ids.password.text))

        usr_data = c.fetchall()
        loginName = self.root.ids.page2.ids.user.text
        loginPassword = self.root.ids.page2.ids.password.text
        # print("this is usr_data", usr_data[0],loginName)  

        #when username or password is empty
        if(loginName.split() == [] and loginPassword.split() == []):
            self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter all the fields',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
            self.dialog.open()      
        elif (len(usr_data) == 0):
            # if not self.dialog:
                # create dialog
            print("I am inside login usr_Data len",len(usr_data))
            self.dialog = MDDialog(
                title="Sign up notice",
                text=f"Please Sign up! or provide a valid username and password",
                buttons=[
                    MDFlatButton(
                        text="Ok", text_color=self.theme_cls.primary_color, 
                        on_release=self.close
                    ),
                ],
            )
            self.dialog.open()        

        elif(usr_data[0][0] == self.root.ids.page2.ids.user.text and usr_data[0][1] == self.root.ids.page2.ids.password.text):
            # print("I am elif usr",usr_data, usr_data[0][1], usr_data[0][0] == self.root.ids.page2.ids.user.text, usr_data[0][1] == int(self.root.ids.page2.ids.password.text))
            print("checking manager", self.root.current)
            print("this is page4 ibia", self.root)
            self.root.current = 'sixth_page' 

                        
        #self.root.ids.word_label.text = f'{self.root.ids.user_signup.text} Added'       
        #self.root.ids.word_input.text = ''
        # ibia.............. self.root.manager.current is used whereas outside this function in testApp it is not
        conn.commit()
        conn.close()
    
    #when "Ok" is clicked in the date picker
    def on_save(self,instance,value,date_range):
        print("on_Save value", value)
        if(self.textval == "patient_features_val"):
            self.root.ids.features.ids.date_features.text= str(value) 
        elif(self.texval == "fourth_page"):     
            self.root.ids.page4.ids.date.text = str(value)

    #when "Cancel" is clicked in the date picker
    def on_cancel(self,instance,value):
        return

    #function for date picker
    def show_date_picker(self,textval):
        date_dialog = MDDatePicker()
        self.textval = textval
        date_dialog.bind(on_save = self.on_save,on_cancel=self.on_cancel)
        date_dialog.open()

    #changes then from dark to light and vice-versa
    def theme_changer(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def changer(self,*args):
        self.root.current = 'fourth_page'    

    def close(self, instance):
        # close dialog
        self.dialog.dismiss()

    def move(self, instance):
        self.root.current = 'sixth_page'
        self.dialog.dismiss()

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''        

        #camera = self.root.ids.page10.ids.camera #uncomment for android devt0
        #timestr = time.strftime("%Y%m%d_%H%M%S")        
        #camera.export_to_png("/sdcard/IMG_{}.png".format(timestr))

if __name__ == '__main__':
    app = TestApp()
    app.run()
