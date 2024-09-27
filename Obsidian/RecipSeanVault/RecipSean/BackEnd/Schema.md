[[Back End]]

- - - 
-Schema Query Using Claude :
I'm creating a recipe app, but I need a schema for inputting and outputting data, I want to create it using json objects in each individual folders, I want it to have a recipe name, ingredients list, utensils required, cooking time, prep time, I want it to be optional 3 languages(slovak, english, and japanese) if one is missing it won't break the code, I want it to have each instruction as a bullet point with time it takes to complete each action, and a favorite boolean for the best recipes - can you create a json schema that I can use for this? I want to seperate it as well by nationality, so indian recipes in indian folder, japanese in japanese folder as json objects, etc
- - -
### Result :
{

"$schema": "http://json-schema.org/draft-07/schema#",

"type": "object",

"properties": {

"id": {

"type": "string",

"description": "Unique identifier for the recipe"

},

"name": {

"type": "string",

"description": "Name of the recipe"

},

"ingredients": {

"type": "array",

"items": {

"type": "string"

},

"description": "List of ingredients"

},

"utensils": {

"type": "array",

"items": {

"type": "string"

},

"description": "List of required utensils"

},

"cookingTime": {

"type": "integer",

"description": "Total cooking time in minutes"

},

"prepTime": {

"type": "integer",

"description": "Preparation time in minutes"

},

"instructions": {

"type": "array",

"items": {

"type": "object",

"properties": {

"time": {

"type": "integer",

"description": "Time for this step in minutes"

},

"en": {

"type": "string",

"description": "Instruction step in English"

},

"sk": {

"type": "string",

"description": "Instruction step in Slovak"

},

"ja": {

"type": "string",

"description": "Instruction step in Japanese"

},

"primaryIngredient": {

"type": "string",

"description": "Primary ingredient for this step"

}

},

"required": ["time", "en"]

},

"description": "List of instruction steps with translations"

},

"favorite": {

"type": "boolean",

"default": false,

"description": "Whether this recipe is a favorite"

},

"recipeType": {

"type": "string",

"description": "The type or category of the recipe"

}

},

"required": ["id", "name", "ingredients", "instructions", "recipeType"]

}
- - -
#### Example JSON:
{
  "id": "pasta_001",
  "name": "Simple Pasta",
  "ingredients": [
    "200g pasta",
    "2L water",
    "1 tsp salt"
  ],
  "utensils": [
    "Large pot",
    "Colander"
  ],
  "cookingTime": 20,
  "prepTime": 5,
  "instructions": [
    {
      "time": 5,
      "en": "Boil water in a large pot",
      "sk": "Priveďte vodu do varu vo veľkom hrnci",
      "ja": "大きな鍋で水を沸騰させる",
      "primaryIngredient": "water"
    },
    {
      "time": 10,
      "en": "Add pasta and cook",
      "sk": "Pridajte cestoviny a varte",
      "ja": "パスタを加えて茹でる",
      "primaryIngredient": "pasta"
    },
    {
      "time": 5,
      "en": "Drain pasta and let it cool",
      "primaryIngredient": "pasta"
    }
  ],
  "favorite": true,
  "recipeType": "simple"
}
- - - 
#### Display Function :
def format_instruction(instruction):

time = f"**{instruction['time']} min:**"

text = instruction['en']

if 'primaryIngredient' in instruction:

primary = instruction['primaryIngredient']

text = text.replace(primary, f"**{primary}**")

return f"{time} {text}"

###### Usage:

for step in recipe['instructions']:

print(format_instruction(step))

##### Appearance:
**5 min:** Boil **water** in a large pot
**10 min:** Add **pasta** and cook
**5 min:** Drain **pasta** and let it cool
- - - 
### Schema Explained :
Key points:

1. The time field is now first in each instruction object.

- Only the time and en (English) fields are required for each instruction step.

- The primaryIngredient field is optional and can be used to highlight the main ingredient in each step.

- If a step doesn't have Slovak or Japanese translations, it won't break the code.

- The formatting function adds bold markdown to the time and primary ingredient.

This structure allows for flexibility in adding instructions with or without translations, always includes the time, and provides a way to highlight the primary ingredient in each step.
- - -
The recipes should be located in the 'src/recipes/<nationality/type>/<recipe>.json' as individual json files
- - -
#Create a type definition for your recipes. In src/types/recipe.ts:
export type Instruction = {

time: number;

en: string;

sk?: string;

ja?: string;

primaryIngredient?: string;

};

  

export type Recipe = {

id: string;

name: string;

ingredients: string[];

utensils: string[];

cookingTime: number;

prepTime: number;

instructions: Instruction[];

favorite: boolean;

recipeType: string;

};
- - -
#Create a utility function to load recipes. In src/lib/loadRecipes.ts:
import fs from 'fs';

import path from 'path';

import { Recipe } from '../types/recipe';

  

const recipesDirectory = path.join(process.cwd(), 'data');

  

export function getAllRecipes(): Recipe[] {

const recipes: Recipe[] = [];

  

function readRecipesInDirectory(dir: string) {

const files = fs.readdirSync(dir);

  

for (const file of files) {

const filePath = path.join(dir, file);

const stat = fs.statSync(filePath);

  

if (stat.isDirectory()) {

readRecipesInDirectory(filePath);

} else if (file.endsWith('.json')) {

const fileContents = fs.readFileSync(filePath, 'utf8');

const recipe: Recipe = JSON.parse(fileContents);

recipes.push(recipe);

}

}

}

  

readRecipesInDirectory(recipesDirectory);

return recipes;

}

  

export function getRecipeById(id: string): Recipe | undefined {

const recipes = getAllRecipes();

return recipes.find(recipe => recipe.id === id);

}

- - -
#Use these functions in your pages or components. For example, in src/app/recipes/page.tsx:
import { getAllRecipes } from '../../lib/loadRecipes';

  

export default function RecipesPage() {

const recipes = getAllRecipes();

  

return (

<div>

<h1 className="text-2xl font-bold mb-4">All Recipes</h1>

<ul>

{recipes.map(recipe => (

<li key={recipe.id} className="mb-2">

<a href={`/recipes/${recipe.id}`} className="text-blue-500 hover:underline">

{recipe.name} - {recipe.recipeType}

</a>

</li>

))}

</ul>

</div>

);

}

- - -
#Use these functions in your pages or components. For example, in src/app/recipes/page.tsx:
import { getAllRecipes } from '../../lib/loadRecipes';

export default function RecipesPage() {
  const recipes = getAllRecipes();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">All Recipes</h1>
      <ul>
        {recipes.map(recipe => (
          <li key={recipe.id} className="mb-2">
            <a href={`/recipes/${recipe.id}`} className="text-blue-500 hover:underline">
              {recipe.name}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

#4. For individual recipe pages, you can create a dynamic route. In src/app/recipes/[id]/page.tsx:
import { getRecipeById } from '../../../lib/loadRecipes';

export default function RecipePage({ params }: { params: { id: string } }) {
  const recipe = getRecipeById(params.id);

  if (!recipe) {
    return <div>Recipe not found</div>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">{recipe.name}</h1>
      {/* Add more recipe details here */}
    </div>
  );
}

- - -
#This structure allows you to:

- Keep your recipe data separate from your application code

- Easily add, remove, or modify recipes without changing your app code

- Use TypeScript for type checking and autocompletion

- Use Tailwind classes for styling your components

Remember to add the data folder to your .gitignore file if you don't want to track the recipe files in your git repository (for example, if you're loading them from an external source or API in production).

