from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="12345",
    database="DB"
)
my_cursor = mydb.cursor()
