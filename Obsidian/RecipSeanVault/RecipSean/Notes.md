I need to figure out how I'm going to build this project before I can get https://v0.dev/chat to design the app -
I know I want a search feature for the ingredients list, but how am I setting up the DB? I'll be the only one using it, so it doesn't need to scale
SQL? NoSQL? GraphQL? MongoDB? just use JSON? What about Schema? How is the app going to read each recipe?
Should I get an API to just populate the DB? or build from scratch?

What does each recipe need? ID / Core Ingredients / Embellishments / Utensils /  times in bold / Multiple languages dropdown instructions - how will I get the app to view these correctly / Pictures? / Favorites? / 

Search Feature - Ingredients list - or by name

English + Slovak + Japanese? how will that work?

Do I want most frequently clicked? this would require a dynamic count which means DB
or it won't work on vercel - Could just add a 'Favorites' option in the schema
