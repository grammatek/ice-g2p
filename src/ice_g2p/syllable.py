#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Syllable:
    """
    Syllabification processes phonetic transcripts of words, where each phone is separated by a space. This space
    separated transcription represents the content field of a Syllable object.
    Note that some phones might be written as two characters.
    """

    def __init__(self):
        self.content = '' #the transcription of the syllable, space between each phone
        self.has_nucleus = False
        self.cons_cluster = None
        self.stress = 0

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.content

    def append(self, phone_str):
        self.content += phone_str + ' '

    def prepend(self, phone_str):
        self.content = phone_str + ' ' + self.content

    def last_phones(self, number=1):
        """
        return number last phones from content
        :param number: number of last phones to return
        :return:
        """
        phone_arr = self.content.split()
        if number <= len(phone_arr):
            result_phones = phone_arr[-number:]
            return ' '.join(result_phones)
        raise IndexError('Number of phones to large: ' + str(number)
                         + ' is larger than length of content (' + self.content + ')')

    def last_index(self):
        """
        :return: index of last character (not space) in content
        """
        cont_len = len(self.content.strip())
        ind = cont_len - 1 if cont_len > 0 else 0
        return ind

    def startswith(self, phone):
        if self.content[0] == phone:
            return True
        return False

    def endswith(self, phone):
        if self.content[self.last_index()] == phone:
            return True
        return False

    def index_of_cluster(self):
        if self.cons_cluster:
            return self.content.rfind(self.cons_cluster)
        else:
            return -1

    def remove_cluster(self):
        self.content = self.content[:self.index_of_cluster()]
