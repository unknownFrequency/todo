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
from kivy.uix.gridlayout import GridLayout
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
    if input('Have you checked that you protected the important stuff? [yN]').lower().strip() == 'y':
        now = datetime.datetime.now()
        for entry in entries:
            if now - entry.timestamp > datetime.timedelta(7, 0, 0) and entry.done and not entry.protected:
                entry.delete_instance()


def modify_task(entry):
    """Modify task"""
    new_task = input('> ')
    entry.task = new_task
    entry.save()


def delete_entry(entry):
    """Erase entry"""
    if input('Are you sure [yN]? ').lower().strip() == 'y':
        entry.delete_instance()


def toggle_done(entry):
    """Toggle 'DONE'"""
    entry.done = not entry.done
    entry.save()


def toggle_protection(entry):
    """Toggle 'protected'"""
    entry.protected = not entry.protected
    entry.save()




class SaveButton(Button):
    pass


class CalendarButton(Button):
    pass


class MainPage(GridLayout):
    # todo_text_input = ObjectProperty()
    # todo_deadline_input = ObjectProperty()

    def get_todos(self):
        cur = db.cursor()
        cur.execute("SELECT * FROM todo WHERE done=0")
        todos = [row for row in cur.fetchall()]
        print(todos)

    def save_task(self):
        initialize()
        task = str(self.todo_text_input.text)
        protected = bool(self.todo_protected_input.text)
        deadline_formatted = str(self.deadline.day) + '-' + str(self.deadline.month) + '-' + str(self.deadline.year)
        deadline = datetime.strptime(deadline_formatted, '%d-%m-%Y')

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



