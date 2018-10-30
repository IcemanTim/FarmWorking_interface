import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import Animal
import Owner
import numpy as np
import random
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MakeTable(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.create_ui()
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def create_ui(self):
        treev = Treeview(self)

        treev['columns'] = ('Начало года', 'Конец года')
        treev.heading("#0", text='Животные')
        treev.column("#0", anchor='center', width=80)

        treev.heading('Начало года', text='Начало года')
        treev.column('Начало года', anchor='center', width=80)

        treev.heading('Конец года', text='Конец года')
        treev.column('Конец года', anchor='center', width=80)

        treev.grid(sticky=(N, S, W, E))
        self.treeview = treev
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def load_table(self, dic, year):
        if year == 0:
            self.treeview.insert('', 'end', text="Молодые",
                                 values=(int(dic.get('y_amount')), int(dic.get('y_Oldamount'))))
            self.treeview.insert('', 'end', text="Взрослые",
                                 values=(int(dic.get('a_amount')), int(dic.get('a_Oldamount'))))
            self.treeview.insert('', 'end', text="Старые",
                                 values=(int(dic.get('o_amount')), int(dic.get('o_Oldamount'))))
            self.treeview.insert('', 'end', text="", values=('', ''))
        else:
            self.treeview.insert('', 'end', text="Молодые",
                                 values=(int(dic.get('y_Oldamount')), int(dic.get('y_amount'))))
            self.treeview.insert('', 'end', text="Взрослые",
                                 values=(int(dic.get('a_Oldamount')), int(dic.get('a_amount'))))
            self.treeview.insert('', 'end', text="Старые",
                                 values=(int(dic.get('o_Oldamount')), int(dic.get('o_amount'))))
            self.treeview.insert('', 'end', text="", values=('', ''))

class Interface(tk.Frame):
    """docstring for Experiment"""
    diction = {}
    cur_year = 0
    active_widjets = {}
    used_btns = {}
    arr_capital = []

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.gui()

    def gui(self):
        self.master.title("Молочная ферма")
        self.pack(fill=BOTH, expand=True)
        self.center_window()

#---------- Зона активных действий с животными -----------------------
        panel_active = tk.Frame(self, bg='white')
        panel_active.place(x=10, y=10, width=680, height=400)
# рисование
        self.img = Image.open("farm.jpg")
        self.tatras = ImageTk.PhotoImage(self.img.resize((680, 350), Image.ANTIALIAS))

        canvas = Canvas(self, width=674, height=350)
        self.active_widjets['canvas'] = canvas
        canvas.place(x=10, y=10)

        canvas.create_image(0, 0, anchor=NW, image=self.tatras)

# обработчик кнопок
        def next_step_all():

            if self.cur_year > 0:
                self.used_btns['g_btn'].destroy()

            self.active_widjets['lll1'].destroy()
            self.active_widjets['lll2'].destroy()

            lll1 = tk.Label(text=str(int(self.diction.get('capital'))), fg='black',
                            font='arial 15')
            self.active_widjets['lll1'] = lll1
            lll1.place(x=200, y=590)

            lll2 = tk.Label(text=str(self.cur_year) + ' / ' +
                            str(int(self.diction.get('contract_time'))), fg='black',
                            font='arial 15')
            self.active_widjets['lll2'] = lll2
            lll2.place(x=320, y=630)

            table.load_table(self.diction, self.cur_year)

            if self.diction.get('flag') == True:

                self.img = Image.open("poor.jpg")
                self.tatras = ImageTk.PhotoImage(self.img.resize((680, 350), Image.ANTIALIAS))

                self.active_widjets['canvas'].destroy()
                canvas = Canvas(self, width=674, height=350)
                self.active_widjets['canvas'] = canvas
                canvas.place(x=10, y=10)

                canvas.create_image(0, 0, anchor=NW, image=self.tatras)

                otime = self.diction.get('contract_time')
                self.cur_year = 0
                self.diction = {}
                self.diction['flag'] = False
                self.arr_capital = []
                self.diction['otime'] = otime

                self.used_btns['g_btn'].destroy()

                r_btn = Button(self, text=u'Попробовать заново', command=ch_params)
                self.used_btns['r_btn'] = r_btn
                r_btn.place(x=380, y=670, width=300, height=30)

            elif self.cur_year == self.diction.get('contract_time'):

                self.used_btns['g_btn1'].destroy()
                self.used_btns['g_btn2'].destroy()

                res_btn = Button(self, text=u'Подведение итогов', command=show_res)
                self.used_btns['res_btn'] = res_btn
                res_btn.place(x=50, y=370, width=250, height=30)

            else:

                g_btn1 = Button(self, text=u'Изменить параметры', command=ch_params)
                self.used_btns['g_btn1'] = g_btn1
                g_btn1.place(x=30, y=370, width=180, height=30)

                g_btn2 = Button(self, text=u'Готово', command=show_params)
                self.used_btns['g_btn2'] = g_btn2
                g_btn2.place(x=300, y=370, width=150, height=30)

# изменение параметров
        def ch_params():

            def show_scale(name_wid, wid, arr):
                self.active_widjets.get(name_wid).destroy()
                wid = tk.Scale(self, length=100, orient=HORIZONTAL, from_=arr[0],
                               to=arr[1], resolution=arr[2])
                self.active_widjets[name_wid] = wid
                wid.place(x=arr[3], y=arr[4])

            show_scale('scale_feedcost', scale_feedcost, [1000, 5000, 100, 880, 110])
            show_scale('scale_allfood', scale_allfood, [50000, 150000, 5000, 1000, 150])
            show_scale('scale_y_sell', scale_y_sell, [10, 50, 5, 870, 230])
            show_scale('scale_y_cost', scale_y_cost, [1000, 3000, 100, 1000, 230])
            show_scale('scale_a_sell', scale_a_sell, [10, 50, 5, 870, 270])
            show_scale('scale_a_cost', scale_a_cost, [3000, 6000, 100, 1000, 270])
            show_scale('scale_o_sell', scale_o_sell, [10, 50, 5, 870, 310])
            show_scale('scale_o_cost', scale_o_cost, [1000, 2000, 100, 1000, 310])
            show_scale('scale_penalty', scale_penalty, [5000, 9000, 500, 880, 350])

            if self.cur_year == 0:

                show_scale('scale_contract', scale_contract, [3, 5, 1, 880, 70])
                show_scale('scale_capital', scale_capital, [50000, 100000, 5000, 880, 490])
                show_scale('scale_y_amount', scale_y_amount, [30, 60, 5, 980, 550])
                show_scale('scale_a_amount', scale_a_amount, [50, 100, 5, 980, 590])
                show_scale('scale_o_amount', scale_o_amount, [20, 70, 5, 980, 630])

                self.used_btns['r_btn'].destroy()

                if self.diction.get('flag') != True:
                    self.used_btns['res_btn'].destroy()

                self.diction['flag'] = False

                self.active_widjets['lll1'].destroy()
                self.active_widjets['lll2'].destroy()

                self.img = Image.open("farm.jpg")
                self.tatras = ImageTk.PhotoImage(self.img.resize((680, 350), Image.ANTIALIAS))

                self.active_widjets['canvas'].destroy()
                canvas = Canvas(self, width=674, height=350)
                self.active_widjets['canvas'] = canvas
                canvas.place(x=10, y=10)

                canvas.create_image(0, 0, anchor=NW, image=self.tatras)

                s_btn = Button(self, text=u'Начать эксперимент', command=show_params)
                self.used_btns['s_btn'] = s_btn
                s_btn.place(x=430, y=670, width=250, height=30)

        def show_res():

            pointsx = []
            i = 0
            while i <= self.cur_year:
                pointsx.append(i)
                i += 1
            osx = np.array(pointsx)
            osy = np.array(self.arr_capital)

            fig = Figure(figsize=(6.74, 3.5), dpi=100)
            atrr = fig.add_subplot(111)
            atrr.plot(osx, osy)

            self.active_widjets['canvas'].destroy()
            canvas = FigureCanvasTkAgg(fig, self)
            canvas.show()

            canvas._tkcanvas.place(x=10, y=10)

            otime = self.diction.get('contract_time')
            self.cur_year = 0
            self.diction = {}
            self.diction['flag'] = False
            self.arr_capital = []
            self.diction['otime'] = otime

            self.used_btns['res_btn'].destroy()

            r_btn = Button(self, text=u'Попробовать заново', command=ch_params)
            self.used_btns['r_btn'] = r_btn
            r_btn.place(x=380, y=670, width=300, height=30)
# кнопка завершения
        def end_action(event):
            exit()

        q_btn = Button(self, text=u'Завершить')
        q_btn.place(x=550, y=370, width=120, height=30)
        q_btn.bind("<Button-1>", end_action)

#---------- Зона внесения изменения в параметры ----------------------
        panel_ch_param = tk.Frame(self, bg='white')
        panel_ch_param.place(x=700, y=10, width=490, height=400)

        lab0 = tk.Label(text='Контракт', width=20, bg='lightgray', fg='black', font='arial 25')
        lab0.place(x=800, y=30)

        lab1 = tk.Label(text='Срок контракта :', fg='black', font='arial 15')
        lab1.place(x=750, y=90)
        scale_contract = tk.Scale(self, length=100, orient=HORIZONTAL, from_=3, to=5,
                                  resolution=1)
        self.active_widjets['scale_contract'] = scale_contract
        scale_contract.place(x=880, y=70)

        lab2 = tk.Label(text='Цена корма :', fg='black', font='arial 15')
        lab2.place(x=750, y=130)
        scale_feedcost = tk.Scale(self, length=100, orient=HORIZONTAL, from_=1000, to=5000,
                                  resolution=100)
        self.active_widjets['scale_feedcost'] = scale_feedcost
        scale_feedcost.place(x=880, y=110)

        lab3 = tk.Label(text='Сумма закупаемого корма :', fg='black', font='arial 15')
        lab3.place(x=750, y=170)
        scale_allfood = tk.Scale(self, length=100, orient=HORIZONTAL, from_=50000, to=150000,
                                 resolution=10000)
        self.active_widjets['scale_allfood'] = scale_allfood
        scale_allfood.place(x=1000, y=150)

        lab4 = tk.Label(text='Необходимо продать голов по цене за голову :', fg='black',
                        font='arial 15')
        lab4.place(x=750, y=205)

        lab5 = tk.Label(text='- молодых', fg='black', font='arial 15')
        lab5.place(x=780, y=250)
        scale_y_sell = tk.Scale(self, length=100, orient=HORIZONTAL, from_=10, to=50,
                                resolution=5)
        self.active_widjets['scale_y_sell'] = scale_y_sell
        scale_y_sell.place(x=870, y=230)
        scale_y_cost = tk.Scale(self, length=100, orient=HORIZONTAL, from_=1000, to=3000,
                                resolution=100)
        self.active_widjets['scale_y_cost'] = scale_y_cost
        scale_y_cost.place(x=1000, y=230)

        lab6 = tk.Label(text='- взрослых', fg='black', font='arial 15')
        lab6.place(x=780, y=290)
        scale_a_sell = tk.Scale(self, length=100, orient=HORIZONTAL, from_=10, to=50,
                                resolution=5)
        self.active_widjets['scale_a_sell'] = scale_a_sell
        scale_a_sell.place(x=870, y=270)
        scale_a_cost = tk.Scale(self, length=100, orient=HORIZONTAL, from_=3000, to=6000,
                                resolution=100)
        self.active_widjets['scale_a_cost'] = scale_a_cost
        scale_a_cost.place(x=1000, y=270)

        lab7 = tk.Label(text='- старых', fg='black', font='arial 15')
        lab7.place(x=780, y=330)
        scale_o_sell = tk.Scale(self, length=100, orient=HORIZONTAL, from_=10, to=50,
                                resolution=5)
        self.active_widjets['scale_o_sell'] = scale_o_sell
        scale_o_sell.place(x=870, y=310)
        scale_o_cost = tk.Scale(self, length=100, orient=HORIZONTAL, from_=1000, to=2000,
                                resolution=100)
        self.active_widjets['scale_o_cost'] = scale_o_cost
        scale_o_cost.place(x=1000, y=310)

        lab8 = tk.Label(text='Неустойка :', fg='black', font='arial 15')
        lab8.place(x=750, y=370)
        scale_penalty = tk.Scale(self, length=100, orient=HORIZONTAL, from_=5000, to=9000,
                                 resolution=500)
        self.active_widjets['scale_penalty'] = scale_penalty
        scale_penalty.place(x=880, y=350)

#---------- Зона статистических данных -------------------------------
        panel_statistics = tk.Frame(self, bg='white')
        panel_statistics.place(x=10, y=420, width=680, height=290)

        table = MakeTable(self)
        table.place(x=10, y=420, width=680, height=156)

        llab1 = tk.Label(text=' Текущий капитал :', fg='black', font='arial 15')
        llab1.place(x=30, y=590)

        llab2 = tk.Label(text=' Прошло лет / Общий срок контракта :', fg='black', font='arial 15')
        llab2.place(x=30, y=630)

        def show_params():

            def put_in_right_place(name, widget, pointx, pointy, wid_name):
                if '.!interface.!scale' in str(widget):
                    self.diction[name] = int(widget.get())
                    wid = tk.Label(text=str(widget.get()), fg='black', font='arial 15')
                    widget.destroy()
                    self.active_widjets[wid_name] = wid
                    wid.place(x=pointx, y=pointy)
                else:
                    pass

            put_in_right_place('feed_cost', self.active_widjets['scale_feedcost'], 880,
                               130, 'scale_feedcost')
            put_in_right_place('all_food', self.active_widjets['scale_allfood'], 1000,
                               170, 'scale_allfood')
            put_in_right_place('young_sell', self.active_widjets['scale_y_sell'], 880,
                               250, 'scale_y_sell')
            put_in_right_place('young_cost', self.active_widjets['scale_y_cost'], 1000,
                               250, 'scale_y_cost')
            put_in_right_place('adult_sell', self.active_widjets['scale_a_sell'], 880,
                               290, 'scale_a_sell')
            put_in_right_place('adult_cost', self.active_widjets['scale_a_cost'], 1000, 290,
                               'scale_a_cost')
            put_in_right_place('old_sell', self.active_widjets['scale_o_sell'], 880,
                               330, 'scale_o_sell')
            put_in_right_place('old_cost', self.active_widjets['scale_o_cost'], 1000,
                               330, 'scale_o_cost')
            put_in_right_place('penalty', self.active_widjets['scale_penalty'], 880,
                               370, 'scale_penalty')

            if self.cur_year == 0:

                put_in_right_place('contract_time', self.active_widjets['scale_contract'],
                                   880, 90, 'scale_contract')
                put_in_right_place('capital', self.active_widjets['scale_capital'],
                                   880, 510, 'scale_capital')
                put_in_right_place('y_amount', self.active_widjets['scale_y_amount'],
                                   980, 570, 'scale_y_amount')
                put_in_right_place('a_amount', self.active_widjets['scale_a_amount'],
                                   980, 610, 'scale_a_amount')
                put_in_right_place('o_amount', self.active_widjets['scale_o_amount'],
                                   980, 650, 'scale_o_amount')

                how_many = random.randint(1, self.diction.get('contract_time'))
                i = 0
                ran_years = []
                ran_amounts = []
                while i < how_many:
                    num = random.randint(1, self.diction.get('contract_time')-1)
                    if num in ran_years:
                        pass
                    else:
                        ran_years.append(num)
                        ran_amounts.append(random.randint(5, 20))
                    i += 1

                self.diction['ran_years'] = ran_years
                self.diction['ran_amounts'] = ran_amounts

                self.diction['need_food'] = 0

                lll1 = tk.Label(text=str(int(self.diction.get('capital'))),
                                fg='black', font='arial 15')
                self.active_widjets['lll1'] = lll1
                lll1.place(x=200, y=590)

                self.arr_capital.append(int(self.diction.get('capital')))

                lll2 = tk.Label(text=str(self.cur_year) + ' / ' +
                                str(int(self.diction.get('contract_time'))), fg='black',
                                font='arial 15')
                self.active_widjets['lll2'] = lll2
                lll2.place(x=320, y=630)

            animal = Animal.Animal(self.diction, self.cur_year)
            animal_amount = animal.count_newamount_animal()
            if self.diction.get('all_food') < animal.count_need_food():
                arr = np.array(animal_amount)
                animal_amount = arr * 0.8  

            self.diction['y_Oldamount'] = self.diction.get('y_amount')
            self.diction['a_Oldamount'] = self.diction.get('a_amount')
            self.diction['o_Oldamount'] = self.diction.get('o_amount')

            self.diction['y_amount'] = animal_amount[0]
            self.diction['a_amount'] = animal_amount[1]
            self.diction['o_amount'] = animal_amount[2]

            owner = Owner.Owner(self.diction, self.cur_year)
            self.diction['capital'] = owner.sell()
            self.diction['flag'] = owner.paying_capacity()

            self.arr_capital.append(int(self.diction.get('capital')))

            if self.cur_year > 0 and self.cur_year <= self.diction.get('contract_time'):
                self.used_btns['g_btn1'].destroy()
                self.used_btns['g_btn2'].destroy()

            if self.cur_year < self.diction.get('contract_time'):

                self.cur_year = self.cur_year + 1

                if self.cur_year == 1:
                    self.used_btns['s_btn'].destroy()

                if self.cur_year <= self.diction.get('contract_time'):

                    g_btn = Button(self, text=u'Следующий шаг', command=next_step_all)
                    self.used_btns['g_btn'] = g_btn
                    g_btn.place(x=30, y=370, width=150, height=30)


        s_btn = Button(self, text=u'Начать эксперимент', command=show_params)
        self.used_btns['s_btn'] = s_btn
        s_btn.place(x=430, y=670, width=250, height=30)

#---------- Зона изменения начальных параметров ----------------------
        panel_param = tk.Frame(self, bg='white')
        panel_param.place(x=700, y=420, width=490, height=290)

        l11 = tk.Label(text='Начальные данные', width=20, bg='lightgray',
                       fg='black', font='arial 25')
        l11.place(x=800, y=440)

        l22 = tk.Label(text='Капитал :', fg='black', font='arial 15')
        l22.place(x=750, y=510)
        scale_capital = tk.Scale(self, length=100, orient=HORIZONTAL, from_=50000,
                                 to=100000, resolution=5000)
        self.active_widjets['scale_capital'] = scale_capital
        scale_capital.place(x=880, y=490)

        l33 = tk.Label(text='Количество голов  :', fg='black', font='arial 15')
        l33.place(x=750, y=550)

        l44 = tk.Label(text='- молодых  ', fg='black', font='arial 15')
        l44.place(x=870, y=570)
        scale_y_amount = tk.Scale(self, length=100, orient=HORIZONTAL, from_=30,
                                  to=60, resolution=5)
        self.active_widjets['scale_y_amount'] = scale_y_amount
        scale_y_amount.place(x=980, y=550)

        l55 = tk.Label(text='- взрослых  ', fg='black', font='arial 15')
        l55.place(x=870, y=610)
        scale_a_amount = tk.Scale(self, length=100, orient=HORIZONTAL, from_=50,
                                  to=100, resolution=5)
        self.active_widjets['scale_a_amount'] = scale_a_amount
        scale_a_amount.place(x=980, y=590)

        l66 = tk.Label(text='- старых  ', fg='black', font='arial 15')
        l66.place(x=870, y=650)
        scale_o_amount = tk.Scale(self, length=100, orient=HORIZONTAL, from_=20,
                                  to=70, resolution=5)
        self.active_widjets['scale_o_amount'] = scale_o_amount
        scale_o_amount.place(x=980, y=630)

    def center_window(self):
        width = 1200
        height = 720
        screen_w = self.master.winfo_screenwidth()
        screen_h = self.master.winfo_screenheight()
        osx = (screen_w - width)/2
        osy = (screen_h - height)/2
        self.master.geometry('%dx%d+%d+%d' % (width, height, osx, osy))

def main():
    root = Tk()
    Interface(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == '__main__':
    main()
