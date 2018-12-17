"""To-do list where you can chronologically add your tasks, modify them and mark if they have been completed.
  A cleanup feature enables you to delete completed tasks which are more than a week old - unless
  you have flagged them as 'protected'."""
from datetime import datetime
import time
import logging
import os
from os import listdir 
from collections import OrderedDict
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivymd.date_picker import MDDatePicker
from kivymd.theming import ThemeManager
from kivymd.button import MDFloatingActionButton, MDFlatButton
from peewee import *

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
    timestamp = DateTimeField(default=datetime.now())

    class Meta:
        database = db


def initialize():
    """Connect to database, build tables if they don't exist"""
    db.connect()
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


class MainPage(BoxLayout):
    # todo_text_input = ObjectProperty()
    # todo_deadline_input = ObjectProperty()

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

    def priority_switch(self, instance, value):
        if value is True:
            print("Priority on!")
        else:
            print("Priority off!")

    def save_task(self):
        #initialize()
        task = str(self.todo_text_input.text)
        protected = bool(self.todo_protected_input.text)
        deadline_formatted = str(self.deadline.year) + '-' + str(self.deadline.month) + '-' + str(self.deadline.day)
        deadline = datetime.strptime(deadline_formatted, '%Y-%m-%d')

        try:
            ToDo.create(task=task,
                        protected=protected,
                        done=False,
                        deadline=deadline,
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
            logging.debug(self.deadline)
        except AttributeError:
            pass
        else:
            pass


class TodoApp(App):
    theme_cls = ThemeManager()

    def build(self):
        self.title = "Todo or not todo - That is the question"
        return MainPage()


todoApp = TodoApp()
todoApp.run()
#if __name__ == '__main__':



