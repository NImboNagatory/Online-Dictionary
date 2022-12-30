from requests import get
from data.data import url_morf, Token
from tkinter import Frame, Entry, Button, RAISED, CENTER, Label, scrolledtext, INSERT, WORD
from urllib.request import urlretrieve
from PIL import Image, ImageTk


class DefinitionScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="Online Dictionary", font=('Times', 20, 'bold'))
        self.entry = Entry(self, width=25, relief=RAISED, justify=CENTER, font=('Times', 20, 'bold'))
        self.button = Button(self, text="Search", width=20, relief=RAISED, command=self.search)

        self.img_hanger = None
        self.definition_hanger = None
        self.next_button = None

        self.label.grid(row=0, padx=(30, 0))
        self.entry.grid(row=1, pady=(40, 30), padx=(25, 0))
        self.button.grid(row=2, padx=(30, 0))
        self.response = None
        self.status_code = None
        self.pronunciation = None
        self.type = None
        self.definition = None
        self.example = None
        self.image_url = None
        self.emoji = None
        self.page = 0

    def search(self):
        self.page = 0
        self.clear_screen()
        self.response = get(url_morf(self.entry.get()), headers={"Authorization": Token})
        self.parse_json(self.response.json(), self.response.status_code)
        self.insert_img()
        self.insert_definition()
        self.next_button_insert()

    def next_button_insert(self):
        if self.next_button is None and self.response.status_code == 200:
            if len((self.response.json())['definitions']) > 1:
                self.next_button = Button(self, text="Next Page", width=15, relief=RAISED, command=self.next_page)
                self.next_button.grid(row=3, padx=(2, 250), pady=(2, 250))

    def next_page(self):
        if self.page+1 == len((self.response.json())['definitions']):
            self.page = 0
            self.clear_screen()
            self.parse_json(self.response.json(), self.response.status_code)
            self.insert_img()
            self.insert_definition()
            self.next_button_insert()
        else:
            self.page += 1
            self.clear_screen()
            self.parse_json(self.response.json(), self.response.status_code)
            self.insert_img()
            self.insert_definition()
            self.next_button_insert()

    def clear_screen(self):
        if self.img_hanger is not None:
            self.image_url = None
            self.img_hanger.grid_forget()
        if self.definition_hanger is not None:
            self.definition = None
            self.definition_hanger.grid_forget()
        if self.next_button is not None:
            self.next_button.grid_forget()
            self.next_button = None

    def parse_json(self, json, status_code):
        if status_code == 404:
            self.clear_screen()
            self.status_code = Label(self, text="No definition :(", font=('Times', 15))
            self.status_code.grid(row=3, pady=(20, 0), padx=(25, 0))
        elif status_code == 429:
            self.clear_screen()
            self.status_code = Label(self, text="Server is Down. Try Later :(", font=('Times', 15))
            self.status_code.grid(row=3, pady=(20, 0), padx=(25, 0))
        elif status_code == 200:
            if self.status_code is not None:
                self.status_code.grid_forget()
                self.status_code = None
            if json['definitions'][self.page]["image_url"] != "":
                self.image_url = json['definitions'][self.page]["image_url"]
            if json['definitions'][self.page]["type"] != "":
                self.type = json['definitions'][self.page]["type"]
            if json['definitions'][self.page]["definition"] != "":
                self.definition = json['definitions'][self.page]["definition"]
            if json['definitions'][self.page]["emoji"] != "":
                self.emoji = json['definitions'][self.page]["emoji"]
            if json['definitions'][self.page]['example'] != "":
                self.example = json['definitions'][self.page]['example']

    def insert_img(self):
        if self.image_url is not None:
            urlretrieve(
                self.image_url,
                "data/img.png")
            img = Image.open("data/img.png")
            img = img.resize((80, 80), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.img_hanger = Label(self, image=img)
            self.img_hanger.image = img
            self.img_hanger.grid(row=3, pady=(10, 0), padx=(20, 250), sticky="nw")

    def insert_definition(self):
        if self.definition is not None and self.example is not None and self.type is not None and self.emoji is not None:
            self.definition_hanger = scrolledtext.ScrolledText(self, width=30, font=('Times', 12), wrap=WORD)
            self.definition_hanger.insert(INSERT,
                                          f"Type:\n{self.type}\n\nEmoji:\n{self.emoji}\n\nDefinition:\n{self.definition}\n\nExample:\n{self.example}")
            self.definition_hanger.grid(row=3, pady=(10, 0), padx=(135, 2))
        elif self.definition is not None and self.example is not None and self.type is not None:
            self.definition_hanger = scrolledtext.ScrolledText(self, width=30, font=('Times', 12), wrap=WORD)
            self.definition_hanger.insert(INSERT,
                                          f"Type:\n{self.type}\n\nDefinition:\n{self.definition}\n\nExample:\n{self.example}")
            self.definition_hanger.grid(row=3, pady=(10, 0), padx=(135, 2))
        elif self.definition is not None and self.example is not None:
            self.definition_hanger = scrolledtext.ScrolledText(self, width=30, font=('Times', 12), wrap=WORD)
            self.definition_hanger.insert(INSERT, f"\nDefinition:\n\n{self.definition}\n\nExample:\n\n{self.example}")
            self.definition_hanger.grid(row=3, pady=(10, 0), padx=(135, 2))
        elif self.definition is not None:
            self.definition_hanger = scrolledtext.ScrolledText(self, width=30, font=('Times', 12), wrap=WORD)
            self.definition_hanger.insert(INSERT, f"\nDefinition:\n\n{self.definition}")
            self.definition_hanger.grid(row=3, pady=(10, 0), padx=(135, 2))
