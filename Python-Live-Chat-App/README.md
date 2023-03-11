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

Import Modules:

from flask import Flask, render_template, request, session, redirect, url_for

from flask_socketio import join_room, leave_room, send, SocketIO

import random

from string import ascii_uppercase

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/1GenerateCode.jpg"</left>  
</p>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/2Home2.jpg"</left>  
</p>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/3Room.jpg"</left>  
</p>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/4Message.jpg"</left>  
</p>

<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/5Connect.jpg"</left>  
</p>


<p align="left">  
<img src="https://github.com/evilusean/Pysean/blob/main/Python-Live-Chat-App/static/Images/6Disconnect.jpg"</left>  
</p>

