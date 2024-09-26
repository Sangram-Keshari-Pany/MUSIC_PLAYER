from kivy.uix.actionbar import Button
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivymd.uix.label import MDIcon
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
import os
import pygame
from kivy.clock import Clock

Window.size=(360,640)

class SPANY(MDApp):
    def build(self,**kwargs):
        super().__init__(**kwargs)
        pygame.mixer.init()
        return Builder.load_file("spany.kv")
    def filechooser(self):
        print("file opening for choose")
        self.folder_chooser=FileChooserIconView(dirselect=True)
        popup_layout = BoxLayout(orientation='vertical',padding=40,spacing=20)
        popup_layout.add_widget(self.folder_chooser)

        self.select_button=Button(text="select",size_hint=(0.5,0.1),pos_hint={"center_x": 0.5,"center_y": 0.5},on_press=self.select_all_song)
        popup_layout.add_widget(self.select_button)

        self.popup = Popup(title="Select your song", content=popup_layout, size_hint=(1,1))
        self.popup.open()
    
    def select_all_song(self,instances):
        selected_folder=self.folder_chooser.selection
        if selected_folder:
            folder_path=selected_folder[0]
            try:
                self.song_list=[os.path.join(folder_path,file) for file in os.listdir(folder_path) if file.endswith((".mp3",".wav"))]
            except Exception as error:
                print("error")
            else:
                if self.song_list:
                    self.current_song_index=0
                    self.playing=False
                    print(f"playing:{os.path.basename(self.song_list[self.current_song_index])}")
                else:
                    print("no audio file found in this folder")
        else:
            print("no folder detected")
        self.popup.dismiss()

    # slider
    def silderchange(self,value):
        if self.playing:
            current_length = pygame.mixer.Sound(self.song_list[self.current_song_index]).get_length()
            new_position = (value / 100) * current_length
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.song_list[self.current_song_index])
            pygame.mixer.music.play(0, new_position)
    
    def upadateslider(self,dt):
        if self.playing:
            current_position = pygame.mixer.music.get_pos() / 1000 
            current_length = pygame.mixer.Sound(self.song_list[self.current_song_index]).get_length()
            if current_length>0:
                # self.ids.slider_bar.value = (current_position / current_length) * 100
                ...
    
    def play_music(self):
        try:
            self.song_list
            if not self.playing:
                if 0<=self.current_song_index<=len(self.song_list):
                    pygame.mixer.music.load(self.song_list[self.current_song_index])
                    pygame.mixer.music.play()
                    # Clock.schedule_interval(self.upadateslider, 1)
                    print("music playing...")
                    self.playing = True
            else:
                pygame.mixer.music.pause()
                self.playing = False
                print("Music paused...")
                # Clock.unschedule(self.upadateslider)
        except:
            print("no folder selected")
    
    def play_next(self):
        if self.song_list:
            self.current_song_index=(self.current_song_index+1)%len(self.song_list)
            self.playing = False
            self.play_music()
            print("next song played")
    
    def play_prev(self):
        if self.song_list:
            self.current_song_index=(self.current_song_index-1)%len(self.song_list)
            self.playing = False
            self.play_music()
            print("previous song played")

SPANY().run()



