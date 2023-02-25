import os
import pathlib
import shutil
import sys

from Cryptodome.Cipher import AES
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd_extensions.akivymd.uix.dialogs import AKAlertDialog

SUCCESS_DIALOG_KV_STRING = """
BoxLayout:
    orientation: "vertical"
    padding: dp(40)

    MDLabel:
        text: "Успешно!"
        size_hint_y: None
        height: self.texture_size[1]
        halign: "center"
        valign: "center"
        bold: True
        theme_text_color: "Custom"
        text_color: 0, .7, 0, 1

    MDLabel:
        text: "Сообщение зашифровано!"
        halign: "center"
        valign: "top"
        theme_text_color: "Custom"
        text_color: 0, .7, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Подтвердить"
        md_bg_color: 0, .7, 0, 1
        pos_hint: {"center_x": .5}
"""

ERROR_PATH_DIALOG_KV_STRING = """
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Ошибка..."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: "Невозможно зашифровать файл((("
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Закрыть"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}
"""

ERROR_DIR_DIALOG_KV_STRING = """
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Ошибка..."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: "Отсутствуют необходимые файлы для открытия."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Закрыть"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}
"""

ERROR_UPDATE_DIALOG_KV_STRING = """
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Ошибка..."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: "Не получается перезаписать файл..."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Закрыть"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}
"""

ERROR_PASSWORDS_DIALOG_KV_STRING = """
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Ошибка..."
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1

    MDLabel:
        text: "Ошибка при дешифровании. Проверьте пароли!"
        halign: "center"
        theme_text_color: "Custom"
        text_color: .9, 0, 0, 1
        font_style: "Caption"

    MDFillRoundFlatButton:
        id: button
        text: "Закрыть"
        md_bg_color: .9, 0, 0, 1
        pos_hint: {"center_x": .5}
"""

KV_STRING = """
ScreenManager:
    id: scr_mng
    
    create_path: create_path
    open_path: open_path
    first_open: first_open
    first_create: first_create
    second_open: second_open
    second_create: second_create
    third_open: third_open
    third_create: third_create
    
    first_hint_create: first_hint_create
    second_hint_create: second_hint_create
    third_hint_create: third_hint_create
    
    message: message
    
    MDScreen:
        name: 'main'
    
        FitImage:
            source: "assets/images/1355238-Bob-Odenkirk-Saul-GoodmanBetter-Call-Saul-4k-Ultra.jpg"
        
        MDBoxLayout:
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": .5}
            
            AnchorLayout:
            
                MDRaisedButton:
                    text: 'Создать'
                    font_size: 40
                    pos_hint: {'center_x': .5, 'center_y': 0.5}
                    on_release: app.go_to_create_page()
                    
            AnchorLayout:    
            
                MDRaisedButton:
                    text: 'Открыть'
                    font_size: 40
                    pos_hint: {'center_x': .5, 'center_y': 0.5}
                    on_release: app.go_to_open_page()
    
    MDScreen:
        name: 'open'
        
        FitImage:
            source: "assets/images/1118full-kim-wexler.jpg"
        
        MDBoxLayout:
            adaptive_height: True
            pos_hint: {"top": 1}
            padding: "6dp", "6dp", 0, 0
            
            MDRaisedButton:
                text: "[b]НАЗАД[/b]"
                on_release: app.go_to_main_page()
        
        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": 0.5}
            padding: 60, 0, 60, 0
            spacing: 70
            
            AnchorLayout:
            
                MDIconButton:
                    icon: 'folder'
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    user_font_size: "64sp"
                    on_release: app.open_open_file_manager()
            
            AnchorLayout:
            
                MDTextFieldRound:
                    id: open_path
                    hint_text: 'Укажите путь к файлу'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
        
            AnchorLayout:
                
                MDTextFieldRound:
                    id: first_open
                    hint_text: 'Пароль 1'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
            
            AnchorLayout:
                
                MDTextFieldRound:
                    id: second_open
                    hint_text: 'Пароль 2'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
            
            AnchorLayout:
                
                MDTextFieldRound:
                    id: third_open
                    hint_text: 'Пароль 3'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
        
            AnchorLayout:
                
                MDRaisedButton:
                    disabled: False if all([open_path.text, first_open.text, second_open.text, third_open.text]) else True
                    text: "[b]ОТКРЫТЬ[/b]"
                    on_release: app.check_passwords()
        
    MDScreen:
        name: 'create'
        
        FitImage:
            source: "assets/images/849119.jpg"
        
        MDBoxLayout:
            adaptive_height: True
            pos_hint: {"top": 1}
            padding: "6dp", "6dp", 0, 0
            
            MDRaisedButton:
                text: "[b]НАЗАД[/b]"
                on_release: app.go_to_main_page()
        
        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": 0.5}
            padding: 60, 0, 60, 0
            spacing: 60
            
            AnchorLayout:
            
                MDIconButton:
                    icon: 'folder'
                    theme_text_color: "Custom"
                    text_color: app.theme_cls.primary_color
                    user_font_size: "64sp"
                    on_release: app.open_create_file_manager()
            
            AnchorLayout:
            
                MDTextFieldRound:
                    id: create_path
                    hint_text: 'Укажите путь к файлу'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
            
            AnchorLayout:
                
                MDTextFieldRound:
                    id: first_hint_create
                    hint_text: 'Подсказка 1'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
                    
            AnchorLayout:
                
                MDTextFieldRound:
                    id: first_create
                    hint_text: 'Пароль 1'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False

            AnchorLayout:
                
                MDTextFieldRound:
                    id: second_hint_create
                    hint_text: 'Подсказка 2'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
                                
            AnchorLayout:
                
                MDTextFieldRound:
                    id: second_create
                    hint_text: 'Пароль 2'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False

            AnchorLayout:
                
                MDTextFieldRound:
                    id: third_hint_create
                    hint_text: 'Подсказка 3'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False

            AnchorLayout:
                
                MDTextFieldRound:
                    id: third_create
                    hint_text: 'Пароль 3'
                    normal_color: app.theme_cls.accent_color
                    color_active: 1, 0, 0, 1
                    font_size: 26
                    write_tab: False
        
            AnchorLayout:
                
                MDRaisedButton:
                    disabled: False if all([create_path.text, first_hint_create.text, first_create.text, second_hint_create.text, second_create.text, third_hint_create.text, third_create.text]) else True
                    text: "[b]СОЗДАТЬ[/b]"
                    on_release: app.cipher_file()
        
    MDScreen:
        name: 'viewer'
        
        FitImage:
            source: "assets/images/LilaLokiKali_hacker_fantasy_prince_friendly_smile_good_person_a_d3d2a383-ad1f-4eb8-a8ac-8df4d82838bb.png"
        
        BoxLayout:
            orientation: 'vertical'
            padding: "6dp"
            spacing: 20
            
            BoxLayout:
                size_hint_y: .1
            
                AnchorLayout:
            
                    MDRaisedButton:
                        text: "[b]НАЗАД[/b]"
                        on_release: app.go_to_open_page()
                    
                AnchorLayout:
            
                    MDRaisedButton:
                        text: "[b]СОХРАНИТЬ[/b]"
                        on_release: app.update_project()
            
            TextInput:
                id: message
                font_size: 26
"""


