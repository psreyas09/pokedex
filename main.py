import requests
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage

# Set window size for mobile (optional)
Window.size = (360, 640)

# Function to fetch Pokémon data
def fetch_pokemon(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Define the app layout using KV language
KV = '''
ScreenManager:
    HomeScreen:
    DetailsScreen:

<HomeScreen>:
    name: 'home'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDTopAppBar:
            title: "Pokédex"
            elevation: 10
            right_action_items: [["theme-light-dark", lambda x: app.toggle_theme()]]

        MDTextField:
            id: search_input
            hint_text: "Enter Pokémon Name or ID"
            size_hint_y: None
            height: 50

        MDRaisedButton:
            text: "Search"
            size_hint_y: None
            height: 50
            on_press: root.search_pokemon()

        ScrollView:
            MDGridLayout:
                id: pokemon_grid
                cols: 2
                spacing: 10
                size_hint_y: None
                height: self.minimum_height
                padding: 10

<DetailsScreen>:
    name: 'details'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        MDLabel:
            id: pokemon_name
            text: "Name: "
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]

        AsyncImage:
            id: pokemon_sprite
            size_hint: None, None
            size: "150dp", "150dp"
            pos_hint: {'center_x': 0.5}

        MDLabel:
            id: pokemon_id
            text: "ID: "
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: pokemon_types
            text: "Types: "
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: pokemon_stats
            text: "Stats: "
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            id: pokemon_abilities
            text: "Abilities: "
            size_hint_y: None
            height: self.texture_size[1]

        MDRaisedButton:
            text: "Back"
            size_hint_y: None
            height: 50
            on_press: root.manager.current = 'home'
'''

# Home Screen
class HomeScreen(Screen):
    def search_pokemon(self):
        pokemon_input = self.ids.search_input.text.strip()
        if not pokemon_input:
            return
        
        pokemon_data = fetch_pokemon(pokemon_input)
        if pokemon_data:
            self.manager.get_screen('details').display_pokemon_details(pokemon_data)
            self.manager.current = 'details'

# Details Screen
class DetailsScreen(Screen):
    def display_pokemon_details(self, pokemon_data):
        self.ids.pokemon_name.text = f"Name: {pokemon_data['name'].capitalize()}"
        self.ids.pokemon_id.text = f"ID: {pokemon_data['id']}"
        
        types = [t['type']['name'] for t in pokemon_data['types']]
        self.ids.pokemon_types.text = f"Types: {', '.join(types)}"
        
        stats_text = "\n".join([f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in pokemon_data['stats']])
        self.ids.pokemon_stats.text = f"Stats:\n{stats_text}"
        
        abilities = [a['ability']['name'] for a in pokemon_data['abilities']]
        self.ids.pokemon_abilities.text = f"Abilities: {', '.join(abilities)}"
        
        sprite_url = pokemon_data['sprites']['front_default']
        if sprite_url:
            self.ids.pokemon_sprite.source = sprite_url

# Main App
class PokedexApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"  # Default to light mode
        return Builder.load_string(KV)

    def toggle_theme(self):
        """Toggle between dark and light mode."""
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

if __name__ == "__main__":
    PokedexApp().run() 