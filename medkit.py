#connection set up
import mysql.connector as sqltor
con=sqltor.connect(host="",user="root", password="codetime",database="MedKit")
if con.is_connected():
    print('''Welcome to MedKit!
Your kit to a healthy life.''')

cur=con.cursor()

import sys

#Main menu
def main_menu(p_id,city):
    print('''1.Book an appointment
2.Book a test
3.Order medicines
4.Quit''')

    task=int(input("Enter your choice: "))

    #1.Booking an appointment
    if task==1:
        cur.execute("select distinct(Speciality)from Doctors order by Speciality")
        splist=cur.fetchall()
        for sp in splist:
            print(sp)                
        speciality=input("Choose speciality: ")        
        spchoose="select D_Id,FName,Sname,Clinic_Address,Fees from Doctors where Speciality='{}' and City='{}'".format(speciality,city)        
        cur.execute(spchoose)
        drdetails=cur.fetchall()        
        if cur.rowcount>0:
            print("   Id           Name                Address       Fees")
            for det in drdetails:
                print(det)                
            drchoice=input("Enter the Id of the Doctor: ")
            cur.execute("select D_Id from Doctors where Speciality='{}' and City='{}' and D_Id={}".format(speciality,city,drchoice))        
            cur.fetchall()
            if cur.rowcount>0:
                drdate=input("Preferred date in yyyy/mm/dd format: ")
                drtime=int(input("Time in HHMMSS format"))
                a_id="select max(Appt_Id) from Dr_Appt"
                cur.execute(a_id)
                x=cur.fetchone()
                if x[0]==None:
                    Appt_Id=10000000
                else:
                    Appt_Id=x[0]+1
                dappt="insert into Dr_Appt values({},{},{},curdate(),curtime(),'{}',{})".format(Appt_Id,drchoice,p_id,drdate,drtime)
                cur.execute(dappt)
                con.commit()
                print("Your appointment is booked and your Appointment_Id is ",Appt_Id)

            else:
                sys.stderr.write("Oops!No match found.")
                print('\n')
        else:
            sys.stderr.write("Oops!No match found.")
            print('\n')


    #2.Booking a test
    elif task==2:    
        cur.execute("select distinct Tests.T_Code, T_Name, Price from Tests,Centres where Centres.City='{}' and Tests.T_Code=Centres.T_Code".format(city))
        tlist=cur.fetchall()
        if cur.rowcount>0:
            print("  Code    Name   Price")
            for t in tlist:
                print(t)    
            tchoice=input("Enter the Test code: ")
            clist="select C_Code,C_Name,Address from Centres where T_Code={}".format(tchoice)
            cur.execute(clist)
            clist=cur.fetchall()
            if cur.rowcount>0:
                print("  Code      Name         Address")
                for c in clist:
                    print(c)
                cchoice=input("Enter the Centre code: ")
                cur.execute("select C_Code from Centres where C_Code='{}' and T_Code={}".format(cchoice,tchoice))
                cur.fetchall()
                if cur.rowcount>0:
                    tdate=input("Preferred date in yyyy/mm/dd format: ")
                    ttime=int(input("Time in HHMMSS format: "))
                    b_id="select max(Book_Id) from T_Book"
                    cur.execute(b_id)
                    x=cur.fetchone()
                    if x[0]==None:
                        Appt_Id=100000000
                    else:
                        Appt_Id=x[0]+1
                    tappt="insert into T_Book values({},{},'{}',{},curdate(),curtime(),'{}',{})".format(Appt_Id,p_id,cchoice,tchoice,tdate,ttime)
                    cur.execute(tappt)
                    con.commit()
                    print("Your booking is confirmed and your Booking id is ",Appt_Id)
                else:
                    sys.stderr.write("Oops!No match found.")
            else:
                sys.stderr.write("Oops!No match found.")
        else:
            sys.stderr.write("Oops!No match found.")


    #3.Ordering Medicines
    elif task==3:
        count=0
        tamount=0
        flag=0
        tid=[]
        bill=[]
        while True:
            amount=0
            head=("Code", "Name", "Price")
            print(head)
            cur.execute("select M_Code,M_Name,Price from Medicines order by M_Name")
            mlist=cur.fetchall()
            for m in mlist:
                print(m)
            med=input("Medicine name/code: ")            
            cur.execute("select M_Code,M_Name,Price from Medicines where M_Name='{}' or M_Code='{}'".format(med,med))
            m=cur.fetchone()
            if cur.rowcount>0:
                count+=1
                mcode=m[0]
                mname=m[1]
                price=m[2]
                
                n=int(input("Quantity: "))
                cur.execute("select max(OrderId) from MedOrder")
                x=cur.fetchone()
                if x[0]==None:
                    o_id=1000000000
                else:
                    o_id=x[0]+1
                order="insert into MedOrder values({},{},curdate(),{},{},{},Units*Price)".format(o_id,p_id,mcode,n,price)
                cur.execute(order)
                con.commit()                
                flag=1
                amount=price*n
                print("This medicine will cost Rs.",amount)
                tid.append(o_id)
                temp=[count,mname,n,price,amount]
                bill.append(temp)
                tamount+=price*n
                
            else:
                sys.stderr.write("Oops!No match found.")
                print('\n')
            print('''1.Continue ordering
2.Exit''')
            mchoice=int(input("Enter your choice:" ))

            if mchoice==1:
                pass
            elif mchoice==2:
                if flag==1:
                    print('''            MEDKIT
   YOUR KIT TO A HEALTHY LIFE
Order id(s):{}
S.no.   Name   Qty. Price  Amount'''.format(tid))
                    for item in bill:
                        print(item)
                    print("Your order for ",count," medicines amounting to Rs.",tamount," is confirmed.")
                    print('''         Thanks for ordering!
      Wishing you a speedy recovery!''')
                break
            else:
                sys.stderr.write("Invalid Choice")
                pass
       
    #4.Quit
    elif task==4:
        pass

    #Invalid option
    else:
        sys.stderr.write("Invalid option")


