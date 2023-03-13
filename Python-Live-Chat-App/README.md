# Python Live Chad Chat App

## Summary:

Project uses HTML/Javascript/CSS Frontend, Python, Flask+ socketIO backend, to create a simple app with multiple chatrooms you can join each using their own socket server, each with their own logs/ID's

<p align="center">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/homepage.jpg"</center>  
</p>

Each room you create gives you a 4 digit code you can input on the home page to join the room with any number of people.

<p align="center">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/ChatChatRoom.jpg"</center>  
</p>

Messages are saved, even if you leave the room or refresh page.

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/ChadChatFiles.jpg"</left>  
</p>

## Code ExplanASeans:

Import Modules: <br/>
from flask import Flask, render_template, request, session, redirect, url_for <br/>
from flask_socketio import join_room, leave_room, send, SocketIO <br/>
import random <br/>
from string import ascii_uppercase <br/>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/1GenerateCode.jpg"</left>  
</p>

Creates a room code of all randomly selected capital letters 4 characters long.

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/2Home2.jpg"</left>  
</p>

Line 23, @app.route.. #uses decorater syntax creates the route for the homepage("/") using the methods of "POST"(posts data) and "GET" <br/>
Line 25, clears any remaining data from previous sessions <br/>
Line 26-28, gets data from the form submission and uses it for this session, typed in "name" or "code" which is then used on the room page <br/>
Line 29-30, Will check to see which button is pressed("POST" request) if given a "null/no response" it will default to False <br/>
Line 32-33, if no name input, will give you an error message if you forget to input a name <br/>
Line 35-36, If join is pressed and if you don't enter a code, will return to home and give you an error message asking for a code <br/>
Line 38, takes the room code as input <br/>
Line 39-43,if create is pressed they will create a new room with new code, if they have a name and room code, but it doesn't exist will give error <br/>
Line 41, Creates a members count dictionary, and a list for messages that will get filled in <br/>
Line 45-46, saves name and room in the session that is stored on server in case they refresh or send another request <br/>
Line 47, returns the redirect for the room they are joining <br/>
Line 49, return render_template("home.html") #Renders the homepage located in the templates file <br/>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/3Room.jpg"</left>  
</p>

Line 51, @app.route("/room") routes to the room.html in the templates folder
Line 52, Room Function
Line 53-54, Session checks for room, ensures you filled out the home page form and input a name, or if the room has not been created, you can't join
Line 55, returns redirect for home if you are missing some information so you can't just join /room
Line 57, renders room.html with 4 character code as room name, 

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/4Message.jpg"</left>  
</p>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/5Connect.jpg"</left>  
</p>


<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/6Disconnect.jpg"</left>  
</p>

Disconnect function 
and finally, the webserver initialization
