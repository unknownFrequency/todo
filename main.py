"""To-do list where you can chronologically add your tasks, modify them and mark if they have been completed.
  A cleanup feature enables you to delete completed tasks which are more than a week old - unless
  you have flagged them as 'protected'."""
from datetime import datetime
import time
from os import listdir
import logging
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivymd.theming import ThemeManager
from kivymd.date_picker import MDDatePicker
from kivymd.time_picker import MDTimePicker
from peewee import *
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker


db = SqliteDatabase('to_do_list.db')
cur = db.cursor()

kv_path = './kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

class ToDo(Model):
    task = CharField(max_length=255)
    done = BooleanField(default=False)
    protected = BooleanField(default=False)
    deadline = DateTimeField(default=datetime.now())
    time_deadline = DateTimeField(default=datetime.now())
    timestamp = DateTimeField(default=datetime.now())

    class Meta:
        database = db


def initialize():
    """Connect to database, build tables if they don't exist"""
    db.create_tables([ToDo], safe=True)


def cleanup_entries(index, entries):
    """Cleanup: delete completed, non-protected entries older than a week"""
    now = datetime.datetime.now()
    for entry in entries:
        if now - entry.timestamp > datetime.timedelta(7, 0, 0) and entry.done and not entry.protected:
            entry.delete_instance()


class SaveButton(Button):
    pass


class CalendarButton(Button):
    pass


class ProtectedButton(Button):
    pass


class TimeButton(Button):
    pass


class MainPageLayout(BoxLayout):
    todo_text_input = ObjectProperty()
    todo_deadline_input = ObjectProperty()
    todo_protected_input = ObjectProperty()
    previous_date = ObjectProperty()
    protected = False
    protected_button_text = "Not Protected"
    protected_button_background_color = (1, 0, 0, .5)
    previous_time = False
    time_deadline = datetime.now()
    time_text = "TIDEN"
    print(time_deadline.time)

    def get_todos(self):
        cur.execute("SELECT * FROM todo WHERE done=0")
        todos = [row for row in cur.fetchall()]
        print(todos)

    def get_protected_tasks(self):
        cur.execute("SELECT * FROM todo WHERE protected=1")
        todos = [row for row in cur.fetchall()]
        print(todos)

    def get_todays_tasks(self):
        pass

    def get_future_tasks(self, start_date, end_date):
        # YYYY-MM-DD format!
        cur.execute("SELECT * FROM todo WHERE timestamp BETWEEN ? AND ?", (start_date, end_date))

    def get_done_tasks(self):
        pass

    def get_tasks_between_dates(self):
        pass

    def toggle_protected(self):
        if self.protected_button_text == "Not Protected":
            self.protected_button_text = "Protected"
            self.protected = True
        else:
            self.protected_button_text = "Not Protected"
            self.protected = False

        return self.protected_button_text

    def toggle_protected_button_background_color(self):
        # TODO: Refactor to be dynamic
        if self.protected_button_background_color == (1, 0, 0, .5):
            self.protected_button_background_color = (0, 1, 0, .5)
        else:
            self.protected_button_background_color = (1, 0, 0, .5)
        return self.protected_button_background_color

    def priority_switch(self, instance, value):
        if value is True:
            print("Priority on!")
        else:
            print("Priority off!")

    def save_task(self):
        task = str(self.todo_text_input.text)
        protected = bool(self.protected)
        deadline_formatted = str(self.deadline.year) + '-' + str(self.deadline.month) + '-' + str(self.deadline.day)
        deadline = datetime.strptime(deadline_formatted, '%Y-%m-%d')

        try:
            ToDo.create(task=task,
                        protected=protected,
                        done=False,
                        deadline=deadline,
                        time_deadline=self.time_deadline,
                        timestamp=datetime.now())
        except Exception as e:
            print(e)
            self.todo_text_input.text = str(e)

    def update_task(self):
        pass

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj

    def show_date_picker(self):
        try:
            self.deadline = MDDatePicker(self.set_previous_date)
            self.deadline.open()
        except AttributeError:
            pass
        else:
            pass

    def get_time_picker_data(self, instance, time_selected):
        self.time_text = str(time_selected)
        self.previous_time = time_selected
        self.time_deadline = time_selected

    def show_time_picker(self):
        self.time_deadline = MDTimePicker()
        self.time_deadline.bind(time=self.get_time_picker_data)
        if self.previous_time:
            try:
                self.time_deadline.set_time(self.previous_time)
            except AttributeError:
                pass
        self.time_deadline.open()


class TodoApp(App):
    theme_cls = ThemeManager()
    initialize()

    def build(self):
        self.title = "Todo or not todo - That is the question"
        return MainPageLayout()


todoApp = TodoApp()
todoApp.run()
#if __name__ == '__main__':



