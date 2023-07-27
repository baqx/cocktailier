from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import CircularRippleBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen
import requests
from kivy.clock import Clock
from kivy.config import Config
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', -1700)
Config.set('graphics', 'top', 100)
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (320, 600)

# --------------------------------------------------------------------------------------------------------
Builder.load_file('kvs/pages/splash.kv')
Builder.load_file('kvs/pages/home.kv')
Builder.load_file('kvs/pages/recipe.kv')


# --------------------------------------------------------------------
# widgets
# ----------------------------------------------------------------------------------------------------------


class WindowManager(ScreenManager):
    pass


class SplashScreen(MDScreen):
    pass



class HomeScreen(MDScreen):
    pass


class RecipeScreen(MDScreen):
    title = StringProperty()
    subtitle = StringProperty()
    img = StringProperty()
    id = NumericProperty()
    description = StringProperty()


# ---------------------------------------------------------------------------------------------------------------------------------
class CardItem(MDCard, CircularRippleBehavior, Button):
    title = StringProperty()
    subtitle = StringProperty()
    description = StringProperty()
    img = StringProperty()
    id = NumericProperty()

    def __init__(self, *args, **kwargs):
        self.ripple_scale = 1
        super().__init__(*args, **kwargs)
        self.elevation = 1


# --------------------------------------------------------------------------------------------------------------------------------
class MainApp(MDApp):

    def build(self):
        Window.borderless = True
        self.my_theme_color = '#37096C'
        self.my_theme_color1 = '#7512FF'
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.accent_hue = '400'
        self.title = "Cocktailier"
        self.theme_cls.material_style = "M3"

        self.wm = WindowManager(transition=FadeTransition())
        screens = [
            SplashScreen(name='Splash'),
            HomeScreen(name='Home'),
            RecipeScreen(name='Recipe'),


        ]

        for screen in screens:
            self.wm.add_widget(screen)

        return self.wm

    def on_start(self):
        skp = "https://api.punkapi.com/v2/beers/random"
        try:
            response = requests.get(skp)
            if response.status_code == 200:
                beer_data = response.json()
                for beer in beer_data:
                    # Extract some information from each beer entry
                    name1 = beer.get("name", "Unknown")
                    image_url1 = beer.get("image_url", "assets/img/product1.png")
                    self.wm.get_screen('Home').ids.spec.source = image_url1
                    self.wm.get_screen('Home').ids.specl.text = name1

            url = "https://api.punkapi.com/v2/beers?page=1&per_page=8"  # Replace this with the actual URL of the JSON data

            response = requests.get(url)
            if response.status_code == 200:
                beer_data = response.json()
                for beer in beer_data:
                    # Extract some information from each beer entry
                    beer_name = beer.get("name", "Unknown")
                    beer_id = beer.get("id", "0")
                    beer_tagline = beer.get("tagline", "No tagline")
                    beer_description = beer.get("description", "No description")
                    image_url = beer.get("image_url", "assets/img/logo.png")
                    beer_ibu = beer.get("ibu", "N/A")
                    self.wm.get_screen('Home').ids.mylist.add_widget(
                        CardItem(title=f"{beer_name}", subtitle=f"{beer_tagline}", img=f"{image_url}", id=int(beer_id),description=str(beer_description)))

                    # Display the extracted information

            else:
                print("Error: Unable to fetch data from the URL.")
                return None
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

        Clock.schedule_once(self.gotohome, 15)



    def change_screen(self, screen):
        '''Change screen using the window manager.'''
        self.wm.current = screen

    def gotohome(self, dt):
        self.change_screen("Home")


    def gotorecipe(self, id, title, description, img, subtitle):
        print(id)
        print(img)
        print(title)
        print(subtitle)
        print(description)
        self.wm.get_screen('Recipe').id=id
        self.wm.get_screen('Recipe').title=title
        self.wm.get_screen('Recipe').description=description
        self.wm.get_screen('Recipe').img=img
        self.wm.get_screen('Recipe').subtitle=subtitle
        self.change_screen("Recipe")


if __name__ == "__main__":
    LabelBase.register(name="swins", fn_regular="assets/fonts/swins.ttf")
    LabelBase.register(name="akadora", fn_regular="assets/fonts/akadora.ttf")
    LabelBase.register(name="firabold", fn_regular="assets/fonts/firabold.ttf")
    LabelBase.register(name="aff", fn_regular="assets/fonts/aff.ttf")
    LabelBase.register(name="firabook", fn_regular="assets/fonts/FiraSans-Book.ttf")
    LabelBase.register(name="firaregular", fn_regular="assets/fonts/FiraSans-Regular.ttf")
    LabelBase.register(name="firaebold", fn_regular="assets/fonts/FiraSans-ExtraBold.ttf")
    MainApp().run()
