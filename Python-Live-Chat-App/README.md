# Python Live Chad Chat App

## Summary:

Project uses HTML/Javascript/CSS Frontend, Python, Flask+ socketIO backend, to create a simple app with multiple chatrooms you can join each using their own socket server, each with their own logs/ID's. <br/>

<p align="center">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/homepage.jpg"</center>  
</p>

Each room you create gives you a 4 digit code you can input on the home page to join the room with any number of people. <br/>

<p align="center">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/ChatChatRoom.jpg"</center>  
</p>

Messages are saved, even if you leave the room or refresh page. <br/>

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

Creates a room code of all randomly selected capital letters 4 characters long. <br/>

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

Line 51, @app.route("/room") routes to the room.html in the templates folder <br/>
Line 52, Room Function <br/>
Line 53-54, Session checks for room, ensures you filled out the home page form and input a name, or if the room has not been created, you can't join <br/>
Line 55, returns redirect for home if you are missing some information so you can't just join /room <br/>
Line 57, renders room.html with 4 character code as room name, messages=rooms.. saves messages so aren't lost if you refresh room  <br/>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/4Message.jpg"</left>  
</p>
Line 59, decorater syntax, listens for message, receives from user session and sends from server transmitted to everyone else <br/>
Line 60, message function <br/>
Line 61, Gets room user message is from <br/>
Line 62-63, If room doesn't exist, returns(does nothing) <br/>
Line 65-68, Gets name of user sending message and message payload and saves as content variable <br/>
Line 69, sends message in content variable to room html from server <br/>
Line 70, appends message content onto the room html <br/>
Line 71, prints a message to the server console logs for debugging, stored in ram not a database <br/>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/5Connect.jpg"</left>  
</p>
Line 73, socketio listens for a "connect" <br/>
Line 74, connect function, with auth parameter(unused) <br/>
Line 75-76, looks for users name and room in the session <br/>
Line 77-78, checks if they do have a room and a name, if not they will leave <br/>
line 79-80, if the room you attempted to join is not in the rooms dictionary, you will leave <br/>
Line 83, after the first 2 checks, we know they have a name and a working room, so we will join the room <br/>
Line 84, sends a JSON message to chat room that user has joined <br/>
Line 85, add a member to the member count <br/>
Line 86, prints a string to server for debugging <br/>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/6Disconnect.jpg"</left>  
</p>

Line 88, @app decorater syntax on disconnect <br/>
Line 89, Disconnect function <br/>
Line 90-91, Gets room and name from user session <br/>
Line 92, users leaves the room <br/>
Line 93-97, Checks for the room in rooms dictionary, subtracts a member, if the member count is equal to or less than zero, deletes room <br/>
Line 99, sends a message to the room <br/>
Line 100, sends a print message to server console for debugging <br/>
Line 103, and finally, the webserver initialization <br/>
