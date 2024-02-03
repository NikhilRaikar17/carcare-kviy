import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from datetime import datetime
import pyrebase
from kivy.clock import Clock

# Firebase imports and setup here
# import pyrebase or any other firebase library
# configure your firebase project details

kivy.require('2.0.0')  # replace with your current kivy version

firebaseConfig = {
"apiKey": "AIzaSyDu-W8ET-1eCppfmaYq0YZMqR5hfzs9tsU",
"authDomain": "r1carcare.firebaseapp.com",
            "databaseURL": "https://r1carcare-default-rtdb.firebaseio.com/",
"projectId": "r1carcare",
"storageBucket": "r1carcare.appspot.com",
"messagingSenderId": "781639349911",
"appId": "1:781639349911:web:56d9904353a8abddd4dbd2",
"measurementId": "G-SRFE2K96P9"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class CarWashApp(App):

    def __init__(self, **kwargs):
        super(CarWashApp, self).__init__(**kwargs)
        self.last_submission_date = datetime.now().date()
        self.today_count = 0

    def build(self):
        self.title = 'R1 Car Care'
        Window.clearcolor = (1, 1, 1, 1)  # Soft green color

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.pos_hint = {"center_x": 0.5, "center_y":0.5}
       
        title_label = Label(text=self.title, color=(0, 0, 0, 1), font_size='30')  # Black color
        layout.add_widget(title_label)

        # Logo
        logo = Image(source='logo.png', size_hint= (1, 2))  # Replace with your logo path
        layout.add_widget(logo)

        # Date and Time
        date_time = Label(text='Date-Time=' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),color=(0, 0, 0, 1))
        layout.add_widget(date_time)

        # Customer Name
        self.customer_name = TextInput(hint_text='Customer Name', multiline=False)
        layout.add_widget(self.customer_name)

        # Vehicle Number
        self.vehicle_number = TextInput(hint_text='Vehicle Number', multiline=False)
        layout.add_widget(self.vehicle_number)

        # Phone Number
        self.phone_number = TextInput(hint_text='Phone Number', multiline=False)
        layout.add_widget(self.phone_number)

        # Amount Paid
        self.amount_paid = TextInput(hint_text='Amount Paid', multiline=False)
        layout.add_widget(self.amount_paid)

        self.todays_count_label = Label(text=f"Today's Vehicle Count: {self.today_count}", color=(0, 0, 0, 1))
        layout.add_widget(self.todays_count_label)

        # Submit Button
        submit_button = Button(text='Submit')
        submit_button.bind(on_press=self.submit_details)
        layout.add_widget(submit_button)

        self.success_label = Label(text='')  # Green color for success
        layout.add_widget(self.success_label)

        return layout

    def submit_details(self, instance):

        current_date = datetime.now().date()
        if current_date != self.last_submission_date:
            self.today_count = 0
            self.last_submission_date = current_date

        try:
            data = {
                "name": self.customer_name.text,
                "vehicle_number": self.vehicle_number.text,
                "phone_number": self.phone_number.text,
                "amount": self.amount_paid.text,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            db.child("vehicles").push(data)
            self.success_label.color = [0, 1, 0, 1]
            self.success_label.text = "Vehicle recorded successfully"

            self.today_count += 1
            self.todays_count_label.text = f"Today's Count: {self.today_count}"

            Clock.schedule_once(self.reset_form, 1)
        except Exception as e:

            self.success_label.color = [1, 0, 0, 1]
            self.success_label.text = f"ERROR!! Please contact Admin"

    def reset_form(self, dt):
        self.customer_name.text = ''
        self.vehicle_number.text = ''
        self.phone_number.text = ''
        self.amount_paid.text = ''
        self.success_label.text = ''


if __name__ == '__main__':
    CarWashApp().run()
