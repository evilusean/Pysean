I need to figure out how I'm going to build this project before I can get https://v0.dev/chat to design the app -
I know I want a search feature for the ingredients list, but how am I setting up the DB? I'll be the only one using it, so it doesn't need to scale
SQL? NoSQL? GraphQL? MongoDB? just use JSON? What about Schema? How is the app going to read each recipe?
Should I get an API to just populate the DB? or build from scratch?

What does each recipe need? ID / Core Ingredients / Embellishments / Utensils /  times in bold / Multiple languages dropdown instructions - how will I get the app to view these correctly / Pictures? / Favorites? / 

Search Feature - Ingredients list - or by name

English + Slovak + Japanese? how will that work?

Do I want most frequently clicked? this would require a dynamic count which means DB
or it won't work on vercel - Could just add a 'Favorites' option in the schema

I think I'm just going to go with JSON objects stored in the project directory, I shouldn't have more than a few hundred, it doesn't need to scale, and it's easier if I keep all the pieces together, and I don't have to mess around with MongoDB again, if I can get the schema working, this should be fine, realistically all I need is a main page with search functionality, and then a recipe page with multiple languages when clicked

- - -
### Recipe Sites :
Torrented some cookbooks to get recipes, also found some sites :
https://www.allrecipes.com/
https://www.recipetineats.com/
https://thecozycook.com/

Keto(LowCarb) - already have visisble abs, no gym, no money for food, I don't need these, yet:
https://www.genaw.com/lowcarb/recipes.html
https://www.gnom-gnom.com/
https://cavemanketo.com/
http://healthyketo.com/
https://www.heyketomama.com/
https://www.ibreatheimhungry.com/
https://www.ketoconnect.net/recipes/
https://www.ruled.me/
https://nobunplease.com/
https://www.tasteaholics.com/recipes/low-carb-recipes/
https://www.strongrfastr.com/meal_plans/keto
https://www.reddit.com/r/ketorecipes/wiki/index/#wiki_useful_keto_recipe_blogs.3A