def cipher_message(passwords_and_hints, message: str, catalog_path: pathlib.Path):
    try:
        message = message.encode(encoding='utf-8') if isinstance(message, str) else message
        file_dict = dict()
        for i, pair in enumerate(passwords_and_hints, start=1):
            password, hint = pair
            password = password.lower()
            file_dict[f"hint{i}"] = hint
            cipher = AESCipher(password)
            message, nonce = cipher.encrypt(message)
            file_dict[f"nonce{i}"] = nonce
        file_dict['content'] = message

        catalog_path.mkdir(parents=True, exist_ok=True)

        for key, value in file_dict.items():
            new_file_path = catalog_path / (key + '.artur')
            value = value.encode(encoding='utf-8') if isinstance(value, str) else value
            with open(str(new_file_path), "wb") as f:
                f.write(value)
        return True
    except Exception as e:
        print(e)
        return False


def create_ciphered_file(passwords_and_hints, path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        content = None
    if content:

        dir_path = pathlib.Path(path).parent.resolve()
        new_catalog_path = dir_path / path[:path.rfind('.')]

        return cipher_message(passwords_and_hints, content, new_catalog_path)
    else:
        return False


def form_dict_from_folder_files(folder_path: str, file_names: list):
    file_dict = dict()
    try:
        for file_name in file_names:
            field = file_name[:file_name.rfind('.')]
            file_path = pathlib.Path(folder_path) / file_name
            with open(str(file_path), 'rb') as f:
                content = f.read()
            file_dict[field] = content
        return file_dict
    except:
        return None


def decode_using_file_dict(file_dict: dict, passwords: list):
    content = file_dict['content']
    try:
        for i in range(1, 4):
            nonce = file_dict[f"nonce{i}"]
            cipher = AESCipher(passwords[i - 1].lower())
            content = cipher.decrypt(content, nonce)
        message = content.decode(encoding='utf-8')
        return message
    except:
        return None


class AESCipher:
    KEY_LENGTH = 16

    def __init__(self, key: str):
        self.tag = None
        self.nonce = None
        if len(key) > self.KEY_LENGTH:
            key = key[:self.KEY_LENGTH]
        elif len(key) < self.KEY_LENGTH:
            key += 'a' * (self.KEY_LENGTH - len(key))
        self.key = key.encode(encoding='utf-8')

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(raw)
        self.tag = tag
        return ciphertext, cipher.nonce

    def decrypt(self, enc, nonce):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(enc)
        return plaintext


class MyApp(MDApp):
    title = 'Secret Viewer'
    icon = 'assets/images/w1500_50462300.jpg'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_open_file_manager = MDFileManager(
            exit_manager=self.exit_open_manager,
            select_path=self.select_open_path,
            selector='folder',
        )
        self.my_create_file_manager = MDFileManager(
            exit_manager=self.exit_create_manager,
            select_path=self.select_create_path,
            selector='file',
            ext=['.txt'],
        )

    def go_to_open_page(self, *args):
        self.root.open_path.text = ''
        self.root.first_open.text = ''
        self.root.second_open.text = ''
        self.root.third_open.text = ''
        self.root.current = 'open'

    def go_to_create_page(self, *args):
        self.root.create_path.text = ''
        self.root.first_create.text = ''
        self.root.first_hint_create.text = ''
        self.root.second_create.text = ''
        self.root.second_hint_create.text = ''
        self.root.third_create.text = ''
        self.root.third_hint_create.text = ''
        self.root.current = 'create'

    def go_to_main_page(self, *args):
        self.root.current = 'main'

    def go_to_viewer_page(self, *args):
        self.root.current = 'viewer'

    def check_passwords(self, *args):
        first = self.root.first_open.text
        second = self.root.second_open.text
        third = self.root.third_open.text
        path = self.root.open_path.text

        files = [x for x in pathlib.Path(path).glob('*') if x.is_file()]
        file_names = [file.name for file in files]
        if set(file_names) != set(
                [el + '.artur' for el in ["content", "hint1", "hint2", "hint3", "nonce1", "nonce2", "nonce3"]]):
            dialog = AKAlertDialog(
                header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
            )
            content = Builder.load_string(ERROR_DIR_DIALOG_KV_STRING)
            content.ids.button.bind(on_release=dialog.dismiss)
            dialog.content_cls = content
            dialog.open()
        else:
            file_dict = form_dict_from_folder_files(path, file_names)
            if file_dict is not None:
                message = decode_using_file_dict(file_dict, [first, second, third])
                if message is None:
                    dialog = AKAlertDialog(
                        header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
                    )
                    content = Builder.load_string(ERROR_PASSWORDS_DIALOG_KV_STRING)
                    content.ids.button.bind(on_release=dialog.dismiss)
                    dialog.content_cls = content
                    dialog.open()
                else:
                    self.root.message.text = message
                    self.go_to_viewer_page()

    def open_open_file_manager(self):
        path = pathlib.Path().resolve()
        self.my_open_file_manager.show(str(path))

    def open_create_file_manager(self):
        path = pathlib.Path().resolve()
        self.my_create_file_manager.show(str(path))

    def exit_create_manager(self, *args):
        self.my_create_file_manager.close()

    def exit_open_manager(self, *args):
        self.my_open_file_manager.close()

    def select_open_path(self, path):
        self.root.open_path.text = path
        self.update_open_hints(path)
        self.exit_open_manager()

    def update_open_hints(self, path: str):
        file_dict = form_dict_from_folder_files(path, ['hint1.artur', 'hint2.artur', 'hint3.artur'])
        if file_dict is not None:
            hint1 = file_dict['hint1'].decode(encoding='utf-8')
            hint2 = file_dict['hint2'].decode(encoding='utf-8')
            hint3 = file_dict['hint3'].decode(encoding='utf-8')

            self.root.first_open.hint_text = hint1
            self.root.second_open.hint_text = hint2
            self.root.third_open.hint_text = hint3

    def update_project(self, *args):
        catalog_path = pathlib.Path(self.root.open_path.text).resolve()
        shutil.rmtree(catalog_path)
        res = cipher_message(
            [
                (self.root.first_open.text, self.root.first_open.hint_text),
                (self.root.second_open.text, self.root.second_open.hint_text),
                (self.root.third_open.text, self.root.third_open.hint_text),
            ],
            self.root.message.text,
            catalog_path,
        )
        if res:
            dialog = AKAlertDialog(
                header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
            )
            content = Builder.load_string(SUCCESS_DIALOG_KV_STRING)
        else:
            dialog = AKAlertDialog(
                header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
            )
            content = Builder.load_string(ERROR_UPDATE_DIALOG_KV_STRING)
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def select_create_path(self, path):
        self.root.create_path.text = path
        self.exit_create_manager()

    def cipher_file(self, *args):
        res = create_ciphered_file(
            [
                (self.root.first_create.text, self.root.first_hint_create.text),
                (self.root.second_create.text, self.root.second_hint_create.text),
                (self.root.third_create.text, self.root.third_hint_create.text),
            ],
            self.root.create_path.text,
        )
        if res:
            dialog = AKAlertDialog(
                header_icon="check-circle-outline", header_bg=[0, 0.7, 0, 1]
            )
            content = Builder.load_string(SUCCESS_DIALOG_KV_STRING)
        else:
            dialog = AKAlertDialog(
                header_icon="close-circle-outline", header_bg=[0.9, 0, 0, 1]
            )
            content = Builder.load_string(ERROR_PATH_DIALOG_KV_STRING)
        content.ids.button.bind(on_release=dialog.dismiss)
        dialog.content_cls = content
        dialog.open()

    def build(self):
        Window.borderless = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_string(KV_STRING)


if __name__ == '__main__':
    MyApp().run()
