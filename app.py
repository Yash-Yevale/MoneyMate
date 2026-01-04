from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.window import Window
from kivy.properties import ObjectProperty

import sqlite3

from datetime import timedelta, datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import yagmail

import os
from win10toast import ToastNotifier

from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse

from pprint import pprint

from screen import screen_helper


class HOScreen(MDScreen):
    pass

class UPScreen(MDScreen):
    pass

class ENScreen(MDScreen):
    pass

class SOScreen(MDScreen):
    pass

class SOCScreen(MDScreen):
    pass

class REScreen(MDScreen):
    pass

class ACScreen(MDScreen):
    pass

class CBScreen(MDScreen):
    pass

class STScreen(MDScreen):
    pass

class RMScreen(MDScreen):
    pass

class CCScreen(MDScreen):
    pass

class MoneyApp(MDApp):
    tablere1 = ObjectProperty(None)
    def build(self):
        #Window.fullscreen = 'auto'
        self.t,self.p="Dark","Green"
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("SELECT * from color;")
        a=v.fetchall()

        if a[0][1]!="":
            self.t=a[0][1]
        if a[0][2]!="":
            self.p=a[0][2]

        self.theme_cls.theme_style=self.t
        self.theme_cls.primary_palette=self.p
        self.theme_cls.primary_hue="A700"
        Window.fullscreen = False
        self.screen=Builder.load_string(screen_helper)
        '''var=sqlite3.connect('data.db')
        v=var.cursor()
        v.execute("""CREATE table data1(id integer PRIMARY KEY,
        dd text NOT NULL,
        ffrom text NOT NULL,
        tto text NOT NULL,
        dc text NOT NULL,
        amt integer NOT NULL,
        more text,
        mainacc text NOT NULL
        )""")
        var.commit()
        var.close()'''
        try:
            self.sendNotif()
        except:
            pass
        
        return self.screen
    
    def sendNotif(self):
        # Get the password from Environment Variable
        password = os.environ.get('password_for_yagmail')

        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("Select * from reminder")
        a=v.fetchall()
        print(a)

        dates=[]
        for i in a:
            dates.append(datetime.strptime(i[1],"%Y-%m-%d").date())

        print(dates)

        v.execute(f'select sum(amt) from data1 where mainacc=\"Bank of Baroda\"')
        ans=v.fetchall()[0][0]
        if ans==None:
            ans=0
        
        ans="{:.2f}".format(ans)
        print(ans)

        v.execute("Select EmailID from user_email")
        emails=v.fetchall()
        print(emails)

        #Check if any one of the date is in the next 7 days
        for i in range(0,len(dates)):
            if datetime.now().date()<=dates[i]<=datetime.now().date()+timedelta(days=7):
                if(float(a[i][4])>=float(ans)):
                    print("Yes")
                    n = ToastNotifier()
    
                    n.show_toast("Bank Balance Notification", a[i][5], duration = 1)
                    # Send Emails
                    
                    if(a[i][6]=="Yes"):
                        v.execute("Select * from email_sent where ddate>=:d1 and ddate<=:d2 and descrip=:dsc",{
                            'd1':datetime.now().date()-timedelta(days=7),
                            'd2':datetime.now().date(),
                            'dsc':a[i][0]
                        })
                        history=v.fetchall()
                        print(history)
                        if(len(history)==0):
                            yag = yagmail.SMTP('', '') # Enter Email ID and Password
                            contents = ["Your Bank Balance is Low!","Please Deposit Money in your Bank Account! The upcoming payment is of Rs."+str(a[i][4])+" on "+str(a[i][1])+" for "+str(a[i][3])+"!"]
                            yag.send(to=str(emails[0][0]),subject="Your Personal Finance Manager!",contents=contents,attachments='my_logo.jpg')

                            v.execute("INSERT INTO email_sent (ddate,descrip) VALUES(:dd,:desc)",{
                                'dd':datetime.now().date(),
                                'desc':a[i][0]
                            })
                else:
                    n = ToastNotifier()

                    n.show_toast(f"{a[i][3]}", a[i][5], duration = 1)
                    if(a[i][6]=="Yes"):
                        v.execute("Select * from email_sent where ddate>=:d1 and ddate<=:d2 and descrip=:dsc",{
                            'd1':datetime.now().date()-timedelta(days=7),
                            'd2':datetime.now().date(),
                            'dsc':a[i][0]
                        })
                        history=v.fetchall()
                        print(history)
                        if(len(history)==0):
                            yag = yagmail.SMTP('', '') # Enter Email ID and Password
                            contents = ["Your Bank Balance is Low!","Please Deposit Money in your Bank Account! The upcoming payment is of Rs."+str(a[i][4])+" on "+str(a[i][1])+" for "+str(a[i][3])+"!"]
                            yag.send(to=str(emails[0][0]),subject="Your Personal Finance Manager!",contents=contents,attachments='my_logo.jpg')

                            v.execute("INSERT INTO email_sent (ddate,descrip) VALUES(:dd,:desc)",{
                                'dd':datetime.now().date(),
                                'desc':a[i][0]
                            })
        var.commit()
        var.close()

    def show_textnamenuu44(self,a):
        self.screen.ids.ups.ids.u3.text=a

    def show_textnamenuu88(self,a):
        self.screen.ids.ups.ids.u7.text=a

    def save1(self):
        #self.screen.ids.ens.ids.enf.text
        var=sqlite3.connect('data.db')
        v=var.cursor()
        ffrom=self.screen.ids.ens.ids.enf.text
        ttype=self.screen.ids.ens.ids.ent.text
        ddate=self.screen.ids.ens.ids.end.text
        aamount=self.screen.ids.ens.ids.ena.text
        mmore=self.screen.ids.ens.ids.enm.text
        ttoo=self.screen.ids.ens.ids.entt.text
        bamount=aamount
        hey=float(float(aamount)*-1)
        v.execute("Select a from accounts")
        a=v.fetchall()
        aa=[i[0] for i in a]
        try:
            if ffrom!='' and ttype!='' and ddate!='' and aamount!='' and ttoo!='' and float(aamount)>0:
                if ffrom in aa and ttoo in aa:
                    if ttype=="Debit":
                        format = "%Y-%m-%d"
                        datetime.strptime(ddate,format)
                        if ttype=="Debit":
                            #str('-') + str(aamount)
                            bamount=float(float(aamount)*-1)
                        v.execute("INSERT INTO data1 (dd,mainacc,ffrom,tto,dc,amt,more) VALUES(:dd,:ma,:f,:ttooo,:dc,:a,:m)",{
                            'dd':ddate,
                            'ma':ffrom,
                            'f':ffrom,
                            'ttooo':ttoo,
                            'dc':ttype,
                            'a':bamount,
                            'm':mmore
                        })
                        v.execute("INSERT INTO data1 (dd,mainacc,ffrom,tto,dc,amt,more) VALUES(:dd,:ma,:f,:ttooo,:dc,:a,:m)",{
                            'dd':ddate,
                            'ma':ttoo,
                            'f':ffrom,
                            'ttooo':ttoo,
                            'dc':"Credit",
                            'a':aamount,
                            'm':mmore
                        })
                        bcloses=MDFlatButton(text="Close",on_release=self.closes)
                        self.dialogs=MDDialog(title="Personal Finance Manager",text="Record Saved!",buttons=[bcloses])
                        self.dialogs.open()
                        self.screen.ids.ens.ids.enf.text=''
                        self.screen.ids.ens.ids.ent.text=''
                        self.screen.ids.ens.ids.ena.text=''
                        self.screen.ids.ens.ids.enm.text=''
                        self.screen.ids.ens.ids.entt.text=''
                    else:
                        format = "%Y-%m-%d"
                        datetime.strptime(ddate,format)
                        v.execute("INSERT INTO data1 (dd,mainacc,ffrom,tto,dc,amt,more) VALUES(:dd,:ma,:f,:ttooo,:dc,:a,:m)",{
                            'dd':ddate,
                            'ma':ttoo,
                            'f':ffrom,
                            'ttooo':ttoo,
                            'dc':ttype,
                            'a':aamount,
                            'm':mmore
                        })
                        v.execute("INSERT INTO data1 (dd,mainacc,ffrom,tto,dc,amt,more) VALUES(:dd,:ma,:f,:ttooo,:dc,:a,:m)",{
                            'dd':ddate,
                            'ma':ffrom,
                            'f':ffrom,
                            'ttooo':ttoo,
                            'dc':"Debit",
                            'a':hey,
                            'm':mmore
                        })
                        bcloses=MDFlatButton(text="Close",on_release=self.closes)
                        self.dialogs=MDDialog(title="Personal Finance Manager",text="Record Saved!",buttons=[bcloses])
                        self.dialogs.open()
                        self.screen.ids.ens.ids.enf.text=''
                        self.screen.ids.ens.ids.ent.text=''
                        self.screen.ids.ens.ids.ena.text=''
                        self.screen.ids.ens.ids.enm.text=''
                        self.screen.ids.ens.ids.entt.text=''
                else:
                    if ttype=="Debit":
                        mmain=ffrom
                    else:
                        mmain=ttoo

                    try:
                        format = "%Y-%m-%d"
                        datetime.strptime(ddate,format)
                        if ttype=="Debit":
                            bamount=float(str('-') + str(aamount))
                        v.execute("INSERT INTO data1 (dd,mainacc,ffrom,tto,dc,amt,more) VALUES(:dd,:ma,:f,:ttooo,:dc,:a,:m)",{
                            'dd':ddate,
                            'ma':mmain,
                            'f':ffrom,
                            'ttooo':ttoo,
                            'dc':ttype,
                            'a':bamount,
                            'm':mmore
                        })
                        bcloses=MDFlatButton(text="Close",on_release=self.closes)
                        self.dialogs=MDDialog(title="Personal Finance Manager",text="Record Saved!",buttons=[bcloses])
                        self.dialogs.open()
                        self.screen.ids.ens.ids.enf.text=''
                        self.screen.ids.ens.ids.ent.text=''
                        self.screen.ids.ens.ids.ena.text=''
                        self.screen.ids.ens.ids.enm.text=''
                        self.screen.ids.ens.ids.entt.text=''
                    except:
                        bclosee=MDFlatButton(text="Close",on_release=self.closee)
                        self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!1",buttons=[bclosee])
                        self.dialogee.open()
                        #print("Error!   1")
            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!2",buttons=[bclosee])
                self.dialogee.open()
                #print("Error!   2")
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!3",buttons=[bclosee])
            self.dialogee.open()
            #print("Error!   3")

        var.commit()
        var.close()
        
    def show_text2(self,word):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        self.screen.ids.ens.ids.ent.text=word
        self.screen.ids.ens.ids.enf.text=""
        if word=="Debit":
            v.execute("Select a from accounts where s=\"Open\"")
            a=v.fetchall()
            aa=[i[0] for i in a]
            aa.sort()
            print(aa)

            self.lst1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_text1(x),
            } for i in aa]
            print(self.lst1)
            self.screen.ids.ens.ids.entt.text=""


            v.execute("select distinct(tto) from data1 where dc=\"Debit\"")
            abc=v.fetchall()
            abc11=[i[0] for i in abc]
            abc11.sort()

            v.execute("Select a from accounts where s=\"Open\"")
            abc=v.fetchall()
            abc12=[i[0] for i in abc]
            abc12.sort()

            abc1=abc12+abc11
            self.lst3=[]

            self.lst3 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_text3(x),
            } for i in abc1]

            self.screen.ids.ens.ids.drop3.disabled=False
        else:
            v.execute("Select a from accounts where s=\"Open\"")
            a=v.fetchall()
            aa=[i[0] for i in a]
            aa.sort()
            self.lst3=[{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_text3(x),
            } for i in aa]
            self.lst1=[]
            self.screen.ids.ens.ids.drop3.disabled=False
            self.screen.ids.ens.ids.entt.text=""

            v.execute("SELECT distinct(ffrom) from data1 where dc=\"Credit\"")
            q=v.fetchall()
            qq1=[i[0] for i in q]
            qq1.sort()

            v.execute("Select a from accounts where s=\"Open\"")
            abc=v.fetchall()
            abc12=[i[0] for i in abc]
            abc12.sort()

            qq=abc12+qq1
            self.lst1=[{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_text1(x),
            } for i in qq]

        
        var.commit()
        var.close()

        #print("HEY",self.lst1)
        self.screen.ids.ens.ids.drop1.disabled=False
        self.menu1=MDDropdownMenu(
            caller=self.screen.ids.ens.ids.drop1,
            items=self.lst1,
            width_mult=5,)

        self.menu3=MDDropdownMenu(
            caller=self.screen.ids.ens.ids.drop3,
            items=self.lst3,
            width_mult=5,)

    def shownormaldatewise(self):
        try:
            self.screen.ids.sos.ids.nda.hint_text=""
            self.screen.ids.sos.ids.ndt.hint_text=""
            self.screen.ids.sos.ids.ndd.hint_text=""
            d1=self.screen.ids.sos.ids.normalfromdate.text
            d2=self.screen.ids.sos.ids.normaltodate.text
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
            data=v.fetchall()
            data1=[]
            for i in data:
                if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                    data1.append(i)

            mainndlist=[]
            for i in data1:
                b=list(i)
                if b[5]<0:
                    b[5]=b[5]*(-1)
                    b[5]="{:.2f}".format(b[5])
                    mainndlist.append(b)
                else:
                    mainndlist.append(b)

            #print(mainndlist)
            self.columnofnormaldatewise=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48))]
            self.tableofnormaldate=MDDataTable(
                            size_hint_y=None,
                            size_hint_x=None,
                            width=1100,
                            height=400,
                            pos_hint={'center_x':0.5,'center_y':0.62},
                            use_pagination=True,
                            column_data=self.columnofnormaldatewise,
                            row_data=mainndlist)
            a=0
            b=0

            for i in mainndlist:
                if i[4]=="Debit":
                    a=a+(float(i[5]))
                else:
                    #print(i[5])
                    b=b+i[5]

            a="{:.2f}".format(a)
            b="{:.2f}".format(b)

            #print("a:",a," b:",b)
            self.screen.ids.sos.ids.ndd.hint_text=str("Credit:")+str(float(b))+str("        Debit:")+str(float(a*(1)))

            #self.tableofnormaldate.open()
            self.screen.ids.sos.add_widget(self.tableofnormaldate)

            var.commit()
            var.close()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def exportshownormaldatewise(self):
        d1=self.screen.ids.sos.ids.normalfromdate.text
        d2=self.screen.ids.sos.ids.normaltodate.text
        if d1!="" and d2!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
            data=v.fetchall()
            data1=[]
            for i in data:
                if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                    data1.append(i)

            mainndlist=[]
            for i in data1:
                b=list(i)
                b[5]=float("{:.2f}".format(b[5]))
                if b[5]<0:
                    b[5]=b[5]*(-1)
                    mainndlist.append(b)
                else:
                    mainndlist.append(b)
            var.commit()
            var.close()
            c=['Id','Date','From','To','D/C','Amount','Narration']
            df=pd.DataFrame(mainndlist,columns=c)
            df.style.set_caption('All Data-> Personal Finance Manager')
            df.to_csv('Exports/Date_Wise.csv',index=False)
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out Date_Wise.csv file in the Exports Folder!",buttons=[bclosee])
            self.dialogee.open()
        else:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def shownormaltypewise(self):
        try:
            self.screen.ids.sos.ids.nda.hint_text=""
            self.screen.ids.sos.ids.ndt.hint_text=""
            self.screen.ids.sos.ids.ndd.hint_text=""
            ntype=self.screen.ids.sos.ids.normaltype.text

            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{ntype}\"")
            ntdata=v.fetchall()

            mainntlist=[]
            m=0
            for i in ntdata:
                b=list(i)
                m+=float(b[5])
                s="{:.2f}".format(m)
                b.append(s)
                b[5]=float("{:.2f}".format(b[5]))
                if b[5]<0:
                    aa=b[5]
                    aab=aa*2
                    b[5]=aa-aab
                mainntlist.append(b)

            self.columnoftype=[("Id",dp(13)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48)),("Balance",dp(30))]
            self.tableoftype=MDDataTable(
                            size_hint_y=None,
                            height=400,
                            size_hint_x=None,
                            width=1250,
                            pos_hint={'center_x':0.5,'center_y':0.62},
                            use_pagination=True,
                            column_data=self.columnoftype,
                            row_data=mainntlist)

            v.execute(f"select sum(amt) from data1 where mainacc=\"{ntype}\" and dc=\"Debit\"")
            a=v.fetchall()
            v.execute(f"select sum(amt) from data1 where mainacc=\"{ntype}\" and dc=\"Credit\"")
            b=v.fetchall()
            #print(a[0][0])
            #print(b[0][0])
            if a[0][0]==None or a[0][0]==0:
                aa=0
            else:
                aa=float(a[0][0])*(-1)
                aa="{:.2f}".format(aa)
            if b[0][0]==None or b[0][0]==0:
                bb=0
            else:
                bb=float(b[0][0])
                bb="{:.2f}".format(bb)

            self.screen.ids.sos.ids.ndt.hint_text=str("Credit:")+str(bb)+str("        Debit:")+str(float(aa))
            
            var.commit()
            var.close()
            #self.tableoftype.open()
            self.screen.ids.sos.add_widget(self.tableoftype)
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()
            
    def exportshownormaltypewise(self):
        ntype=self.screen.ids.sos.ids.normaltype.text
        if ntype!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{ntype}\"")
            ntdata=v.fetchall()
            var.commit()
            var.close()

            mainntlist=[]
            m=0
            for i in ntdata:
                b=list(i)
                m+=float(b[5])
                s="{:.2f}".format(m)
                b.append(s)
                if b[5]<0:
                    b[5]=float(b[5])*-1
                mainntlist.append(b)

            c=['Id','Date','From','To','D/C','Amount','Narration','Balance']
            df=pd.DataFrame(mainntlist,columns=c)
            df.style.set_caption('All Data-> Personal Finance Manager')
            df.to_csv('Exports/Account_Wise.csv',index=False)
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out Account_Wise.csv file in the Exports Folder!",buttons=[bclosee])
            self.dialogee.open()
        else:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()
            

    def showalltypewise(self):
        self.screen.ids.sos.ids.nda.hint_text=""
        self.screen.ids.sos.ids.ndt.hint_text=""
        self.screen.ids.sos.ids.ndd.hint_text=""
        d1=self.screen.ids.sos.ids.alltypefromdate.text
        d2=self.screen.ids.sos.ids.alltypetodate.text
        attype=self.screen.ids.sos.ids.alltype.text

        try:
            b=datetime.strptime(d1,"%Y-%m-%d")
            c=datetime.strptime(d2,"%Y-%m-%d")
            if attype!="":
                var=sqlite3.connect('data.db')
                v=var.cursor()
                v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{attype}\"")
                ntdata=v.fetchall()

                mainntlist0=[]
                m=0
                for i in ntdata:
                    b=list(i)
                    m+=float(b[5])
                    s="{:.2f}".format(m)
                    b.append(s)
                    if b[5]<0:
                        aa=b[5]
                        aab=aa*2
                        b[5]=aa-aab
                    mainntlist0.append(b)

                var.commit()
                var.close()
                mainatlist=[]
                for i in mainntlist0:
                    if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                        mainatlist.append(i)

                self.columnofalltype=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(50)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48)),("Balance",dp(30))]
                self.tableofalltype=MDDataTable(
                                size_hint_y=None,
                                height=400,
                                size_hint_x=None,
                                width=1300,
                                pos_hint={'center_x':0.5,'center_y':0.62},
                                use_pagination=True,
                                column_data=self.columnofalltype,
                                row_data=mainatlist)

                #self.tableofalltype.open()
                self.screen.ids.sos.add_widget(self.tableofalltype)
                a=0
                b=0
                for i in mainatlist:
                    if i[4]=="Debit":
                        a=a+i[5]
                    else:
                        b=b+i[5]
                
                a="{:.2f}".format(a)
                b="{:.2f}".format(b)

                self.screen.ids.sos.ids.nda.hint_text=str("Credit:")+str(float(b))+str("        Debit:")+str(float(a*(1)))
            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
                self.dialogee.open()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def exportshowalltypewise(self):
        d1=self.screen.ids.sos.ids.alltypefromdate.text
        d2=self.screen.ids.sos.ids.alltypetodate.text
        attype=self.screen.ids.sos.ids.alltype.text
        try:
            b=datetime.strptime(d1,"%Y-%m-%d")
            c=datetime.strptime(d2,"%Y-%m-%d")
            if attype!="":
                var=sqlite3.connect('data.db')
                v=var.cursor()
                v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{attype}\"")
                ntdata=v.fetchall()

                mainntlist0=[]
                m=0
                for i in ntdata:
                    b=list(i)
                    m+=float(b[5])
                    s="{:.2f}".format(m)
                    b.append(s)
                    if b[5]<0:
                        aa=b[5]
                        aab=aa*2
                        b[5]=aa-aab
                    mainntlist0.append(b)

                var.commit()
                var.close()
                mainatlist=[]
                for i in mainntlist0:
                    if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                        mainatlist.append(i)

                c=['Id','Date','From','To','D/C','Amount','Narration','Balance']
                df=pd.DataFrame(mainatlist,columns=c)
                df.style.set_caption('All Data-> Personal Finance Manager')
                df.to_csv('Exports/Account_and_Date_Wise.csv',index=False)
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out Account_and_Date_Wise.csv file in the Exports Folder!",buttons=[bclosee])
                self.dialogee.open()

            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
                self.dialogee.open()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def showall(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
        data=v.fetchall()
        mainndlist=[]
        for i in data:
            b=list(i)
            b[5]="{:.2f}".format(b[5])
            b[5]=float(b[5])
            if b[5]<0:
                aa=b[5]
                aab=aa*2
                b[5]=aa-aab
            mainndlist.append(b)

        self.columnofall=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(53))]
        self.tableofall=MDDataTable(
						size_hint_y=None,
						height=450,
                        size_hint_x=None,
                        width=1200,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
						column_data=self.columnofall,
						row_data=mainndlist)

        #self.tableofall.open()
        self.screen.ids.sos.add_widget(self.tableofall)
        
        var.commit()
        var.close()

    def exportall(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
        data=v.fetchall()
        var.commit()
        var.close()

        mainndlist=[]
        for i in data:
            b=list(i)
            b[5]=float("{:.2f}".format(b[5]))
            if b[5]<0:
                aa=b[5]
                aab=aa*2
                b[5]=aa-aab
            mainndlist.append(b)

        c=['Id','Date','From','Tp','D/C','Amount','Narration']
        df=pd.DataFrame(mainndlist,columns=c)
        df.to_csv('Exports/All_Data.csv',index=False)
        bclosee=MDFlatButton(text="Close",on_release=self.closee)
        self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out All_Data.csv file in the Exports Folder!",buttons=[bclosee])
        self.dialogee.open()

    def socshowall(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
        data=v.fetchall()
        mainndlist=[]
        for i in data:
            b=list(i)
            b[5]="{:.2f}".format(b[5])
            b[5]=float(b[5])
            if b[5]<0:
                aa=b[5]
                aab=aa*2
                b[5]=aa-aab
            mainndlist.append(b)

        self.columnofall=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(53))]
        self.tableofall=MDDataTable(
						size_hint_y=None,
						height=450,
                        size_hint_x=None,
                        width=1200,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
						column_data=self.columnofall,
						row_data=mainndlist)

        #self.tableofall.open()
        self.screen.ids.socs.add_widget(self.tableofall)
        
        var.commit()
        var.close()

    def shownormaltypewiseu(self):
        ntype=self.screen.ids.ups.ids.u3.text
        if ntype=="":
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()
        else:
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{ntype}\"")
            ntdata=v.fetchall()
            #print(ntdata)
            mainntlist=[]
            m=0
            for i in ntdata:
                b=list(i)
                m+=float(b[5])
                s="{:.2f}".format(m)
                b.append(s)
                if b[5]<0:
                    aa=b[5]
                    aab=aa*2
                    b[5]=aa-aab
                mainntlist.append(b)
            #print(mainntlist)
            self.columnoftypeu=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(45)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48)),("Balance",dp(30))]
            self.tableoftypeu=MDDataTable(
                            size_hint_y=None,
                            height=450,
                            size_hint_x=None,
                            width=1250,
                            pos_hint={'center_x':0.5,'center_y':0.62},
                            use_pagination=True,
                            column_data=self.columnoftypeu,
                            row_data=mainntlist)
            self.tableoftypeu.bind(on_row_press=self.tableoftype_press)
            
            #self.tableoftypeu.open()
            #print(mainntlist)
            var.commit()
            var.close()
            self.screen.ids.ups.add_widget(self.tableoftypeu)

    def shownormaldatewiseu(self):
        try:
            d1=self.screen.ids.ups.ids.u1.text
            d2=self.screen.ids.ups.ids.u2.text
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
            data=v.fetchall()
            data1=[]
            for i in data:
                if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                    data1.append(i)
            data2=[]

            for i in data1:
                c=list(i)
                if c[5]<0:
                    c[5]=float(c[5])*(-1)
                else:
                    pass
                data2.append(c)

            self.columnofnormaldatewiseu=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(45)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48))]
            self.tableofnormaldateu=MDDataTable(
                            size_hint_y=None,
                            size_hint_x=None,
                            width=1100,
                            height=450,
                            pos_hint={'center_x':.5,'center_y':.5},
                            use_pagination=True,
                            column_data=self.columnofnormaldatewiseu,
                            row_data=data2)
            self.tableofnormaldateu.bind(on_row_press=self.tableoftype_press)
            
            #self.tableofnormaldateu.open()
            self.screen.ids.ups.add_widget(self.tableofnormaldateu)
            var.commit()
            var.close()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def showalltypewiseu(self):
        d1=self.screen.ids.ups.ids.u5.text
        d2=self.screen.ids.ups.ids.u6.text
        attype=self.screen.ids.ups.ids.u7.text

        try:
            b=datetime.strptime(d1,"%Y-%m-%d")
            c=datetime.strptime(d2,"%Y-%m-%d")
            if attype!="":
                var=sqlite3.connect('data.db')
                v=var.cursor()
                v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where mainacc=\"{attype}\"")
                ntdata=v.fetchall()
                #print(ntdata)
                mainntlist0=[]
                m=0
                for i in ntdata:
                    b=list(i)
                    m+=float(b[5])
                    s="{:.2f}".format(m)
                    b.append(s)
                    if b[5]<0:
                        aa=b[5]
                        aab=aa*2
                        b[5]=aa-aab
                    mainntlist0.append(b)

                var.commit()
                var.close()
                mainatlist=[]
                for i in mainntlist0:
                    if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                        mainatlist.append(i)
                #print(mainatlist)
                self.columnofalltypeu=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(45)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48)),("Balance",dp(30))]
                self.tableofalltypeu=MDDataTable(
                                size_hint_y=None,
                                height=450,
                                size_hint_x=None,
                                width=1250,
                                pos_hint={'center_x':0.5,'center_y':0.62},
                                use_pagination=True,
                                column_data=self.columnofalltypeu,
                                row_data=mainatlist)
                self.tableofalltypeu.bind(on_row_press=self.tableoftype_press)
                
                #self.tableofalltypeu.open()
                self.screen.ids.ups.add_widget(self.tableofalltypeu)
            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
                self.dialogee.open()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def showallu(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("select id,dd,ffrom,tto,dc,amt,more from data1")
        data=v.fetchall()
        mainndlist=[]
        for i in data:
            b=list(i)
            b[5]=float("{:.2f}".format(b[5]))
            if float(b[5])<0:
                aa=b[5]
                aab=aa*2
                b[5]=aa-aab
            mainndlist.append(b)

        self.columnofallu=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(53))]
        self.tableofallu=MDDataTable(
						size_hint_y=None,
						height=450,
                        size_hint_x=None,
                        width=1100,
                        use_pagination=True,
                        pos_hint={'center_x':0.5,'center_y':0.62},
						column_data=self.columnofallu,
						row_data=mainndlist)
        self.tableofallu.bind(on_row_press=self.tableoftype_press)

        #self.tableofallu.open()
        self.screen.ids.ups.add_widget(self.tableofallu)
        
        var.commit()
        var.close()

    def tableoftype_press(self,a,b):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        try:
            v.execute(f"select id,dd,ffrom,tto,dc,amt,more,mainacc from data1 where id={int(b.text)}")
            self.d=v.fetchall()
        except:
            pass

        try:
            if self.d[0][4]=='Debit':
                self.screen.ids.ups.ids.uu3.disabled=True
                self.screen.ids.ups.ids.uu5.disabled=False

                v.execute("Select a from accounts")
                a1=v.fetchall()
                aa=[i[0] for i in a1]
                aa.sort()
                #self.lsstfrom=[{'text':f'{i}'} for i in aa]
                self.lsstfrom = [{
                    "text": f"{i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{i}": self.show_textnamenuu4(x),
                } for i in aa]
                #self.lsstfrom=[{'text':'Bank of Baroda'},{'text':'Cash'},{'text':'PhonePe Wallet'}]

                self.lsstto=[]
                v.execute('select distinct(tto) from data1 where dc=\"Debit\"')
                s=v.fetchall()
                s1=[i[0] for i in s if i[0] not in aa]
                s1.sort()
                #self.lsstto=[{'text':f'{i}'} for i in s1]
                self.lsstto = [{
                    "text": f"{i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{i}": self.show_textnamenuu6(x),
                } for i in s1]
                self.lsstto=self.lsstfrom+self.lsstto
                
                b=float(self.d[0][5])*2
                a=float(self.d[0][5])-b
            else:
                self.screen.ids.ups.ids.uu3.disabled=False
                self.screen.ids.ups.ids.uu5.disabled=True
                a=float(self.d[0][5])

                v.execute("Select a from accounts")
                a1=v.fetchall()
                aa=[i[0] for i in a1]
                aa.sort()
                #self.lsstto=[{'text':f'{i}'} for i in aa]
                self.lsstto = [{
                    "text": f"{i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{i}": self.show_textnamenuu6(x),
                } for i in aa]

                #self.lsstto=[{'text':'Bank of Baroda'},{'text':'Cash'},{'text':'PhonePe Wallet'}]
                self.lsstfrom=[]
                v.execute('select distinct(ffrom) from data1 where dc=\"Credit\"')
                s=v.fetchall()
                s1=[i[0] for i in s if i[0] not in aa]
                s1.sort()
                #self.lsstfrom=[{'text':f'{i}'} for i in s1]
                self.lsstfrom = [{
                    "text": f"{i}",
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=f"{i}": self.show_textnamenuu4(x),
                } for i in s1]
                self.lsstfrom=self.lsstto+self.lsstfrom
                
        except:
            pass

        self.screen.ids.ups.ids.uu4.disabled=False
        self.screen.ids.ups.ids.uu6.disabled=False
        try:
            self.screen.ids.ups.ids.uu1.text=self.d[0][4]
            self.screen.ids.ups.ids.uu3.text=self.d[0][2]
            self.screen.ids.ups.ids.uu5.text=self.d[0][3]
            self.screen.ids.ups.ids.uu7.text=self.d[0][1]
            self.screen.ids.ups.ids.uu8.text=str(a)
            self.screen.ids.ups.ids.uu9.text=self.d[0][6]
        except:
            pass

        
        self.menu1u=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.uu4,
            items=self.lsstfrom,
            width_mult=5,)
        """
            callback=self.show_textnamenuu4,"""

        self.menu3u=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.uu6,
            items=self.lsstto,
            width_mult=5,)
        """
            callback=self.show_textnamenuu6,"""
        

        var.commit()
        var.close()

    def show_textnamenuu4(self,a):
        self.screen.ids.ups.ids.uu3.text=a

    def show_textnamenuu6(self,a):
        self.screen.ids.ups.ids.uu5.text=a

    def updatee(self):
        try:
            var=sqlite3.connect('data.db')
            v=var.cursor()
            itype=self.screen.ids.ups.ids.uu1.text
            ifrom=self.screen.ids.ups.ids.uu3.text
            ito=self.screen.ids.ups.ids.uu5.text
            idate=self.screen.ids.ups.ids.uu7.text
            iamt=self.screen.ids.ups.ids.uu8.text
            inarr=self.screen.ids.ups.ids.uu9.text

            flag=0
            test=[self.d[0][0],self.d[0][1],self.d[0][2],self.d[0][3],self.d[0][4],self.d[0][5],self.d[0][6]]
            if itype=='Credit':
                mainlst=[self.d[0][0],idate,ifrom,ito,itype,float(iamt),inarr]
            elif itype=='Debit':
                mainlst=[self.d[0][0],idate,ifrom,ito,itype,float(float(iamt)*-1),inarr]
            
            print("self.d->",self.d)

            lst1=[idate,ifrom,ito,itype,iamt,inarr,self.d[0][7]]
                
            if itype=="Credit":
                ttype1="Debit"
            else:
                ttype1="Credit"

            tid2=int(self.d[0][0])+1
            tid1=int(self.d[0][0])-1

            v.execute(f"select id,dd,ffrom,tto,dc,amt,more,mainacc from data1 where id={tid1}")
            lst2=v.fetchall()
            print("lst2->",lst2)
                
            v.execute(f"select id,dd,ffrom,tto,dc,amt,more,mainacc from data1 where id={tid2}")
            lst3=v.fetchall()
            print("lst3->",lst3)

            idtodo=None

            if itype=='Credit':
                d2=[(int(self.d[0][0]+1),self.d[0][1],self.d[0][2],self.d[0][3],'Debit',(float(self.d[0][5])*-1),self.d[0][6],self.d[0][2])]
                d1=[(int(self.d[0][0]-1),self.d[0][1],self.d[0][2],self.d[0][3],'Debit',(float(self.d[0][5])*-1),self.d[0][6],self.d[0][2])]
                print("d2->",d2)
            elif itype=='Debit':
                d2=[(int(self.d[0][0]+1),self.d[0][1],self.d[0][2],self.d[0][3],'Credit',(float(self.d[0][5])*-1),self.d[0][6],self.d[0][3])]
                d1=[(int(self.d[0][0]-1),self.d[0][1],self.d[0][2],self.d[0][3],'Credit',(float(self.d[0][5])*-1),self.d[0][6],self.d[0][3])]
                #print(d1)

            if d2==lst3:
                idtodo=self.d[0][0]+1
                print("OP")
                main2ndlst=lst3
                print("To do->",lst3)
            elif d1==lst2:
                idtodo=self.d[0][0]-1
                print("OP")
                main2ndlst=lst2
                print("To do->",lst2)

            print(f"{idtodo=}")
            
            i=self.d[0][0]

            z=float(self.screen.ids.ups.ids.uu8.text)

            if itype=='Debit':
                a=str('-')+str(z)
                z=float(a)
            #'iddd':self.d[0][0],   id=:iddd,

            if self.screen.ids.ups.ids.uu1.text=="Debit":
                mainaccvar=self.screen.ids.ups.ids.uu3.text
            else:
                mainaccvar=self.screen.ids.ups.ids.uu5.text

            if idtodo is None:
                print("lel1")
                v.execute(f"UPDATE data1 SET dd=:ddd,dc=:dc,ffrom=:ffromf,tto=:ttot,amt=:amta,more=:morem,mainacc=:mainaccv where id={i}",{
                    
                    'ddd':self.screen.ids.ups.ids.uu7.text,
                    'dc':self.screen.ids.ups.ids.uu1.text,
                    'ffromf':self.screen.ids.ups.ids.uu3.text,
                    'ttot':self.screen.ids.ups.ids.uu5.text,
                    'amta':z,
                    'morem':self.screen.ids.ups.ids.uu9.text,
                    'mainaccv':mainaccvar
                    })
            else:
                print("lel2")
                a1=self.d[0][4]
                a2=main2ndlst[0][4]
                if itype=="Credit":
                    aa1="Credit"
                    aa2="Debit"
                    v.execute(f"UPDATE data1 SET dd=:ddd,ffrom=:ffromf,tto=:ttot,amt=:amta,more=:morem,mainacc=:macc where id={i}",{                    
                        'ddd':self.screen.ids.ups.ids.uu7.text,
                        'ffromf':self.screen.ids.ups.ids.uu3.text,
                        'ttot':self.screen.ids.ups.ids.uu5.text,
                        'amta':float(self.screen.ids.ups.ids.uu8.text),
                        'morem':self.screen.ids.ups.ids.uu9.text,
                        'macc':self.screen.ids.ups.ids.uu5.text
                    })
                    v.execute(f"UPDATE data1 SET dd=:ddd,ffrom=:ffromf,tto=:ttot,amt=:amta,more=:morem,mainacc=:macc where id={idtodo}",{                   
                        'ddd':self.screen.ids.ups.ids.uu7.text,
                        'ffromf':self.screen.ids.ups.ids.uu3.text,
                        'ttot':self.screen.ids.ups.ids.uu5.text,
                        'amta':float(self.screen.ids.ups.ids.uu8.text)*(-1),
                        'morem':self.screen.ids.ups.ids.uu9.text,
                        'macc':self.screen.ids.ups.ids.uu3.text
                    })

                else:
                    aa1="Debit"
                    aa2="Credit"
                    v.execute(f"UPDATE data1 SET dd=:ddd,ffrom=:ffromf,tto=:ttot,amt=:amta,more=:morem,mainacc=:macc where id={i}",{                
                        'ddd':self.screen.ids.ups.ids.uu7.text,
                        'ffromf':self.screen.ids.ups.ids.uu3.text,
                        'ttot':self.screen.ids.ups.ids.uu5.text,
                        'amta':float(self.screen.ids.ups.ids.uu8.text)*(-1),
                        'morem':self.screen.ids.ups.ids.uu9.text,
                        'macc':self.screen.ids.ups.ids.uu3.text
                    })
                    v.execute(f"UPDATE data1 SET dd=:ddd,ffrom=:ffromf,tto=:ttot,amt=:amta,more=:morem,mainacc=:macc where id={idtodo}",{                    
                        'ddd':self.screen.ids.ups.ids.uu7.text,
                        'ffromf':self.screen.ids.ups.ids.uu3.text,
                        'ttot':self.screen.ids.ups.ids.uu5.text,
                        'amta':float(self.screen.ids.ups.ids.uu8.text),
                        'morem':self.screen.ids.ups.ids.uu9.text,
                        'macc':self.screen.ids.ups.ids.uu5.text
                    })

            var.commit()
            var.close()
            #print("---------------------------------------")
            self.screen.ids.ups.ids.uu1.text=''
            self.screen.ids.ups.ids.uu3.text=''
            self.screen.ids.ups.ids.uu5.text=''
            self.screen.ids.ups.ids.uu7.text=''
            self.screen.ids.ups.ids.uu8.text=''
            self.screen.ids.ups.ids.uu9.text=''
            bclosesd=MDFlatButton(text="Close",on_release=self.closesd)
            self.dialogsd=MDDialog(title="Personal Finance Manager",text="Entry Updated!",buttons=[bclosesd])
            self.dialogsd.open()
            self.d=[]
            self.screen.ids.ups.ids.uu4.disabled=True
            self.screen.ids.ups.ids.uu6.disabled=True
        except:
            bcloseed=MDFlatButton(text="Close",on_release=self.closeed)
            self.dialogeed=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bcloseed])
            self.dialogeed.open()

    def deletee(self):
        try:
            var=sqlite3.connect('data.db')
            v=var.cursor()
            itype=self.screen.ids.ups.ids.uu1.text
            ifrom=self.screen.ids.ups.ids.uu3.text
            ito=self.screen.ids.ups.ids.uu5.text
            idate=self.screen.ids.ups.ids.uu7.text
            iamt=self.screen.ids.ups.ids.uu8.text
            inarr=self.screen.ids.ups.ids.uu9.text

            flag=0
            test=[self.d[0][0],self.d[0][1],self.d[0][2],self.d[0][3],self.d[0][4],self.d[0][5],self.d[0][6]]
            if itype=='Credit':
                mainlst=[self.d[0][0],idate,ifrom,ito,itype,float(iamt),inarr]
            elif itype=='Debit':
                mainlst=[self.d[0][0],idate,ifrom,ito,itype,float(float(iamt)*-1),inarr]

            print(test)
            print(mainlst)

            if test==mainlst:
                print("OP")
                flag=1
            else:
                a="adasf"+15748178+"Afaf"

            lst1=[idate,ifrom,ito,itype,iamt,inarr,self.d[0][7]]
            
            if itype=="Credit":
                ttype1="Debit"
            else:
                ttype1="Credit"

            tid2=int(self.d[0][0])+1
            tid1=int(self.d[0][0])-1

            v.execute(f"select id,dd,ffrom,tto,dc,amt,more,mainacc from data1 where id={tid1}")
            lst2=v.fetchall()
            print(lst2)
            #
            v.execute(f"select id,dd,ffrom,tto,dc,amt,more,mainacc from data1 where id={tid2}")
            lst3=v.fetchall()
            #print(lst3)

            idtodo=None

            if itype=='Credit':
                d2=[(int(self.d[0][0]+1),idate,ifrom,ito,'Debit',(float(iamt)*-1),inarr,ifrom)]
                d1=[(int(self.d[0][0]-1),idate,ifrom,ito,'Debit',(float(iamt)*-1),inarr,ifrom)]
                #print(d1)
            elif itype=='Debit':
                d2=[(int(self.d[0][0]+1),idate,ifrom,ito,'Credit',(float(iamt)),inarr,ito)]
                d1=[(int(self.d[0][0]-1),idate,ifrom,ito,'Credit',(float(iamt)),inarr,ito)]
                #print(d1)

            if d2==lst3:
                idtodo=self.d[0][0]+1
                #print("OP")
            elif d1==lst2:
                idtodo=self.d[0][0]-1
                #print("OP")

            #print(f"{idtodo=}")

            i=self.d[0][0]

            if idtodo is None:
                v.execute(f"DELETE from data1 where id={i}")
            else:
                v.execute(f"DELETE from data1 where id={i}")
                v.execute(f"DELETE from data1 where id={idtodo}")

            var.commit()
            var.close()
            self.screen.ids.ups.ids.uu1.text=''
            self.screen.ids.ups.ids.uu3.text=''
            self.screen.ids.ups.ids.uu5.text=''
            self.screen.ids.ups.ids.uu7.text=''
            self.screen.ids.ups.ids.uu8.text=''
            self.screen.ids.ups.ids.uu9.text=''
            bclosesd=MDFlatButton(text="Close",on_release=self.closesd)
            self.dialogsd=MDDialog(title="Personal Finance Manager",text="Entry Deleted!",buttons=[bclosesd])
            self.dialogsd.open()
            self.d=[]
            self.screen.ids.ups.ids.uu4.disabled=True
            self.screen.ids.ups.ids.uu6.disabled=True

        except:
            bcloseed=MDFlatButton(text="Close",on_release=self.closeed)
            self.dialogeed=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bcloseed])
            self.dialogeed.open()


    def socshownormaltypewise(self):
        self.screen.ids.socs.ids.socnda.hint_text=""
        self.screen.ids.socs.ids.socndt.hint_text=""
        ntype=self.screen.ids.socs.ids.socnormaltype.text
        if ntype!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where ffrom=\"{ntype}\" or tto=\"{ntype}\"")
            ntdata=v.fetchall()

            mainntlist=[]
            for i in ntdata:
                b=list(i)
                b[5]=float("{:.2f}".format(b[5]))
                if b[5]<0:
                    b[5]=float(b[5])*(-1)

                mainntlist.append(b)

            self.soccolumnoftype=[("Id",dp(13)),("Date",dp(23)),("From",dp(40)),("To",dp(40)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48))]
            self.soctableoftype=MDDataTable(
                            size_hint_y=None,
                            height=400,
                            size_hint_x=None,
                            width=1110,
                            pos_hint={'center_x':0.5,'center_y':0.62},
                            use_pagination=True,
                            column_data=self.soccolumnoftype,
                            row_data=mainntlist)

            #self.soctableoftype.open()
            self.screen.ids.socs.add_widget(self.soctableoftype)

            d=0
            c=0
            for i in mainntlist:
                if i[4]=="Debit":
                    d+=i[5]
                else:
                    c+=i[5]

            d="{:.2f}".format(d)
            c="{:.2f}".format(c)

            self.screen.ids.socs.ids.socndt.hint_text=str("Debit:")+str(d)+str("   Credit:")+str(c)
            var.commit()
            var.close()
        else:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()
       
    def exportsocshownormaltypewise(self):
        self.screen.ids.socs.ids.socnda.hint_text=""
        self.screen.ids.socs.ids.socndt.hint_text=""
        ntype=self.screen.ids.socs.ids.socnormaltype.text
        if ntype!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where ffrom=\"{ntype}\" or tto=\"{ntype}\"")
            ntdata=v.fetchall()

            mainntlist=[]
            for i in ntdata:
                b=list(i)
                if b[5]<0:
                    b[5]=float(b[5])*(-1)
                mainntlist.append(b)
            var.commit()
            var.close()
            
            c=['Id','Date','From','To','D/C','Amount','Narration']
            df=pd.DataFrame(mainntlist,columns=c)
            df.to_csv('Exports/Category_Wise.csv',index=False)
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out Category_Wise.csv file in the Exports Folder!",buttons=[bclosee])
            self.dialogee.open()
        else:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()


    def socshowalltypewise(self):
        self.screen.ids.socs.ids.socnda.hint_text=""
        self.screen.ids.socs.ids.socndt.hint_text=""
        d1=self.screen.ids.socs.ids.socalltypefromdate.text
        d2=self.screen.ids.socs.ids.socalltypetodate.text
        attype=self.screen.ids.socs.ids.socalltype.text
        try:
            b=datetime.strptime(d1,"%Y-%m-%d")
            c=datetime.strptime(d2,"%Y-%m-%d")
            if attype!="":

                var=sqlite3.connect('data.db')
                v=var.cursor()
                v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where ffrom=\"{attype}\" or tto=\"{attype}\"")
                ntdata=v.fetchall()

                mainntlist0=[]
                for i in ntdata:
                    b=list(i)
                    b[5]=float("{:.2f}".format(b[5]))
                    if b[5]<0:
                        b[5]=float(b[5])*(-1)
                    mainntlist0.append(b)

                var.commit()
                var.close()
                mainatlist=[]
                for i in mainntlist0:
                    if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                        mainatlist.append(i)

                self.soccolumnofalltype=[("Id",dp(10)),("Date",dp(23)),("From",dp(40)),("To",dp(50)),("D/C",dp(25)),("Amount",dp(20)),("Narration",dp(48))]
                self.soctableofalltype=MDDataTable(
                                size_hint_y=None,
                                height=400,
                                size_hint_x=None,
                                width=1117,
                                pos_hint={'center_x':0.5,'center_y':0.62},
                                use_pagination=True,
                                column_data=self.soccolumnofalltype,
                                row_data=mainatlist)
               
                #self.soctableofalltype.open()
                self.screen.ids.socs.add_widget(self.soctableofalltype)
               
                d=0
                c=0
                for i in mainatlist:
                    if i[4]=="Debit":
                        d+=i[5]
                    else:
                        c+=i[5]
                
                c="{:.2f}".format(c)
                d="{:.2f}".format(d)

                self.screen.ids.socs.ids.socnda.hint_text=str("Debit:")+str(d)+str("   Credit:")+str(c)
            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
                self.dialogee.open()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def exportsocshowalltypewisee(self):
        d1=self.screen.ids.socs.ids.socalltypefromdate.text
        d2=self.screen.ids.socs.ids.socalltypetodate.text
        attype=self.screen.ids.socs.ids.socalltype.text
        try:
            b=datetime.strptime(d1,"%Y-%m-%d")
            c=datetime.strptime(d2,"%Y-%m-%d")
            if attype!="":

                var=sqlite3.connect('data.db')
                v=var.cursor()
                v.execute(f"select id,dd,ffrom,tto,dc,amt,more from data1 where ffrom=\"{attype}\" or tto=\"{attype}\"")
                ntdata=v.fetchall()

                mainntlist0=[]
                for i in ntdata:
                    b=list(i)
                    b[5]="{:.2f}".format(b[5])
                    if b[5]<0:
                        b[5]=float(b[5])*(-1)
                    mainntlist0.append(b)

                var.commit()
                var.close()
                mainatlist=[]
                for i in mainntlist0:
                    if datetime.strptime(d1,"%Y-%m-%d")<=datetime.strptime(i[1],"%Y-%m-%d") and datetime.strptime(d2,"%Y-%m-%d")>=datetime.strptime(i[1],"%Y-%m-%d"):
                        mainatlist.append(i)

                c=['Id','Date','From','To','D/C','Amount','Narration']
                df=pd.DataFrame(mainatlist,columns=c)
                df.to_csv('Exports/Category_and_Date_Wise.csv',index=False)
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="The Data has been Exported Successfully!\nCheck Out Category_and_Date_Wise.csv file in the Exports Folder!",buttons=[bclosee])
                self.dialogee.open()
            else:
                bclosee=MDFlatButton(text="Close",on_release=self.closee)
                self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
                self.dialogee.open()
        except:
            bclosee=MDFlatButton(text="Close",on_release=self.closee)
            self.dialogee=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bclosee])
            self.dialogee.open()

    def startsoc(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        v.execute("select distinct(ffrom) from data1")
        first=v.fetchall()
        v.execute("select distinct(tto) from data1")
        second=v.fetchall()
        tp=['Bank of Baroda','Cash','PhonePe Wallet']
        data=[]
        for i in first:
            if i[0] not in tp and i[0] not in data:
                data.append(i[0])
        for i in second:
            if i[0] not in tp and i[0] not in data:
                data.append(i[0])

        data.sort()
        maindata1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.socshow_textnamenu(x),
            } for i in data]

        maindata2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.socshow_textalltypemenu(x),
            } for i in data]
        #print(maindata)

        self.socnamenu=MDDropdownMenu(
            caller=self.screen.ids.socs.ids.socdrop4,
            items=maindata1,
            width_mult=5,)

        self.socalltypemenu=MDDropdownMenu(
            caller=self.screen.ids.socs.ids.socdrop5,
            items=maindata2,
            width_mult=5,)

        var.commit()
        var.close()

    def starten(self):
        l=["Debit","Credit"]
        self.lst2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_text2(x),
            } for i in l]
        self.menu2=MDDropdownMenu(
            caller=self.screen.ids.ens.ids.drop2,
            items=self.lst2,
            width_mult=4,)

    def startup(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        
        v.execute("Select a from accounts")
        a=v.fetchall()
        aa=[i[0] for i in a]
        #lst=[{'text':f'{i}'} for i in aa]

        lst44=[{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_textnamenuu44(x),
            } for i in aa]

        lst88=[{
            "text": f"{i}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=f"{i}": self.show_textnamenuu88(x),
        } for i in aa]

        lstupdate1=[{
            "text": f"{i}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=f"{i}": self.show_textnamenuu88(x),
        } for i in aa]

        lst22=[{
            "text": f"{i}",
            "viewclass": "OneLineListItem",
            "on_release": lambda x=f"{i}": self.show_textnamenuu22(x),
        } for i in ['Credit','Debit']]

        self.u44=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.u4,
            items=lst44,
            width_mult=4,)

        self.u88=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.u8,
            items=lst88,
            width_mult=4,)

        self.update1=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.u8,
            items=lstupdate1,
            width_mult=4,)

        self.menutotype=MDDropdownMenu(
            caller=self.screen.ids.ups.ids.uu2,
            items=lst22,
            width_mult=4,)

        var.commit()
        var.close()

    def startso(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        v.execute("Select a from accounts")
        a=v.fetchall()
        aa=[i[0] for i in a]
        lst1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_textnamenu(x),
            } for i in aa]
        
        lst2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.show_textalltypemenu(x),
            } for i in aa]
        
        self.namenu=MDDropdownMenu(
            caller=self.screen.ids.sos.ids.drop4,
            items=lst1,
            width_mult=4,)

        self.alltypemenu=MDDropdownMenu(
            caller=self.screen.ids.sos.ids.drop5,
            items=lst2,
            width_mult=4,)

        var.commit()
        var.close()

    def startac(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("Select a from accounts")
        a=v.fetchall()
        aa=[i[0] for i in a]
        aa.sort()
        lst = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.updatemenushow(x),
            } for i in aa]

        v.execute("Select a from accounts where s=\"Open\"")
        a1=v.fetchall()
        aa1=[i[0] for i in a1]
        aa1.sort()
        lst1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.deletemenushow(x),
            } for i in aa1]

        lst2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.updatestatusmenushow(x),
            } for i in ['Open','Closed']]

        self.deletemenu=MDDropdownMenu(
            caller=self.screen.ids.acs.ids.dropdelete,
            items=lst1,
            width_mult=4,)

        self.updatemenu=MDDropdownMenu(
            caller=self.screen.ids.acs.ids.dropupdate,
            items=lst,
            width_mult=4,)

        self.updatestatusmenu=MDDropdownMenu(
            caller=self.screen.ids.acs.ids.dropstatus,
            items=lst2,
            width_mult=4,)

        var.commit()
        var.close()

    def startre(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute("select dd from data1")
        a=v.fetchall()
        tyrs=[]
        for i in a:
            b=i[0].split('-')
            if b[0] not in tyrs:
                tyrs.append(b[0])
        yrs1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrey1(x),
            } for i in tyrs]
        
        yrs2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrey2(x),
            } for i in tyrs]

        yrs3 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrey3(x),
            } for i in tyrs]

        self.rey1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropy1,
            items=yrs1,
            width_mult=4,)

        self.rey2=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropy2,
            items=yrs2,
            width_mult=4,)

        self.rey3=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropy3,
            items=yrs3,
            width_mult=4,)

        v.execute("Select a from accounts")
        aa=v.fetchall()
        aa1=[i[0] for i in aa]
        aa1.sort()

        lsta = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showreay1(x),
            } for i in aa1]

        self.reay1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropay1,
            items=lsta,
            width_mult=4,)

        tm=['January','February','March','April','May','June','July','August','September','October','November','December']
        m1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrem1(x),
            } for i in tm]

        m2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrem2(x),
            } for i in tm]
        
        self.rem1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropm1,
            items=m1,
            width_mult=4,)

        self.rem2=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropm2,
            items=m2,
            width_mult=4,)

        v.execute("select distinct(ffrom) from data1")
        first=v.fetchall()
        v.execute("select distinct(tto) from data1")
        second=v.fetchall()
        tp=['Bank of Baroda','Cash','PhonePe Wallet']
        data=[]
        for i in first:
            if i[0] not in tp and i[0] not in data:
                data.append(i[0])
            else:
                pass
        for i in second:
            if i[0] not in tp and i[0] not in data:
                data.append(i[0])
            else:
                pass

        maindata=[]
        data.sort()
        
        maindata= [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrecy1(x),
            } for i in data]

        self.recy1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropcy1,
            items=maindata,
            width_mult=5,)

        yrs4 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showremy1(x),
            } for i in tyrs]

        self.remy1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropmy1,
            items=yrs4,
            width_mult=4,)

        yrs5 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showremy2(x),
            } for i in tyrs]

        self.remy2=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropmy2,
            items=yrs5,
            width_mult=4,)
        
        mad=aa1+data
        madata1=[{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrema1(x),
            } for i in mad]

        self.needed1=aa1
        print(aa1)

        self.rema1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropma1,
            items=madata1,
            width_mult=5,)

        yrs6 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showreyy1(x),
            } for i in tyrs]

        self.reyy1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropyy1,
            items=yrs6,
            width_mult=4,)
        
        yrs7 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showreyy2(x),
            } for i in tyrs]

        self.reyy2=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropyy2,
            items=yrs7,
            width_mult=4,)

        yrs8 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrey2y1(x),
            } for i in tyrs]

        self.rey2y1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropy2y1,
            items=yrs8,
            width_mult=4,)

        yrs9 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showrey2y2(x),
            } for i in tyrs]

        self.rey2y2=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropy2y2,
            items=yrs9,
            width_mult=4,)

        madata2=[{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showreya1(x),
            } for i in mad]

        self.reya1=MDDropdownMenu(
            caller=self.screen.ids.res.ids.dropya1,
            items=madata2,
            width_mult=5,)

        
        var.commit()
        var.close()

    def startcb(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()

        v.execute('select a from accounts')
        a=v.fetchall()
        b=[i[0] for i in a]
        b.sort()
        accdata=[{'text':i} for i in b]
        accdata = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showcbacc(x),
            } for i in b]
        #accdata=[{'text':i[0]} for i in a]
        
        self.cbaccmenu=MDDropdownMenu(
            caller=self.screen.ids.cbs.ids.dropcbacc,
            items=accdata,
            width_mult=5,)

        var.commit()
        var.close()

    def startse(self):
        t = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showst(x),
            } for i in ['Light','Dark']]
        
        self.tmenu=MDDropdownMenu(
            caller=self.screen.ids.sts.ids.sdropt,
            items=t,
            width_mult=4,)

        plst=['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        plst.sort()
        p = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showsp(x),
            } for i in plst]
        
        self.pmenu=MDDropdownMenu(
            caller=self.screen.ids.sts.ids.sdropc,
            items=p,
            width_mult=4,)

    def createacc(self):
        #print("Entered createacc")
        name=self.screen.ids.acs.ids.ace.text
        if name!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()
            '''v.execute("""CREATE table accounts(id integer PRIMARY KEY,
                        a text NOT NULL,
                        s text NOT NULL)
                        """)'''
            v.execute("SELECT a from accounts")
            lst=v.fetchall()
            mlst=[]
            for i in lst:
                mlst.append(i[0])
            
            if name not in mlst:
                v.execute("INSERT INTO accounts (a,s) VALUES(:a,:s)",{
                        'a':name,
                        's':"Open",
                    })
                bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
                self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Account Created Successfully!",buttons=[bcloseeac])
                self.dialogeeac.open()
                self.screen.ids.acs.ids.ace.text=""
            else:
                bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
                self.dialogeeac=MDDialog(title="Personal Finance Manager",text="The Account already Exist for changes use Update part!",buttons=[bcloseeac])
                self.dialogeeac.open()

            var.commit()
            var.close()
        else:
            bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bcloseeac])
            self.dialogeeac.open()

    def deleteacc(self):
        #print("Entered deleteacc")
        names=str(self.screen.ids.acs.ids.acd.text)
        if names!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()

            '''v.execute(f"UPDATE accounts SET s=:ss where acc={str(names)}",{
                'ss':"Closed",
            })'''
            v.execute(f"Delete from accounts where a=\"{names}\"")
            v.execute("INSERT INTO accounts (a,s) VALUES(:a,:s)",{
                        'a':names,
                        's':"Closed",
                    })
            var.commit()
            var.close()
            bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Account Deleted!",buttons=[bcloseeac])
            self.dialogeeac.open()
            self.screen.ids.acs.ids.acd.text=""
        else:
            bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bcloseeac])
            self.dialogeeac.open()

    def updateacc(self):
        #print("Entered updateacc")
        pn=self.screen.ids.acs.ids.acu1.text
        nn=self.screen.ids.acs.ids.acu2.text
        ns=self.screen.ids.acs.ids.acus.text

        if pn!="" and nn!="" and ns!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute(f"Delete from accounts where a=\"{pn}\"")
            v.execute("INSERT INTO accounts (a,s) VALUES(:a,:s)",{
                        'a':nn,
                        's':ns,
                    })
            var.commit()
            var.close()
            self.screen.ids.acs.ids.acu1.text=""
            self.screen.ids.acs.ids.acu2.text=""
            self.screen.ids.acs.ids.acus.text=""
            bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Account is Updated Successfully!",buttons=[bcloseeac])
            self.dialogeeac.open()
            MoneyApp.startac(self)
        else:
            bcloseeac=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeeac=MDDialog(title="Personal Finance Manager",text="Invalid Inputs!",buttons=[bcloseeac])
            self.dialogeeac.open()

    def startrm(self):
        tm=['Once','Daily','Weekly']
        m1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showRMType(x),
            } for i in tm]
        
        self.rmtMenu=MDDropdownMenu(
            caller=self.screen.ids.rms.ids.dropRmt,
            items=m1,
            width_mult=5,)


    def saveReminder(self):
        var=sqlite3.connect('data.db')
        v=var.cursor()
        forr=self.screen.ids.rms.ids.forr.text
        rmt=self.screen.ids.rms.ids.rmt.text
        rmd=self.screen.ids.rms.ids.rmd.text
        amt=self.screen.ids.rms.ids.minBal.text
        narr=self.screen.ids.rms.ids.rmm.text

        # Check switch yes or no
        if self.screen.ids.rms.ids.emailSwitch.active==True:
            emails="Yes"
        else:
            emails="No"

        format = "%Y-%m-%d"
        datetime.strptime(rmd,format)
        v.execute("INSERT INTO reminder (ddate,ttype,ffor,amountt,descrip,needEmailNotif) VALUES(:dd,:tt,:ff,:aa,:nn,:em)",{
            'dd':rmd,
            'tt':rmt,
            'ff':forr,
            'aa':amt,
            'nn':narr,
            'em':emails,
        })
        
        
        bcloses=MDFlatButton(text="Close",on_release=self.closes)
        self.dialogs=MDDialog(title="Personal Finance Manager",text="Record Saved!",buttons=[bcloses])
        self.dialogs.open()

        # self.screen.ids.rms.ids.forr.text=""
        # self.screen.ids.rms.ids.rmt.text=""
        # self.screen.ids.rms.ids.rmd.text=""
        # self.screen.ids.rms.ids.minBal.text=""
        # self.screen.ids.rms.ids.rmm.text=""

        var.commit()
        var.close()

    def showacc(self):
        #print("Entered showacc")
        var=sqlite3.connect('data.db')
        v=var.cursor()
        v.execute("Select * from accounts")
        a=v.fetchall()
        #pprint(a)
        c=[("Id",dp(10)),("Account Name",dp(45)),("Status",dp(25))]
        self.tableshowacc=MDDataTable(
                        size_hint_y=None,
                        size_hint_x=None,
                        width=450,
                        height=350,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
                        column_data=c,
                        row_data=a)
        
        #self.tableshowacc.open()
        self.screen.ids.acs.add_widget(self.tableshowacc)

        var.commit()
        var.close()

    def startcc(self):
        tm=['USD','EUR','INR','CAD','GBP','AUD','JPY','BRL']
        self.dictOfCurrencies={'US Dollar':'USD','Euro':'EUR','Indian Rupee':'INR','Canadian Dollar':'CAD','British Pound':'GBP','Australian Dollar':'AUD','Japanese Yen':'JPY','Brazilian Real':'BRL'}
        #All Key values
        self.dictOfCurrenciesKeys=list(self.dictOfCurrencies.keys())
        m1 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showFFC(x),
            } for i in self.dictOfCurrenciesKeys]
        
        m2 = [{
                "text": f"{i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"{i}": self.showTTC(x),
            } for i in self.dictOfCurrenciesKeys]
        
        self.ffcMenu=MDDropdownMenu(
            caller=self.screen.ids.ccs.ids.dropffc,
            items=m1,
            width_mult=5,)
        
        self.ttcMenu=MDDropdownMenu(
            caller=self.screen.ids.ccs.ids.dropttc,
            items=m2,
            width_mult=5,)
        
    def convertCurrency(self):
        amt=self.screen.ids.ccs.ids.amt.text
        ffc=self.screen.ids.ccs.ids.ffc.text
        ttc=self.screen.ids.ccs.ids.ttc.text

        print(amt,ffc,ttc)

        if amt=="" or ffc=="" or ttc=="":
            pass
        else:
            r=requests.get(f"https://www.xe.com/currencyconverter/convert/?Amount={amt}&From={self.dictOfCurrencies[ffc]}&To={self.dictOfCurrencies[ttc]}").content
            soup = BeautifulSoup(r, "html.parser")

            a=soup.find_all("p", attrs={"class": "result__BigRate-sc-1bsijpp-1 iGrAod"})

            print(a)

            a=str(a)
            a=a.split(">")
            a=a[1].split("<")
            a=a[0]
            print(a)

            self.screen.ids.ccs.ids.res.text=a


    def clearCurrency(self):
        self.screen.ids.ccs.ids.amt.text=""
        self.screen.ids.ccs.ids.ffc.text=""
        self.screen.ids.ccs.ids.ttc.text=""
        self.screen.ids.ccs.ids.res.text=""
        

    def graphy1(self):
        y=self.screen.ids.res.ids.y1.text
        if y!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute("select dd,amt from data1")
            data=v.fetchall()

            var.commit()
            var.close()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            c=[]
            for i in range(1,13):
                nd=0
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):
                        if float(j[1])<0:
                            nd=nd+float(j[1])
                        else:
                            nc=nc+float(j[1])
                nd=float(nd)*(-1)
                d.append(nd)
                c.append(nc)

            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            x = np.arange(len(labels))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, c, width, label='Credit')
            g2 = ax.bar(x + width/2, d, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Monthly Report of Year {y}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(labels)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            mng = plt.get_current_fig_manager()
            plt.tight_layout()
            return plt.show()
        
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeere)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select the Year!",buttons=[bcloseere])
            self.dialogeere.open()

    def closetable(self):
        try:
            self.screen.ids.res.remove_widget(self.tablere1)
        except:
            pass
        try:
            self.screen.ids.res.remove_widget(self.remtable11)
        except:
            pass
        try:
            self.screen.ids.res.remove_widget(self.remtable12)
        except:
            pass
        try:
            self.screen.ids.res.remove_widget(self.tablerec)
        except:
            pass
        try:
            self.screen.ids.res.remove_widget(self.reytable1)
        except:
            pass
        try:
            self.screen.ids.res.remove_widget(self.reytable2)
        except:
            pass
        try:
            self.screen.ids.ups.remove_widget(self.tableoftypeu)
        except:
            pass
        try:
            self.screen.ids.ups.remove_widget(self.tableofallu)
        except:
            pass
        try:
            self.screen.ids.ups.remove_widget(self.tableofalltypeu)
        except:
            pass
        try:
            self.screen.ids.ups.remove_widget(self.tableofnormaldateu)
        except:
            pass
        try:
            self.screen.ids.sos.remove_widget(self.tableofnormaldate)
        except:
            pass
        try:
            self.screen.ids.sos.remove_widget(self.tableoftype)
        except:
            pass
        try:
            self.screen.ids.sos.remove_widget(self.tableofall)
        except:
            pass
        try:
            self.screen.ids.sos.remove_widget(self.tableofalltype)
        except:
            pass
        try:
            self.screen.ids.socs.remove_widget(self.soctableoftype)
        except:
            pass
        try:
            self.screen.ids.socs.remove_widget(self.soctableofalltype)
        except:
            pass
        try:
            self.screen.ids.socs.remove_widget(self.tableofall)
        except:
            pass
        try:
            self.screen.ids.acs.remove_widget(self.tableshowacc)
        except:
            pass

    def retable(self):
        y=self.screen.ids.res.ids.y1.text
        if y!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute("select dd,amt from data1")
            data=v.fetchall()

            var.commit()
            var.close()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            c=[]
            for i in range(1,13):
                nd=0
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):
                        if float(j[1])<0:
                            nd=nd+float(j[1])*(-1)
                        else:
                            nc=nc+float(j[1])
                d.append(nd)
                c.append(nc)

            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            lst=zip(labels,c,d)
            mlst=list(lst)
            #print(mlst)
            c=[("Month",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            
            self.tablere1=MDDataTable(
                        size_hint_y=None,
                        size_hint_x=None,
                        width=500,
                        height=400,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
                        column_data=c,
                        row_data=mlst,)

            #self.tablere1.open()
            """self.tablere1.create_pagination_menu(10)
            self.tablere1.table_data.open_pagination_menu()"""
            """self.screen.ids.res.add_widget(self.tablere1)
            self.screen.ids.res.remove_widget(self.tablere1)"""
            self.screen.ids.res.add_widget(self.tablere1)
            #self.tablere1.open()

            

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select the Year!",buttons=[bcloseere])
            self.dialogeere.open()

    def graphay1(self):
        y=self.screen.ids.res.ids.y2.text
        ac=self.screen.ids.res.ids.ay2.text
        if y!='' and ac!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select dd,amt from data1 where mainacc=\'{ac}\' and dc=\'Debit\'")
            data=v.fetchall()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            for i in range(1,13):
                nd=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nd=nd+float(j[1])*(-1)
                    else:
                        pass   
                        
                d.append(nd)

            v.execute(f"select dd,amt from data1 where mainacc=\'{ac}\' and dc=\'Credit\'")
            data=v.fetchall()

            data1=[]
            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            c=[]
            for i in range(1,13):
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nc=nc+float(j[1])
                    else:
                        pass    
                c.append(nc)


            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            x = np.arange(len(labels))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, c, width, label='Credit')
            g2 = ax.bar(x + width/2, d, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Monthly Report of {ac} in Year {y}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(labels)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()
        
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeere)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select Both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def retableay(self):
        y=self.screen.ids.res.ids.y2.text
        ac=self.screen.ids.res.ids.ay2.text
        if y!='' and ac!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select dd,amt from data1 where mainacc=\'{ac}\' and dc=\'Debit\'")
            data=v.fetchall()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            for i in range(1,13):
                nd=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nd=nd+float(j[1])*(-1)
                    else:
                        pass   
                        
                d.append(nd)

            v.execute(f"select dd,amt from data1 where mainacc=\'{ac}\' and dc=\'Credit\'")
            data=v.fetchall()

            data1=[]
            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            c=[]
            for i in range(1,13):
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nc=nc+float(j[1])
                    else:
                        pass    
                c.append(nc)


            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            lst=zip(labels,c,d)
            mlst=list(lst)
            print(mlst)

            var.commit()
            var.close()

            c=[("Month",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.tablere1=MDDataTable(
                        size_hint_y=None,
                        size_hint_x=None,
                        width=500,
                        height=400,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
                        column_data=c,
                        row_data=mlst)
            #self.tablere1.open()
            self.screen.ids.res.add_widget(self.tablere1)

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select Both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def graphcy1(self):
        y=self.screen.ids.res.ids.y3.text
        ac=self.screen.ids.res.ids.c3.text
        if y!='' and ac!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select dd,amt from data1 where tto=\'{ac}\' and dc=\'Debit\'")
            data=v.fetchall()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            for i in range(1,13):
                nd=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nd=nd+float(j[1])*(-1)
                    else:
                        pass   
                        
                d.append(nd)

            v.execute(f"select dd,amt from data1 where ffrom=\'{ac}\' and dc=\'Credit\'")
            data=v.fetchall()

            data1=[]
            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            c=[]
            for i in range(1,13):
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nc=nc+float(j[1])
                    else:
                        pass    
                c.append(nc)


            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            x = np.arange(len(labels))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, c, width, label='Credit')
            g2 = ax.bar(x + width/2, d, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Monthly Report of {ac} in Year {y}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(labels)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()
        
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeere)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def retablecy(self):
        y=self.screen.ids.res.ids.y3.text
        ac=self.screen.ids.res.ids.c3.text
        if y!='' and ac!='':
            var=sqlite3.connect('data.db')
            v=var.cursor()

            v.execute(f"select dd,amt from data1 where tto=\'{ac}\' and dc=\'Debit\'")
            data=v.fetchall()

            data1=[]

            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            d=[]
            for i in range(1,13):
                nd=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nd=nd+float(j[1])*(-1)
                    else:
                        pass   
                        
                d.append(nd)

            v.execute(f"select dd,amt from data1 where ffrom=\'{ac}\' and dc=\'Credit\'")
            data=v.fetchall()

            data1=[]
            for i in data:
                a=i[0].split('-')
                a=a[0]
                if a==str(y):
                    data1.append(i)

            c=[]
            for i in range(1,13):
                nc=0
                for j in data1:
                    a=j[0].split('-')
                    if float(a[1])==float(i):    
                        nc=nc+float(j[1])
                    else:
                        pass    
                c.append(nc)


            labels = ['January', 'February', 'March', 'April', 'May','June','July','August','September','October',
            'November','December']

            lst=zip(labels,c,d)
            mlst=list(lst)
            #print(mlst)

            var.commit()
            var.close()

            c=[("Month",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.tablerec=MDDataTable(
                        size_hint_y=None,
                        size_hint_x=None,
                        width=500,
                        height=400,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
                        column_data=c,
                        row_data=mlst)
            #self.tablerec.open()
            self.screen.ids.res.add_widget(self.tablerec)

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def remtable1(self):
        m=self.screen.ids.res.ids.m1.text
        y=self.screen.ids.res.ids.my1.text
        if m!="" and y!="":
            mo=[{'January':1}, {'February':2}, {'March':3}, {'April':4}, {'May':5}, {'June':6},
            {'July':7},{'August':8},{'September':9},{'October':10},{'November':11},{'December':12}]
            for i in mo:
                a=i.get(m)
                if a!=None:
                    mn=a
            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute("select dd,amt from data1")
            z=v.fetchall()

            d1=[]
            for i in z:
                ii=i[0].split('-')
                if float(ii[1])==mn and float(ii[0])==float(y):
                    d1.append(i)
                else:
                    pass

            dates=[]
            for i in d1:
                s=datetime.strptime(i[0],"%Y-%m-%d")
                if s not in dates:
                    dates.append(s)
                else:
                    pass

            fdates=[]
            for i in dates:
                dd=str(i).split(" ")
                fdates.append(dd[0])

            c=[]
            d=[]
            for i in fdates:
                nc=0
                nd=0
                for j in d1:
                    if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                        if float(j[1])<0:
                            nd=nd+float(float(j[1]*-1))
                        else:
                            nc=nc+float(j[1])
                c.append(nc)
                d.append(nd)

            var.commit()
            var.close()

            daa=zip(fdates,c,d)
            data=list(daa)
            
            c=[("Date",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.remtable11=MDDataTable(
                        size_hint_y=None,
                        size_hint_x=None,
                        width=500,
                        height=400,
                        pos_hint={'center_x':0.5,'center_y':0.62},
                        use_pagination=True,
                        column_data=c,
                        row_data=data)
            #self.remtable11.open()
            self.screen.ids.res.add_widget(self.remtable11)

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select Both the Above Fields!",buttons=[bcloseere])
            self.dialogeere.open()


    def remgraph1(self):
        m=self.screen.ids.res.ids.m1.text
        y=self.screen.ids.res.ids.my1.text
        if m!="" and y!="":
            mo=[{'January':1}, {'February':2}, {'March':3}, {'April':4}, {'May':5}, {'June':6},
            {'July':7},{'August':8},{'September':9},{'October':10},{'November':11},{'December':12}]
            for i in mo:
                a=i.get(m)
                if a!=None:
                    mn=a

            var=sqlite3.connect('data.db')
            v=var.cursor()
            v.execute("select dd,amt from data1")
            z=v.fetchall()

            d1=[]
            for i in z:
                ii=i[0].split('-')
                if float(ii[1])==mn and float(ii[0])==float(y):
                    d1.append(i)
                else:
                    pass

            dates=[]
            for i in d1:
                s=datetime.strptime(i[0],"%Y-%m-%d")
                if s not in dates:
                    dates.append(s)
                else:
                    pass

            fdates=[]
            for i in dates:
                dd=str(i).split(" ")
                fdates.append(dd[0])

            c=[]
            d=[]
            for i in fdates:
                nc=0
                nd=0
                for j in d1:
                    if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                        if float(j[1])<0:
                            nd=nd+float(float(j[1]*-1))
                        else:
                            nc=nc+float(j[1])
                c.append(nc)
                d.append(nd)

            var.commit()
            var.close()

            x = np.arange(len(fdates))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, c, width, label='Credit')
            g2 = ax.bar(x + width/2, d, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Daily Report of {m} in Year {y}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(fdates)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select Both the Above Fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def remtable2(self):
        m=self.screen.ids.res.ids.m2.text
        y=self.screen.ids.res.ids.my2.text
        aa=self.screen.ids.res.ids.ma1.text

        if m!="" and y!="" and aa!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()

            mo=[{'January':1}, {'February':2}, {'March':3}, {'April':4}, {'May':5}, {'June':6},
            {'July':7},{'August':8},{'September':9},{'October':10},{'November':11},{'December':12}]
            for i in mo:
                a=i.get(m)
                if a!=None:
                    mn=a

            if aa in self.needed1:
                v.execute(f"select dd,amt,id from data1 where mainacc=\"{aa}\" and dc=\"Debit\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt,id from data1 where mainacc=\"{aa}\" and dc=\"Credit\"")
                c1=v.fetchall()
            else:
                v.execute(f"select dd,amt,id from data1 where tto=\"{aa}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt,id from data1 where ffrom=\"{aa}\"")
                c1=v.fetchall()

            ddata1=[]
            cdata1=[]

            for i in d1:
                a=i[0].split('-')
                if int(a[0])==int(y) and int(a[1])==int(mn):
                    ddata1.append(i)

            for i in c1:
                a=i[0].split('-')
                if int(a[0])==int(y) and int(a[1])==int(mn):
                    cdata1.append(i)
            
            #print(ddata1+cdata1)
            i1=[]
            for i in cdata1:
                i1.append(i[2])
            for i in ddata1:
                i1.append(i[2])
            i1.sort()
            #print(i1)

            iddd=[]
            demo=cdata1+ddata1
            for i in i1:
                for j in demo:
                    if int(i)==j[2]:
                        iddd.append(j[0])
            #print(iddd)

            dates=[]
            for i in iddd:
                s=datetime.strptime(i,"%Y-%m-%d")
                if s not in dates:
                    dates.append(s)
                else:
                    pass
            #print(dates)

            fdates=[]
            for i in dates:
                dd=str(i).split(" ")
                fdates.append(dd[0])
            #print(fdates)'

            fd1=[]
            fc1=[]
            for i in fdates:
                nd=0
                nc=0
                for j in demo:
                    if j[1]<0:
                        if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                            nd=nd+float(float(j[1]*-1))
                    else:
                        if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                            nc=nc+float(j[1])
                fd1.append(nd)
                fc1.append(nc)

            #print(fd1,fc1)

            sd1=zip(fdates,fc1,fd1)
            sd2=list(sd1)

            c=[("Date",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.remtable12=MDDataTable(
                    size_hint_y=None,
                    size_hint_x=None,
                    width=500,
                    height=400,
                    pos_hint={'center_x':0.5,'center_y':0.62},
                    use_pagination=True,
                    column_data=c,
                    row_data=sd2)
            #self.remtable12.open()
            var.commit()
            var.close()

            self.screen.ids.res.add_widget(self.remtable12)
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select All the above Three Fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def remgraph2(self):
        m=self.screen.ids.res.ids.m2.text
        y=self.screen.ids.res.ids.my2.text
        aa=self.screen.ids.res.ids.ma1.text

        if m!="" and y!="" and aa!="":
            var=sqlite3.connect('data.db')
            v=var.cursor()

            mo=[{'January':1}, {'February':2}, {'March':3}, {'April':4}, {'May':5}, {'June':6},
            {'July':7},{'August':8},{'September':9},{'October':10},{'November':11},{'December':12}]
            for i in mo:
                a=i.get(m)
                if a!=None:
                    mn=a

            if aa in self.needed1:
                v.execute(f"select dd,amt,id from data1 where mainacc=\"{aa}\" and dc=\"Debit\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt,id from data1 where mainacc=\"{aa}\" and dc=\"Credit\"")
                c1=v.fetchall()
            else:
                v.execute(f"select dd,amt,id from data1 where tto=\"{aa}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt,id from data1 where ffrom=\"{aa}\"")
                c1=v.fetchall()

            ddata1=[]
            cdata1=[]

            for i in d1:
                a=i[0].split('-')
                if int(a[0])==int(y) and int(a[1])==int(mn):
                    ddata1.append(i)

            for i in c1:
                a=i[0].split('-')
                if int(a[0])==int(y) and int(a[1])==int(mn):
                    cdata1.append(i)
            
            #print(ddata1+cdata1)
            i1=[]
            for i in cdata1:
                i1.append(i[2])
            for i in ddata1:
                i1.append(i[2])
            i1.sort()
            #print(i1)

            iddd=[]
            demo=cdata1+ddata1
            for i in i1:
                for j in demo:
                    if int(i)==j[2]:
                        iddd.append(j[0])
            #print(iddd)

            dates=[]
            for i in iddd:
                s=datetime.strptime(i,"%Y-%m-%d")
                if s not in dates:
                    dates.append(s)
                else:
                    pass
            #print(dates)

            fdates=[]
            for i in dates:
                dd=str(i).split(" ")
                fdates.append(dd[0])
            #print(fdates)

            fd1=[]
            fc1=[]
            for i in fdates:
                nd=0
                nc=0
                for j in demo:
                    if j[1]<0:
                        if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                            nd=nd+float(float(j[1]*-1))
                    else:
                        if datetime.strptime(j[0],"%Y-%m-%d")==datetime.strptime(i,"%Y-%m-%d"):
                            nc=nc+float(j[1])
                fd1.append(nd)
                fc1.append(nc)

            var.commit()
            var.close()

            x = np.arange(len(fdates))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, fc1, width, label='Credit')
            g2 = ax.bar(x + width/2, fd1, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Daily Report of {aa} in {m} of Year {y}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(fdates)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select All the above Three Fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def retableyy1(self):
        y1=self.screen.ids.res.ids.yy1.text
        y2=self.screen.ids.res.ids.yy2.text

        if y1!="" and y2!="" and int(y2)>=int(y1):
            var=sqlite3.connect("data.db")
            v=var.cursor()

            v.execute("select dd,amt from data1")
            data1=v.fetchall()

            data2=[]
            for i in data1:
                a=i[0].split('-')
                if int(a[0])>=int(y1) and int(a[0])<=int(y2):
                    data2.append(i)

            y3=int(y2)+1
            lst=[i for i in range(int(y1),int(y3))]

            dc=[]
            dd=[]

            for i in lst:
                c=0
                d=0
                for j in data2:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])>0:
                            c=c+float(j[1])
                        else:
                            d=d+float(float(j[1])*-1)
                dc.append("{:.2f}".format(c))
                dd.append("{:.2f}".format(d))

            show=zip(lst,dc,dd)
            showdata=list(show)

            c=[("Year",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.reytable1=MDDataTable(
                    size_hint_y=None,
                    size_hint_x=None,
                    width=500,
                    height=400,
                    pos_hint={'center_x':0.5,'center_y':0.62},
                    use_pagination=True,
                    column_data=c,
                    row_data=showdata)
            #self.reytable1.open()

            var.commit()
            var.close()
            self.screen.ids.res.add_widget(self.reytable1)

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def graphyy1(self):
        y1=self.screen.ids.res.ids.yy1.text
        y2=self.screen.ids.res.ids.yy2.text

        if y1!="" and y2!="" and int(y2)>=int(y1):
            var=sqlite3.connect("data.db")
            v=var.cursor()

            v.execute("select dd,amt from data1")
            data1=v.fetchall()

            data2=[]
            for i in data1:
                a=i[0].split('-')
                if int(a[0])>=int(y1) and int(a[0])<=int(y2):
                    data2.append(i)

            y3=int(y2)+1
            lst=[i for i in range(int(y1),int(y3))]

            dc=[]
            dd=[]

            for i in lst:
                c=0
                d=0
                for j in data2:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])>0:
                            c=c+float(j[1])
                        else:
                            d=d+float(float(j[1])*-1)
                dc.append(c)
                dd.append(d)

            var.commit()
            var.close()

            x = np.arange(len(lst))  # the label locations
            width = 0.45  # the width of the bars

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, dc, width, label='Credit')
            g2 = ax.bar(x + width/2, dd, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Year Report from {y1} to {y2}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(lst)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()
        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select both the above fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def reyytable1(self):
        y1=self.screen.ids.res.ids.y2y1.text
        y2=self.screen.ids.res.ids.y2y2.text
        acc=self.screen.ids.res.ids.ya1.text

        if y1!="" and y2!="" and acc!="" and int(y2)>=int(y1):
            var=sqlite3.connect("data.db")
            v=var.cursor()

            if acc in self.needed1:
                v.execute(f"select dd,amt from data1 where mainacc=\"{acc}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt from data1 where mainacc=\"{acc}\"")
                c1=v.fetchall()
            else:
                v.execute(f"select dd,amt from data1 where tto=\"{acc}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt from data1 where ffrom=\"{acc}\"")
                c1=v.fetchall()

            var.commit()
            var.close()

            y3=int(y2)+1
            lst=[i for i in range(int(y1),int(y3))]

            d11=[]
            for i in lst:
                n=0
                for j in d1:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])<0:
                            n=n+float(float(j[1]*-1))
                d11.append("{:.2f}".format(n))


            c11=[]
            for i in lst:
                n=0
                for j in c1:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])>0:
                            n=n+float(j[1])
                c11.append("{:.2f}".format(n))

            print(c11,d11)

            show=zip(lst,c11,d11)
            showdata=list(show)

            c=[("Year",dp(30)),("Credit",dp(30)),("Debit",dp(30))]
            self.reytable2=MDDataTable(
                    size_hint_y=None,
                    size_hint_x=None,
                    width=500,
                    height=400,
                    pos_hint={'center_x':0.5,'center_y':0.62},
                    use_pagination=True,
                    column_data=c,
                    row_data=showdata)
            #self.reytable2.open()
            self.screen.ids.res.add_widget(self.reytable2)

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select All the above Three Fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def reyygraph1(self):
        y1=self.screen.ids.res.ids.y2y1.text
        y2=self.screen.ids.res.ids.y2y2.text
        acc=self.screen.ids.res.ids.ya1.text

        if y1!="" and y2!="" and acc!="" and int(y2)>=int(y1):
            var=sqlite3.connect("data.db")
            v=var.cursor()

            if acc in self.needed1:
                v.execute(f"select dd,amt from data1 where mainacc=\"{acc}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt from data1 where mainacc=\"{acc}\"")
                c1=v.fetchall()
            else:
                v.execute(f"select dd,amt from data1 where tto=\"{acc}\"")
                d1=v.fetchall()
                v.execute(f"select dd,amt from data1 where ffrom=\"{acc}\"")
                c1=v.fetchall()

            var.commit()
            var.close()

            y3=int(y2)+1
            lst=[i for i in range(int(y1),int(y3))]

            d11=[]
            for i in lst:
                n=0
                for j in d1:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])<0:
                            n=n+float(float(j[1]*-1))
                d11.append(n)


            c11=[]
            for i in lst:
                n=0
                for j in c1:
                    a=j[0].split('-')
                    if int(a[0])==int(i):
                        if float(j[1])>0:
                            n=n+float(j[1])
                c11.append(n)

            print(c11,d11)

            x = np.arange(len(lst))
            width = 0.45

            fig, ax = plt.subplots()
            g1 = ax.bar(x - width/2, c11, width, label='Credit')
            g2 = ax.bar(x + width/2, d11, width, label='Debit')
            ax.set_ylabel('Rupees')
            ax.set_title(f'Year Report of {acc} from {y1} to {y2}')
            ax.set_xticks(x)
            plt.xticks(rotation=45)
            ax.set_xticklabels(lst)

            def autolabel(rects):
                for rect in rects:
                    height = rect.get_height()
                    ax.annotate('{}'.format(height),
                                xy=(rect.get_x() + rect.get_width() / 2, height+2),
                                xytext=(0, 3),
                                textcoords="offset points",
                                ha='center', va='bottom')

            autolabel(g1)
            autolabel(g2)

            ax.legend()
            plt.tight_layout()
            return plt.show()

        else:
            bcloseere=MDFlatButton(text="Close",on_release=self.closeeac)
            self.dialogeere=MDDialog(title="Personal Finance Manager",text="Select All the above Three Fields!",buttons=[bcloseere])
            self.dialogeere.open()

    def checkaccbalance(self):
        acc=self.screen.ids.cbs.ids.cbacc.text
        if acc!="":
            var=sqlite3.connect("data.db")
            v=var.cursor()

            v.execute(f'select sum(amt) from data1 where mainacc=\"{acc}\"')
            ans=v.fetchall()[0][0]

            if ans==None:
                ans=0
            
            ans="{:.2f}".format(ans)
            
            bcloseecb=MDFlatButton(text="Close",on_release=self.closeecb)
            self.dialogeecb=MDDialog(title="Personal Finance Manager",text=f"Balance of {acc} = {ans}",buttons=[bcloseecb])
            self.dialogeecb.open()

            var.commit()
            var.close()
        else:
            bcloseecb=MDFlatButton(text="Close",on_release=self.closeecb)
            self.dialogeecb=MDDialog(title="Personal Finance Manager",text="Select the Account Name!",buttons=[bcloseecb])
            self.dialogeecb.open()

    def displaysetting(self):
        #['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
        stt=self.screen.ids.sts.ids.stt.text
        stc=self.screen.ids.sts.ids.stc.text

        if stt!="":self.t=stt
        if stc!="":self.p=stc

        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = self.t
        self.theme_cls.primary_palette = self.p
        self.theme_cls.accent_palette = self.p

        var=sqlite3.connect("data.db")
        v=var.cursor()
        v.execute("delete from color;")
        v.execute("INSERT INTO color (theme,palette) VALUES(:t,:p)",{'t':stt,'p':stc})
        var.commit()
        var.close()


        '''self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Light"'''
        #self.screen.ids.sts.ids.apply.text_color = "Red"
        
        #self.screen=Builder.load_string(screen_helper)

    def closeecb(self,obj):
        try:
            self.dialogeecb.dismiss()
        except:
            pass

    def closeeac(self,obj):
        try:
            self.dialoge.dismiss()
        except:
            pass

    def closee(self,obj):
        try:
            self.dialogeeac.dismiss()
        except:
            pass

    def closes(self,obj):
        try:
            self.dialogs.dismiss()
        except:
            pass

    def closeed(self,obj):
        try:
            self.dialogeed.dismiss()
        except:
            pass

    def closesd(self,obj):
        try:
            self.dialogsd.dismiss()
        except:
            pass

    def closeeu(self,obj):
        try:
            self.dialogsu.dismiss()
        except:
            pass

    def closesu(self,obj):
        try:
            self.dialogsu.dismiss()
        except:
            pass

    def closeere(self,obj):
        try:
            self.dialogeere.dismiss()
        except:
            pass

    def show_text3(self,word):
        self.screen.ids.ens.ids.entt.text=word

    def show_textnamenu(self,a):
        self.screen.ids.sos.ids.normaltype.text=a

    def socshow_textnamenu(self,a):
        self.screen.ids.socs.ids.socnormaltype.text=a

    def show_textalltypemenu(self,b):
        self.screen.ids.sos.ids.alltype.text=b

    def show_text1(self,word):
        self.screen.ids.ens.ids.enf.text=word

    def socshow_textalltypemenu(self,b):
        self.screen.ids.socs.ids.socalltype.text=b

    def deletemenushow(self,b):
        self.screen.ids.acs.ids.acd.text=b

    def updatemenushow(self,b):
        self.screen.ids.acs.ids.acu1.text=b
        self.screen.ids.acs.ids.acu2.text=b

    def updatestatusmenushow(self,b):
        self.screen.ids.acs.ids.acus.text=b

    def showrey1(self,a):
        self.screen.ids.res.ids.y1.text=a
        
    def showrey2(self,a):
        self.screen.ids.res.ids.y2.text=a

    def showreay1(self,a):
        self.screen.ids.res.ids.ay2.text=a

    def showrey3(self,a):
        self.screen.ids.res.ids.y3.text=a

    def showrecy1(self,a):
        self.screen.ids.res.ids.c3.text=a

    def showrem1(self,a):
        self.screen.ids.res.ids.m1.text=a

    def showremy1(self,a):
        self.screen.ids.res.ids.my1.text=a

    def showrem2(self,a):
        self.screen.ids.res.ids.m2.text=a

    def showremy2(self,a):
        self.screen.ids.res.ids.my2.text=a

    def showrema1(self,a):
        self.screen.ids.res.ids.ma1.text=a

    def showreyy1(self,a):
        self.screen.ids.res.ids.yy1.text=a

    def showreyy2(self,a):
        self.screen.ids.res.ids.yy2.text=a

    def showrey2y1(self,a):
        self.screen.ids.res.ids.y2y1.text=a

    def showrey2y2(self,a):
        self.screen.ids.res.ids.y2y2.text=a

    def showreya1(self,a):
        self.screen.ids.res.ids.ya1.text=a
    
    def show_textnamenuu22(self,a):
        self.screen.ids.ups.ids.uu1.text=a

    def showcbacc(self,a):
        self.screen.ids.cbs.ids.cbacc.text=a

    def showst(self,a):
        self.screen.ids.sts.ids.stt.text=a
    
    def showsp(self,a):
        self.screen.ids.sts.ids.stc.text=a  

    def showRMType(self,a):
        self.screen.ids.rms.ids.rmt.text=a

    def showFFC(self,a):
        self.screen.ids.ccs.ids.ffc.text=a  

    def showTTC(self,a):
        self.screen.ids.ccs.ids.ttc.text=a  



MoneyApp().run()
#elevator-down
#gamepad-circle-down
#menu-down
#menu-down-outline
#gamepad-down