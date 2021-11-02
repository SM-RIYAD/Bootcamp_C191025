import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
import smtplib

import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
import yaml
from db_connection import get_database_connection


st.set_page_config(
    page_title="Admission Form",
    page_icon=":sunny:",
    # layout="wide",
     initial_sidebar_state="expanded",
)

cursor, db = get_database_connection()

# cursor.execute("SHOW DATABASES")
 
# databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
 
# cursor.execute('''CREATE TABLE details (id varchar(255),
#                                               studentname varchar(255),
#                                               re_date date,
# 												status varchar(255), Phone_no int,email varchar(255) ,institution varchar(255))''')
# cursor.execute("Select * from details")
# tables = cursor.fetchall()
# # st.write(tables)
def regform():
    id=uuid4()
    id=str(id)[:10]
    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        re_date=st.date_input('Registration Date')
        status='In Progress'
        phone_no=st.text_input('Phone Number')
        email=st.text_input('Email')
        institution =st.text_input('Institution')
        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO details (id,studentname,
                                                re_date,status,phone_no,email,institution) VALUES ('{id}','{sname}',
                                                '{re_date}','{status}','{phone_no}','{ email}','{institution}')'''
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.code(id)
            st.warning("Please Store this code!!!")  
def admin():
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
 
    if st.session_state.login==True:
        if username=="admin" and password=='adpass':
            st.sidebar.success('Login Success')

            date1=st.date_input('Date1')
            date2=st.date_input('Date2')
            cursor.execute(f"select * from details where re_date between '{date1}' and '{date2}'")
            # db.commit()
            tables =cursor.fetchall()
            # st.write(tables)
            for i in tables:
                # st.text('Name:')
                st.write('Name:',i[1])
                # st.text('Institution:')
                st.write('ID: ',i[0])
                # st.text('Registration date:')
                st.write('Phone no: ',i[4])
                # st.text('Current status:')
                st.write('Email: ',i[5])
                st.write('Institution',i[6])
                st.write('Current status:',i[3])
                st.write('Registration date:',i[2])
                Accept=st.button('Accept',key=i[0])
                  
                if Accept:
                    st.success('Accepted')
                    cursor.execute(f"Update details set status='Accepted' where id='{i[0]}'")
                    db.commit()
                Reject=st.button('Reject',key=i[0])
                if Reject:
                    st.warning('Rejected')
                    cursor.execute(f"Update details set status='Rejected' where id='{i[0]}'")
                    db.commit()
                 



def info():
    id=st.text_input('Your Code')
    Submit=st.button(label='Search')
    if Submit:
    	cursor.execute(f"select * from details where id='{id}'")
    	table = cursor.fetchall()
    st.write(table)
                 
def stat():
    id=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select status from details where id='{id}'")
        table=cursor.fetchall()
        # st.write(table)
        for i in table:
                 st.text('Current Status:')
                 st.info(i[0])      

def main():
    st.title('Diploma in Data Science Admission')
    selected=st.sidebar.selectbox('Select',
                        ('-----------',
                        'Admin',
                        'Registration',
                        'Information',
                        'Status'
                        ))
   

    if selected=='Admin':
         admin()
    elif selected=='Registration':
         regform()
    elif selected=='Information':
        info()
    elif selected=='Status':
       stat()
if __name__=='__main__':
    main()

