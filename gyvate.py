from tkinter import *
from random import randint
from PIL import Image, ImageTk


judėjimas = 20
RPM = 7
greitis = 1200 // RPM
bloko_dydis = 700


class Gyvatė(Canvas):
    def __init__(self):
        super().__init__(width=bloko_dydis, height=bloko_dydis, background='#53ff1a', highlightthickness=0)

        self.gyvates_pos = [(100, 80), (80, 100), (80, 100)]
        self.maisto_pos = self.nauja_maisto_pos()
        self.kryptis = 'Right'

        self.taškai = 0

        self.užkrauti_nuotrauka()
        self.sukurti_nuotrauka()

        self.bind_all('<Key>', self.on_key_press)

        self.pack()

        self.after(greitis, self.veiksmo_atlikimas)

    def užkrauti_nuotrauka(self):
        try:
            self.gyvatės_kunas = ImageTk.PhotoImage(Image.open('gyvate.png'))
            self.maistas = ImageTk.PhotoImage(Image.open('maistas.png'))
        except IOError as error:
            return langas.destroy()

    def sukurti_nuotrauka(self):
        self.create_text(35, 12, text=f'Taškai: {self.taškai}', tag='Taškai', fill='black', font=10)

        for x_pozicija, y_pozicija in self.gyvates_pos:
            self.create_image(x_pozicija, y_pozicija, image=self.gyvatės_kunas, tag='gyvate')

        self.create_image(*self.maisto_pos, image=self.maistas, tag='maistas')
        self.create_rectangle(7, 27, 690, 690, outline='#d9d8d7')

    def finish_game(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2,self.winfo_height() / 2,text=f'Žaidimas baigtas! Surinkti taškai  {self.taškai}!',fill='black',font=20)

    def valgyti_maista(self):
        if self.gyvates_pos[0] == self.maisto_pos:
            self.taškai += 10
            self.gyvates_pos.append(self.gyvates_pos[-1])

            self.create_image(*self.gyvates_pos[-1], image=self.gyvatės_kunas, tag='gyvate')
            self.maisto_pos = self.nauja_maisto_pos()
            self.coords(self.find_withtag('maistas'), *self.maisto_pos)

            taškai = self.find_withtag('Taškai')
            self.itemconfigure(taškai, text=f'Taškai: {self.taškai}', tag= 'Taškai')
    
    def siena(self):
        x_gyvatės_galvos_pozicija, y_gyvatės_galvos_pozicija = self.gyvates_pos[0]

        return (x_gyvatės_galvos_pozicija in (0, 700) or y_gyvatės_galvos_pozicija in (20, 700) or (x_gyvatės_galvos_pozicija, y_gyvatės_galvos_pozicija) in self.gyvates_pos[1:])

    def gyvates_judėjimas(self):
        x_gyvatės_galvos_pozicija, y_gyvatės_galvos_pozicija = self.gyvates_pos[0]

        if self.kryptis == 'Left':
            nauja_gyvatės_galvos_pozicija = (x_gyvatės_galvos_pozicija - judėjimas, y_gyvatės_galvos_pozicija)
        elif self.kryptis == 'Right':
            nauja_gyvatės_galvos_pozicija = (x_gyvatės_galvos_pozicija + judėjimas, y_gyvatės_galvos_pozicija)
        elif self.kryptis == 'Down':
            nauja_gyvatės_galvos_pozicija = (x_gyvatės_galvos_pozicija, y_gyvatės_galvos_pozicija + judėjimas)
        elif self.kryptis == 'Up':
            nauja_gyvatės_galvos_pozicija = (x_gyvatės_galvos_pozicija, y_gyvatės_galvos_pozicija - judėjimas)

        self.gyvates_pos = [nauja_gyvatės_galvos_pozicija] + self.gyvates_pos[:-1]

        for dalis, pozicija in zip(self.find_withtag('gyvate'), self.gyvates_pos):
            self.coords(dalis, pozicija)

    def on_key_press(self, e):
        nauja_kryptis = e.keysym

        visos_kryptis = (
            'Up', 
            'Down', 
            'Left', 
            'Right'
            )
        sutapimas = (
            {'Up', 'Down'}, 
            {'Left', 'Right'}
            )

        if (nauja_kryptis in visos_kryptis and {nauja_kryptis, self.kryptis} not in sutapimas):
            self.kryptis = nauja_kryptis

    def veiksmo_atlikimas(self):
        if self.siena():
            self.finish_game()

        self.valgyti_maista()
        self.gyvates_judėjimas()

        self.after(greitis, self.veiksmo_atlikimas)

    def nauja_maisto_pos(self):
        while True:
            x_pozicija = randint(1, 29) * judėjimas
            y_pozicija = randint(3, 30) * judėjimas
            maisto_pos = (x_pozicija, y_pozicija)

            if maisto_pos not in self.gyvates_pos:
                return maisto_pos


langas = Tk()
langas.title('Gyvatels žaidimas')
langas.resizable(False, False)

board = Gyvatė()

langas.mainloop()