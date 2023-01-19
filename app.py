import os,random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
class MyPopup(Popup):
    def on_dismiss(self):
        self.am = -1
class GeneratorKartek(App):
    def build(self):
        self.colors=['green','yellow','red','black']
        self.x=0
        self.weight=[40, 30, 15, 10]
        self.end=False
        self.history_images = []
        self.am = -1
        self.l = 0
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        for i in self.colors:
            for f in os.listdir(os.path.join(self.current_dir, i)):
                if f.endswith('.png'):
                    self.l += 1
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image(source=os.path.join(self.current_dir,'start.png'), size_hint=(1, 20))
        self.text = Label(text=f'0/{self.l}')
        self.layout.add_widget(self.image)
        self.layout.add_widget(self.text)
        self.button_layout = BoxLayout(orientation='horizontal')
        self.change_image_button = Button(text='Następna kartka', size_hint=(0.5, 1))
        self.change_image_button.bind(on_press=self.change_image)
        self.button_layout.add_widget(self.change_image_button)

        self.popup_button = Button(text='Historia', size_hint=(0.5, 1))
        self.button_layout.add_widget(self.popup_button)
        self.popup_button.bind(on_press=self.open_popup)
        self.layout.add_widget(self.button_layout)
        return self.layout
    def generate_image(self):
        color = random.choices(self.colors, weights=self.weight, k=1)[0]
        images = []
        for f in os.listdir(os.path.join(self.current_dir, color)):
            if f.endswith('.png'):
                images.append(os.path.join(self.current_dir, color, f))
        new_image = random.choice(images)
        while new_image in self.history_images:

            new_image = random.choice(images)
            if all([new_image in self.history_images for new_image in images]):
                index = self.colors.index(color)
                self.colors.remove(color)
                self.weight.pop(index)

                color = random.choices(self.colors, weights=self.weight, k=1)[0]
                images = []
                for f in os.listdir(os.path.join(self.current_dir, color)):
                    if f.endswith('.png'):
                        images.append(os.path.join(self.current_dir, color, f))
                new_image = random.choice(images)
        self.history_images.append(new_image)
        self.image.source = new_image
    def change_image(self, instance):
        self.x += 1
        if self.x == self.l:
            self.text.text = 'Gra skończona'
            self.change_image_button.text = 'Zagraj ponownie'
            self.change_image_button.bind(on_press=self.restart)
            self.generate_image()

        else:
            self.text.text = f'{self.x}/{self.l}'
            self.generate_image()

    def open_popup(self, instance):
        layout = BoxLayout(orientation='vertical')
        if self.history_images!=[]:
            self.image2 = Image(source=self.history_images[self.am], size_hint=(1, 20))
            layout.add_widget(self.image2)
            button_layout = BoxLayout(orientation='horizontal')
            next_button = Button(text='Następna', size_hint=(0.5, 1))
            next_button.bind(on_press=self.next)
            button_layout.add_widget(next_button)
            previous_button = Button(text='Poprzednia', size_hint=(0.5, 1))
            button_layout.add_widget(previous_button)
            previous_button.bind(on_press=self.previous)
            layout.add_widget(button_layout)
            popup = MyPopup(title='Historia kartek', content=layout, size_hint=(0.9, 0.9))
            popup.open()
    def next(self,instance):
        if self.am+1<0:
            self.am+=1
        self.image2.source = self.history_images[self.am]
    def previous(self,insance):
        if abs(self.am)<len(self.history_images):
            self.am-=1
        self.image2.source = self.history_images[self.am]
    def restart(self, instance):
        self.x = 0
        self.colors= ['green', 'yellow', 'red', 'black']
        self.weight = [50, 30, 10, 5]
        self.text.text = f'{self.x}/{self.l}'
        self.change_image_button.unbind(on_press=self.restart)
        self.change_image_button.bind(on_press=self.change_image)
        self.change_image_button.text = 'Następna kartka'
        self.history_images.clear()


if __name__ == '__main__':
    GeneratorKartek().run()