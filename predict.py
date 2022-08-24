import kivy
from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
from kivy.properties import ObjectProperty
from kivymd.uix.picker import MDDatePicker
from firebase import firebase
from fpdf import FPDF

typhoidresult = ""
typhoid_results = ""
nameofpatient =""
firebase = firebase.FirebaseApplication('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/', None)	
class Predict(FloatLayout):    
    def close(self, instance):
        # close dialog
        self.dialog.dismiss()
    def predictusingai(self):
        # conn = sqlite3.connect('doctechpat.db')       
        # c = conn.cursor()
        nameofpatient = self.ids.patientname.text
        recordentry = self.ids.recordentrydate.text
        print("first recordentry", recordentry)
        if(nameofpatient == "" or recordentry == "Record entry date"):
            self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter a valid user and date',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
            self.dialog.open()        
        else:            
            # c.execute("SELECT * FROM 'patientfeatures' where patientid =?", [nameofpatient])
            # usr_data = c.fetchall()
            patientfeatureresult = firebase.get('https://testingcloudstorage-db6b3-default-rtdb.firebaseio.com/Patientfeatures', "")
            usr_data = [];
            #for i in patientfeatureresult.keys():
            for i in range(len(patientfeatureresult.values())):
                patfeatres = list(patientfeatureresult.values())[i]
                print("second recordentry",nameofpatient, recordentry, patfeatres['recordentrydate'],recordentry== patfeatres['recordentrydate'])
                if (patfeatres['patientid'] == nameofpatient and patfeatres['recordentrydate'] == recordentry):
                    usr_data = list(patientfeatureresult.values())[i]
                    print("this difficult no",usr_data)
            
            if(len(usr_data) == 0):
                print("inside if(len(usr_data))")
                self.dialog = MDDialog(
                    title = 'Invalid Input !',
                    text = 'Please enter a valid user',
                    size_hint = (0.7,0.2),
                    buttons = [MDFlatButton(text='Retry',on_release = self.close)]
                    )
                self.dialog.open()
            else:
                # c.execute("SELECT * from 'patientfeatures' where patientid =?", [nameofpatient])
                Fever,Abdominal_Pain,Cough,Diarrheoa,Constipation,Rose_spots,Muscle_Weakness,Anorexia,Headache,Skin_Rash,Wieghtless,Stomach_distention,Malaise,Occult_blood_in_stool,Haemorrahages,Derilium,Abdominal_rigidity,Epistaxis= usr_data["Fever"],usr_data["Abdominal_Pain"],usr_data["Cough"],usr_data["Diarrheoa"],usr_data["Constipation"],usr_data["Rose_spots"],usr_data["Muscle_Weakness"],usr_data["Anorexia"],usr_data["Headache"],usr_data["Skin_Rash"],usr_data["Wieghtless"],usr_data["Stomach_distention"],usr_data["Malaise"],usr_data["Occult_blood_in_stool"],usr_data["Haemorrahages"],usr_data["Derilium"],usr_data["Abdominal_rigidity"],usr_data["Epistaxis"]
                print("I am Derilium", Derilium)
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
        print("this is typhoid_results", typhoid_results)
        if (typhoid_results != None):       
            self.ids.predict_patlab.text = ""
            self.ids.typhoidresult.opacity = 1
            self.ids.typhoidresult.text = "Patient" + " "+ (self.ids.patientname.text) +" has " + typhoid_results + " " + "typhoid"        
            self.ids.patientname.opacity = 0
            self.ids.recordentrydate.opacity = 0
        else:
            self.ids.predict_patlab.text = ""
            self.ids.typhoidresult.opacity = 1
            self.ids.typhoidresult.text = "Patient" + " "+ (self.ids.patientname.text) +" has " + "no" + " " + "typhoid"        
            self.ids.patientname.opacity = 0
            self.ids.recordentrydate.opacity = 0

    def generatePDF(self):        
        pdf = FPDF() 
        # Add a page
        pdf.add_page()    
        #add text        
        print("I am self.predictusingai", self.predictusingai())
        if (self.predictusingai() != None):
            reportxt = "The patient" +" "+ (self.ids.patientname.text) +" has " + self.predictusingai() +"typhoid"
        else:
            reportxt = "The patient" +" "+ (self.ids.patientname.text) +" has " + "no typhoid"     
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

    def on_save(self,instance,value,date_range):
        self.ids.recordentrydate.text = str(value)

    #when "Cancel" is clicked in the date picker
    def on_cancel(self,instance,value):
        return

    #function for date picker
    def show_date_picker(self):
        date_dialog = MDDatePicker()        
        date_dialog.bind(on_save = self.on_save,on_cancel=self.on_cancel)
        date_dialog.open()