#__main__
#Log in
print('''1.Sign In using Username & Password
2.Sign in using OTP
3.Sign Up''')
login=int(input("Enter your choice: "))
flag=0

#1.Sign in
if login==1:   
    for attempt in range(3):
        username=input("Username: ")
        password=input("Password: ")
        check="select 'Welcome Back!',FName,SName from Patients where Username='{}' and Password='{}'".format(username,password)
        cur.execute(check)
        welcome=cur.fetchall()
        if cur.rowcount>0:
            print(welcome)
            flag=1
            generate="select P_Id,City from Patients where Username='{}' and Password='{}'".format(username,password)
            break
        else:
            sys.stderr.write("Incorrect Username or Password")
            print('\n')

    else:
        sys.stderr.write("Access Denied")

elif login==2:
    import random
    no=int(input("Enter your phone no: "))
    cur.execute("select Contact_no from Patients where Contact_no={}".format(no))
    cur.fetchone()
    if cur.rowcount>0:            
        otp=random.randint(1000,9999)
        print(otp)
        otp1=int(input("Enter the OTP: "))
        if otp1==otp:
            cur.execute("select 'Welcome Back!',FName,SName from Patients where Contact_no={}".format(no))
            welcome=cur.fetchall()
            print(welcome)
            flag=1
            generate="select P_Id,City from Patients where Contact_no={}".format(no)
        else:
            sys.stderr.write('''Incorrect OTP
Access Denied''')                
    else:
        sys.stderr.write("Oops!Your number has not been registered.")            
            

#2.Sign up
elif login==3:
    fname=input("First name: ")
    sname=input("Surname: ")
    dob=input("DOB in yyyy/mm/dd format: ")
    contact_no=int(input("Contact no: "))
    address=input("Address: ")
    city=input("City: ")
    state=input("State: ")
    pincode=int(input("Pincode: "))
    uname=input("Username: ")
    pwd=input("Password: ")
    idn="select max(P_Id) from Patients"
    cur.execute(idn)
    x=cur.fetchone()
    if x[0]==None:
        p_id=1000000
    else:
        p_id=x[0]+1
    details="insert into Patients values({},'{}','{}','{}',curdate(),'{}','{}','{}','{}',{},'{}','{}')".format(p_id,fname,sname,dob,contact_no,address,city,state,pincode,uname,pwd)
    cur.execute(details)
    con.commit()
    print("Thanks for signing up!")

    main_menu(p_id,city)

#Invalid option
else:
    sys.stderr.write("Invalid option")


#After signing in successfully 
if flag==1:        
    cur.execute(generate)
    x=cur.fetchone()
    p_id=x[0]
    city=x[1]
    main_menu(p_id,city)
