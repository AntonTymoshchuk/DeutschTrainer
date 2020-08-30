from gtts import gTTS
from playsound import playsound
from speech_recognition import Recognizer, Microphone, UnknownValueError
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from pathlib import Path
import threading
import platform
import sqlite3
import time
import os


class DeutschTrainerLayout(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)

        self.directory_name = 'Deutsch Trainer'

        self.home_path = str(Path.home())
        self.home_path += os.sep
        self.home_path += 'Dropbox'
        self.home_path += os.sep
        self.home_path += 'MAIN'
        self.home_path += os.sep
        self.home_path += 'ПАПКИ ЦЕЛЕЙ'
        self.home_path += os.sep
        self.home_path += 'Deutschland Studien'
        self.home_path += os.sep
        self.home_path += self.directory_name

        self.de_path = '{0}{1}de'.format(self.home_path, os.sep)
        self.ru_path = '{0}{1}ru'.format(self.home_path, os.sep)

        self.database_path = '{0}{1}database.db'.format(self.home_path, os.sep)

        self.test_type = None
        self.cognitive_thread = None

    def allow_user_to_add_words(self):
        self.ids.german_word_text_input.disabled = False
        self.ids.russian_word_text_input.disabled = False
        self.ids.accept_adding_words_button.disabled = False
        self.ids.start_visual_russian_to_verbal_deutsch_training.disabled = True
        self.ids.start_visual_russian_to_written_deutsch_training.disabled = True
        self.ids.start_hearing_russian_to_verbal_deutsch_training.disabled = True
        self.ids.start_hearing_russian_to_written_deutsch_training.disabled = True
        self.ids.start_visual_deutsch_to_verbal_russian_training.disabled = True
        self.ids.start_visual_deutsch_to_written_russian_training.disabled = True
        self.ids.start_hearing_deutsch_to_verbal_russian_training.disabled = True
        self.ids.start_hearing_deutsch_to_written_russian_training.disabled = True

    def accept_adding_new_words(self):
        if platform.system() == 'Linux':
            tts = gTTS(self.ids.german_word_text_input.text, lang='de')
            tts.save('{0}/{1}.mp3'.format(self.de_path, self.ids.german_word_text_input.text))
            tts = gTTS(self.ids.russian_word_text_input.text, lang='ru')
            tts.save('{0}/{1}.mp3'.format(self.ru_path, self.ids.russian_word_text_input.text))
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Dictionary (WordDe, WordRu) "
                           "VALUES ('{0}', '{1}');".format(self.ids.german_word_text_input.text,
                                                           self.ids.russian_word_text_input.text))
            connection.commit()
            result = cursor.execute("SELECT Id FROM Dictionary "
                                    "WHERE WordDe='{0}'".format(self.ids.german_word_text_input.text))
            result_id = list(result)[0][0]
            cursor.execute("INSERT INTO VisualRussianToVerbalDeutsch (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO VisualRussianToWrittenDeutsch (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO HearingRussianToVerbalDeutsch (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO HearingRussianToWrittenDeutsch (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO VisualDeutschToVerbalRussian (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO VisualDeutschToWrittenRussian (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO HearingDeutschToVerbalRussian (DictId) "
                           "VALUES ({0});".format(result_id))
            cursor.execute("INSERT INTO HearingDeutschToWrittenRussian (DictId) "
                           "VALUES ({0});".format(result_id))
            connection.commit()
            connection.close()
            self.ids.german_word_text_input.text = ''
            self.ids.russian_word_text_input.text = ''

    def allow_user_to_start_training(self):
        self.ids.german_word_text_input.disabled = True
        self.ids.russian_word_text_input.disabled = True
        self.ids.accept_adding_words_button.disabled = True
        self.ids.start_visual_russian_to_verbal_deutsch_training.disabled = False
        self.ids.start_visual_russian_to_written_deutsch_training.disabled = False
        self.ids.start_hearing_russian_to_verbal_deutsch_training.disabled = False
        self.ids.start_hearing_russian_to_written_deutsch_training.disabled = False
        self.ids.start_visual_deutsch_to_verbal_russian_training.disabled = False
        self.ids.start_visual_deutsch_to_written_russian_training.disabled = False
        self.ids.start_hearing_deutsch_to_verbal_russian_training.disabled = False
        self.ids.start_hearing_deutsch_to_written_russian_training.disabled = False

    def do_common_disabling_actions_for_training_type_buttons(self):
        self.ids.add_words_button.disabled = True
        self.ids.start_training_button.disabled = True
        self.ids.start_visual_russian_to_verbal_deutsch_training.disabled = True
        self.ids.start_visual_russian_to_written_deutsch_training.disabled = True
        self.ids.start_hearing_russian_to_verbal_deutsch_training.disabled = True
        self.ids.start_hearing_russian_to_written_deutsch_training.disabled = True
        self.ids.start_visual_deutsch_to_verbal_russian_training.disabled = True
        self.ids.start_visual_deutsch_to_written_russian_training.disabled = True
        self.ids.start_hearing_deutsch_to_verbal_russian_training.disabled = True
        self.ids.start_hearing_deutsch_to_written_russian_training.disabled = True
        self.ids.answer_text_input.disabled = True
        self.ids.accept_answer_button.disabled = True
        self.ids.quit_training_button.disabled = False

    def do_common_disabling_actions_for_train_ending(self):
        self.ids.add_words_button.disabled = False
        self.ids.start_training_button.disabled = False
        self.ids.start_visual_russian_to_verbal_deutsch_training.disabled = False
        self.ids.start_visual_russian_to_written_deutsch_training.disabled = False
        self.ids.start_hearing_russian_to_verbal_deutsch_training.disabled = False
        self.ids.start_hearing_russian_to_written_deutsch_training.disabled = False
        self.ids.start_visual_deutsch_to_verbal_russian_training.disabled = False
        self.ids.start_visual_deutsch_to_written_russian_training.disabled = False
        self.ids.start_hearing_deutsch_to_verbal_russian_training.disabled = False
        self.ids.start_hearing_deutsch_to_written_russian_training.disabled = False
        self.ids.answer_text_input.disabled = True
        self.ids.accept_answer_button.disabled = True

    def start_visual_russian_to_verbal_deutsch(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM VisualRussianToVerbalDeutsch"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'VisualRussianToVerbalDeutsch'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.question_language_label.text = 'Русский'
            self.ids.answer_language_label.text = 'Deutsch'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_visual_russian_to_written_deutsch(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM VisualRussianToWrittenDeutsch"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'VisualRussianToWrittenDeutsch'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.answer_text_input.disabled = False
            self.ids.accept_answer_button.disabled = False
            self.ids.question_language_label.text = 'Русский'
            self.ids.answer_language_label.text = 'Deutsch'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_hearing_russian_to_verbal_deutsch(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM HearingRussianToVerbalDeutsch"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'HearingRussianToVerbalDeutsch'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.question_language_label.text = 'Русский'
            self.ids.answer_language_label.text = 'Deutsch'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_hearing_russian_to_written_deutsch(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM HearingRussianToWrittenDeutsch"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'HearingRussianToWrittenDeutsch'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.answer_text_input.disabled = False
            self.ids.accept_answer_button.disabled = False
            self.ids.question_language_label.text = 'Русский'
            self.ids.answer_language_label.text = 'Deutsch'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_visual_deutsch_to_verbal_russian(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM VisualDeutschToVerbalRussian"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'VisualDeutschToVerbalRussian'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.question_language_label.text = 'Deutsch'
            self.ids.answer_language_label.text = 'Русский'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_visual_deutsch_to_written_russian(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM VisualDeutschToWrittenRussian"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'VisualDeutschToWrittenRussian'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.answer_text_input.disabled = False
            self.ids.accept_answer_button.disabled = False
            self.ids.question_language_label.text = 'Deutsch'
            self.ids.answer_language_label.text = 'Русский'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_hearing_deutsch_to_verbal_russian(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM HearingDeutschToVerbalRussian"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'HearingDeutschToVerbalRussian'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.question_language_label.text = 'Deutsch'
            self.ids.answer_language_label.text = 'Русский'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    def start_hearing_deutsch_to_written_russian(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        result = list(cursor.execute("SELECT * FROM HearingDeutschToWrittenRussian"))
        connection.close()
        test_list = self.sort(result)
        if test_list is not None:
            self.test_type = 'HearingDeutschToWrittenRussian'
            self.do_common_disabling_actions_for_training_type_buttons()
            self.ids.answer_text_input.disabled = False
            self.ids.accept_answer_button.disabled = False
            self.ids.question_language_label.text = 'Deutsch'
            self.ids.answer_language_label.text = 'Русский'
            self.cognitive_thread = CognitiveThread(self, test_list)
            self.cognitive_thread.daemon = True
            self.cognitive_thread.start()

    @staticmethod
    def calculate_absolute_value(item):
        return item[1] + item[2] + item[3]

    @staticmethod
    def calculate_negative_value(item):
        return item[2] + item[3]

    def sort(self, result):
        if len(result) > 0:
            absolute_sorting_list = result.copy()
            negative_sorting_list = result.copy()
            absolute_sorting_list.sort(key=self.calculate_absolute_value, reverse=False)
            negative_sorting_list.sort(key=self.calculate_negative_value, reverse=True)
            complete_list = []
            for item1, item2 in zip(absolute_sorting_list, negative_sorting_list):
                list1 = []
                for value in item1:
                    list1.append(value)
                complete_list.append(list1)
                list2 = []
                for value in item2:
                    list2.append(value)
                complete_list.append(list2)
            return complete_list
        return None

    def accept_answer_button_press(self):
        self.cognitive_thread.require_answer_check = True

    def quit_training_after_current_question(self):
        self.cognitive_thread.quit_training = True


class CognitiveThread(threading.Thread):
    def __init__(self, app_layout, test_list):
        threading.Thread.__init__(self)
        self.app_layout = app_layout
        self.test_list = test_list
        self.require_answer_check = False
        self.quit_training = False

    def run(self):
        self.test()

    def test(self):
        index = -1
        if self.app_layout.test_type == 'VisualRussianToVerbalDeutsch':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                index += 1
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                self.app_layout.ids.question_label.text = word_ru
                recognizer = Recognizer()
                phrase = None
                try:
                    with Microphone() as microphone:
                        recognizer.adjust_for_ambient_noise(microphone)
                        audio = recognizer.listen(microphone, timeout=30)
                    phrase = recognizer.recognize_google(audio, language='de-DE')
                except (UnknownValueError, TimeoutError):
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_de)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE VisualRussianToVerbalDeutsch "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                if phrase is not None:
                    if phrase == word_de:
                        self.app_layout.ids.test_result_label.text = 'Правильно!'
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE VisualRussianToVerbalDeutsch "
                                       "SET Correct = {0} "
                                       "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][1] += 1
                            next_index += 1
                    else:
                        self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_de)
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE VisualRussianToVerbalDeutsch "
                                       "SET Mistaked = {0} "
                                       "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][2] += 1
                            next_index += 1
                time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'VisualRussianToWrittenDeutsch':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.answer_text_input.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                self.app_layout.ids.question_label.text = word_ru
                time_temp = 0.0
                while time_temp < 30:
                    if self.require_answer_check:
                        self.require_answer_check = False
                        if self.app_layout.ids.answer_text_input.text == word_de:
                            self.app_layout.ids.test_result_label.text = 'Правильно!'
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VisualRussianToWrittenDeutsch "
                                           "SET Correct = {0} "
                                           "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][1] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                        else:
                            self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_de)
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VisualRussianToWrittenDeutsch "
                                           "SET Mistaked = {0} "
                                           "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][2] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                    time_temp += 0.1
                    time.sleep(0.1)
                if int(time_temp) == 30:
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_de)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE VisualRussianToWrittenDeutsch "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                    time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.answer_text_input.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'HearingRussianToVerbalDeutsch':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                index += 1
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                playsound('{0}{1}{2}.mp3'.format(self.app_layout.ru_path, os.sep, word_ru))
                recognizer = Recognizer()
                phrase = None
                try:
                    with Microphone() as microphone:
                        recognizer.adjust_for_ambient_noise(microphone)
                        audio = recognizer.listen(microphone, timeout=30)
                    phrase = recognizer.recognize_google(audio, language='de-DE')
                except (UnknownValueError, TimeoutError):
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_de)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE HearingRussianToVerbalDeutsch "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                if phrase is not None:
                    if phrase == word_de:
                        self.app_layout.ids.test_result_label.text = 'Правильно!'
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE HearingRussianToVerbalDeutsch "
                                       "SET Correct = {0} "
                                       "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][1] += 1
                            next_index += 1
                    else:
                        self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_de)
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE HearingRussianToVerbalDeutsch "
                                       "SET Mistaked = {0} "
                                       "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][2] += 1
                            next_index += 1
                time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'HearingRussianToWrittenDeutsch':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.answer_text_input.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                playsound('{0}{1}{2}.mp3'.format(self.app_layout.ru_path, os.sep, word_ru))
                time_temp = 0.0
                while time_temp < 30:
                    if self.require_answer_check:
                        self.require_answer_check = False
                        if self.app_layout.ids.answer_text_input.text == word_de:
                            self.app_layout.ids.test_result_label.text = 'Правильно!'
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE HearingRussianToWrittenDeutsch "
                                           "SET Correct = {0} "
                                           "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][1] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                        else:
                            self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_de)
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE HearingRussianToWrittenDeutsch "
                                           "SET Mistaked = {0} "
                                           "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][2] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                    time_temp += 0.1
                    time.sleep(0.1)
                if int(time_temp) == 30:
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_de)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE HearingRussianToWrittenDeutsch "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                    time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.answer_text_input.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'VisualDeutschToVerbalRussian':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                index += 1
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                self.app_layout.ids.question_label.text = word_de
                recognizer = Recognizer()
                phrase = None
                try:
                    with Microphone() as microphone:
                        recognizer.adjust_for_ambient_noise(microphone)
                        audio = recognizer.listen(microphone, timeout=30)
                    phrase = recognizer.recognize_google(audio, language='ru-RU')
                except (UnknownValueError, TimeoutError):
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_ru)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE VisualDeutschToVerbalRussian "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                if phrase is not None:
                    if phrase == word_ru:
                        self.app_layout.ids.test_result_label.text = 'Правильно!'
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE VisualDeutschToVerbalRussian "
                                       "SET Correct = {0} "
                                       "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][1] += 1
                            next_index += 1
                    else:
                        self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_ru)
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE VisualDeutschToVerbalRussian "
                                       "SET Mistaked = {0} "
                                       "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][2] += 1
                            next_index += 1
                time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'VisualDeutschToWrittenRussian':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.answer_text_input.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                self.app_layout.ids.question_label.text = word_de
                time_temp = 0.0
                while time_temp < 30:
                    if self.require_answer_check:
                        self.require_answer_check = False
                        if self.app_layout.ids.answer_text_input.text == word_ru:
                            self.app_layout.ids.test_result_label.text = 'Правильно!'
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VisualDeutschToWrittenRussian "
                                           "SET Correct = {0} "
                                           "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][1] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                        else:
                            self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_ru)
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE VisualDeutschToWrittenRussian "
                                           "SET Mistaked = {0} "
                                           "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][2] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                    time_temp += 0.1
                    time.sleep(0.1)
                if int(time_temp) == 30:
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_ru)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE VisualDeutschToWrittenRussian "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                    time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.answer_text_input.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'HearingDeutschToVerbalRussian':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                index += 1
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                playsound('{0}{1}{2}.mp3'.format(self.app_layout.de_path, os.sep, word_de))
                recognizer = Recognizer()
                phrase = None
                try:
                    with Microphone() as microphone:
                        recognizer.adjust_for_ambient_noise(microphone)
                        audio = recognizer.listen(microphone, timeout=30)
                    phrase = recognizer.recognize_google(audio, language='ru-RU')
                except (UnknownValueError, TimeoutError):
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_ru)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE HearingDeutschToVerbalRussian "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                if phrase is not None:
                    if phrase == word_ru:
                        self.app_layout.ids.test_result_label.text = 'Правильно!'
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE HearingDeutschToVerbalRussian "
                                       "SET Correct = {0} "
                                       "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][1] += 1
                            next_index += 1
                    else:
                        self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_ru)
                        connection = sqlite3.connect(self.app_layout.database_path)
                        cursor = connection.cursor()
                        cursor.execute("UPDATE HearingDeutschToVerbalRussian "
                                       "SET Mistaked = {0} "
                                       "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                        connection.commit()
                        connection.close()
                        next_index = index + 1
                        while next_index < len(self.test_list):
                            if self.test_list[next_index][0] == test_item[0]:
                                self.test_list[next_index][2] += 1
                            next_index += 1
                time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()

        elif self.app_layout.test_type == 'HearingDeutschToWrittenRussian':
            for test_item in self.test_list:
                if self.quit_training:
                    break
                self.app_layout.ids.question_label.text = ''
                self.app_layout.ids.answer_text_input.text = ''
                self.app_layout.ids.test_result_label.text = ''
                time.sleep(1)
                connection = sqlite3.connect(self.app_layout.database_path)
                cursor = connection.cursor()
                result = list(cursor.execute("SELECT WordDe, WordRu "
                                             "FROM Dictionary "
                                             "WHERE Id = {0};".format(test_item[0])))
                connection.close()
                word_de = result[0][0]
                word_ru = result[0][1]
                playsound('{0}{1}{2}.mp3'.format(self.app_layout.de_path, os.sep, word_de))
                time_temp = 0.0
                while time_temp < 30:
                    if self.require_answer_check:
                        self.require_answer_check = False
                        if self.app_layout.ids.answer_text_input.text == word_ru:
                            self.app_layout.ids.test_result_label.text = 'Правильно!'
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE HearingDeutschToWrittenRussian "
                                           "SET Correct = {0} "
                                           "WHERE DictId = {1}".format(test_item[1] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][1] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                        else:
                            self.app_layout.ids.test_result_label.text = "Неправильно, '{0}'".format(word_ru)
                            connection = sqlite3.connect(self.app_layout.database_path)
                            cursor = connection.cursor()
                            cursor.execute("UPDATE HearingDeutschToWrittenRussian "
                                           "SET Mistaked = {0} "
                                           "WHERE DictId = {1}".format(test_item[2] + 1, test_item[0]))
                            connection.commit()
                            connection.close()
                            next_index = index + 1
                            while next_index < len(self.test_list):
                                if self.test_list[next_index][0] == test_item[0]:
                                    self.test_list[next_index][2] += 1
                                next_index += 1
                            time.sleep(1)
                            break
                    time_temp += 0.1
                    time.sleep(0.1)
                if int(time_temp) == 30:
                    self.app_layout.ids.test_result_label.text = "Нет ответа, '{0}'".format(word_ru)
                    connection = sqlite3.connect(self.app_layout.database_path)
                    cursor = connection.cursor()
                    cursor.execute("UPDATE HearingDeutschToWrittenRussian "
                                   "SET NoAnswer = {0} "
                                   "WHERE DictId = {1}".format(test_item[3] + 1, test_item[0]))
                    connection.commit()
                    connection.close()
                    next_index = index + 1
                    while next_index < len(self.test_list):
                        if self.test_list[next_index][0] == test_item[0]:
                            self.test_list[next_index][3] += 1
                        next_index += 1
                    time.sleep(1)
            self.app_layout.ids.question_language_label.text = ''
            self.app_layout.ids.answer_language_label.text = ''
            self.app_layout.ids.question_label.text = ''
            self.app_layout.ids.answer_text_input.text = ''
            self.app_layout.ids.test_result_label.text = "Тренировка окончена"
            self.app_layout.ids.quit_training_button.disabled = True
            time.sleep(1)
            self.app_layout.ids.test_result_label.text = ''
            self.app_layout.do_common_disabling_actions_for_train_ending()


class DeutschTrainerApp(App):
    def build(self):
        return DeutschTrainerLayout()


if __name__ == '__main__':
    Window.clearcolor = [1, 1, 1, 1]
    DeutschTrainerApp().run()
    # tts = gTTS('Бла бла бла!', lang='ru')
    # tts.save('Бла бла бла.mp4')
    # playsound('Бла бла бла.mp4')

    # recognizer = Recognizer()
    # with Microphone() as microphone:
    #     audio = recognizer.listen(microphone)

    # query = recognizer.recognize_google(audio, language='ru-RU')
    # print(query)
