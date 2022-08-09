import kivy
from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
import sqlite3
from fpdf import FPDF

typhoidresult = ""
typhoid_results = ""
nameofpatient =""
	
class Predict(FloatLayout):    
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()
    def predictusingai(self):
        conn = sqlite3.connect('doctechpat.db')       
        c = conn.cursor()
        nameofpatient = self.ids.patientname.text
        if(nameofpatient == "" ):
            self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter a valid user',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
            self.dialog.open()        
        else:            
            c.execute("SELECT * FROM 'patientfeatures' where patientid =?", [nameofpatient])
            usr_data = c.fetchall()
            if(len(usr_data) == 0):
                self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter a valid user',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
                self.dialog.open()
            else:
                c.execute("SELECT * from 'patientfeatures' where patientid =?", [nameofpatient])
                pat_data = c.fetchall()
                Fever,Abdominal_Pain,Cough,Diarrheoa,Constipation,Rose_spots,Muscle_Weakness,Anorexia,Headache,Skin_Rash,Wieghtless,Stomach_distention,Malaise,Occult_blood_in_stool,Haemorrahages,Derilium,Abdominal_rigidity,Epistaxis= pat_data[0][2],pat_data[0][3],pat_data[0][4],pat_data[0][5],pat_data[0][6],pat_data[0][7],pat_data[0][8],pat_data[0][9],pat_data[0][10],pat_data[0][11],pat_data[0][12],pat_data[0][13],pat_data[0][14],pat_data[0][15],pat_data[0][16],pat_data[0][17],pat_data[0][18],pat_data[0][19]
                
                if ((Muscle_Weakness==1) and (Anorexia==1) and (Headache==1) and (Skin_Rash==1) and (Wieghtless==1) and (Stomach_distension==1) and (Haemorrahages==1) and(Derilium==1)):
                    return "Very low risk"
                if((Anorexia==1) and (Skin_Rash==1) and (Wieghtless==2) and (Haemorrahages==1)):
                    return "Low risk"
                if( (Diarrheoa==1) and (Constipation==1) and (Muscle_Weakness==1) and (Headache==2) and (Malaise==1)):    
                    return "Low risk"
                if((Diarrheoa==1) and (Muscle_Weakness==1) and (Anorexia ==2) and (Headache==1) and (Wieghtless==1) and (Epitaxis==1)):
                    return "Low risk"
                if( (Muscle_Weakness==1) and (Anorexia==1) and (Headache==2) and (Skin_Rash==1) and (Malaise==1) and (Occult_blood_on_stool==1)):  
                    return "Low risk"  
                if((Muscle_Weakness==2) and (Occult_blood_in_stool==1) and (Haemorrahages==1) and (Epitaxis==1) and (Malaise==1) and (Occult_blood_on_stool==1)):
                    return "Moderate risk"   
                if( (Diarrheoa==1) and (Headache==1) and (Stomach_distension==2)): 
                    return "Moderate risk"
                if((Skin_Rash==2) and (Occult_blood_in_stool==1) and (Haemorrahages==1) and (Epitaxis==1)): 
                    return "Moderate risk"
                if((Malaise==2) and (Occult_blood_in_stool==1) and (Haemorrahages==1) and (Epitaxis==1)):
                    return "Moderate risk"
                if( (Diarrheoa==2) and (Anorexia==2) and (Haemorrahages==1)):
                    return "Moderate risk"
                if( (Muscle_Weakness==2) and (Haemorrahages==2) and (Derilium==1)):  
                    return "High risk"
                if( (Headache==2) and (Haemorrahages==2) and (Derilium==1)): 
                    return "High risk"
                if((Constipation==1) and (Occult_blood_in_stool==2) and (Derilium==1)): 
                    return "High risk"
                if((Muscle_Weakness==1) and(Anorexia==1) and (Haemorrahages==2)):
                    return "High risk"                
                if((Derilium==2)):  
                    return "Very High risk"
                if((Diarrheoa==1) and (Muscle_Weakness==2) and (Skin_Rash ==2) and (Wieghtless==1) and(Haemorrahages==1)):
                    return "Very High risk"
                if((Constipation==2) and (Muscle_Weakness==1) and (Anorexia==2) and (Headache==2) and (Haemorrahages== 1)):                               
                    return "Low or Moderate risk"
                if((Constipation==1) and (Muscle_Weakness==1) and (Anorexia==2) and (Headache==1) and (Wieghtless==1) and (Haemorrahages==1)):
                    return "High or Very High Risk" 

    def show_results(self):  
        typhoid_results = self.predictusingai()        
        self.ids.predict_patlab.text = ""
        self.ids.typhoidresult.opacity = 1
        self.ids.typhoidresult.text = "Patient" + " "+ (self.ids.patientname.text) +" has " + typhoid_results + " " + "typhoid"        
        self.ids.patientname.opacity = 0
    def generatePDF(self):        
        pdf = FPDF() 
        # Add a page
        pdf.add_page()    
        #add text        
        reportxt = "The patient" +" "+ (self.ids.patientname.text) +" has " + self.predictusingai()     
        # set style and size of font
        # that you want in the pdf
        pdf.set_font("Arial", size = 15)         
        # create a cell        
        pdf.cell(200, 10, txt = reportxt,	
                 ln = 1, align = 'C')

        # save the pdf with name .pdf
        nameoffile = (self.ids.patientname.text) + ".pdf"
        pdf.output(nameoffile) 
        print("I am pdf genrator*** end ibia")
