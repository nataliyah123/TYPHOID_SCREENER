import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
import pyrebase
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.factory import Factory
from android.permissions import request_permissions, Permission

request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                     Permission.READ_EXTERNAL_STORAGE])

import os
# folder = os.path.dirname(os.path.realpath(__file__))
config ={
	
  "apiKey": "AIzaSyDLdBkSysTsUAe0wTpm99ekeVt6V-Xqpkk",
  "authDomain": "testingcloudstorage-db6b3.firebaseapp.com",
  "projectId": "testingcloudstorage-db6b3",
  "storageBucket": "testingcloudstorage-db6b3.appspot.com",
  "messagingSenderId": "359473405022",
  "appId": "1:359473405022:web:6d54a9934600416edbe8cf",
  "databaseURL": "your db ibia"
}

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Uploader(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    #loadfile = ObjectProperty(None)
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    

    def load(self, path, filename):
        print("this should be it ibia", filename, path)
        #with open(os.path.join(path, filename[0])) as stream:
        with open(os.path.join(path, filename[0])):
            print("when is the lad", os.path.split(filename[0])[1], path)
            firebase = pyrebase.initialize_app(config)
            storage = firebase.storage()
            tail = os.path.split(filename[0])[1]
            path_on_cloud = tail
            local_path = filename[0]
            print("I am filen_name and local_path and local_path", tail,path_on_cloud, local_path)
            storage.child(path_on_cloud).put(local_path)
                # self.text_input.text = stream.read()

        self.dismiss_popup()
    
 
    
   