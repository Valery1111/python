# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:41:50 2020

@author: ВАЛЕРИЙ
"""

class Grazhdanin:
    def __init__(self): # функция-конструктор
        #print('Пустой объект класса ' + self.__class__.__name__ + ' создан.')
        pass
    # setters

        
    def SetName(self, name):
        self._name = name # инициализация private-поля _surname
        
    def SetSurname(self, surname):
        self._surname = surname # инициализация private-поля _surname
    
    def SetAge(self, age): 
        self._age = age  # ... private поля _age
    
    def SetNationality(self, nationality):
        self._nationality = nationality # ... private поля _nationality
    
    def SetAddress(self, address): 
        self._address = address # ... private поля _nationality
        
    
    # getters - для доступа к private-полям извне через методы
    def GetName(self):
        return self._name
    
    def GetSurname(self):
        return self._surname
    
    def GetAge(self):
        return self._age
    
    def GetNationality(self):
        return self._nationality
    
    def GetAddress(self):
        return self._address


class Worker(Grazhdanin):  # родительский класс указывается в скобках
    def SetCompanyName(self, companyName):
        self._companyName = companyName
        
    def SetCompanyAddress(self, companyAddress):
        self._companyAddress = companyAddress
        
    def SetWorkPhone(self, workPhone):
        self._workPhone = workPhone
        
        
    def GetCompanyName(self):
        return self._companyName
    
    def GetCompanyAddress(self):
        return self._companyAddress
    
    def GetWorkPhone(self):
        return self._workPhone
    
class Scientist(Worker):
    def SetScientific_field(self, scientific_field):
        self._scientific_field = scientific_field
        
    def SetType_of_scientist(self, type_of_scientist):
        self._type_of_scientist = type_of_scientist
        
    def SetNumber_of_publications(self, number_of_publications):
        self._number_of_publications = number_of_publications
        
        
    def GetScientific_field(self):
        return self._scientific_field
        
    def GetType_of_scientist(self):
        return self._type_of_scientist
        
    def GetNumber_of_publications(self):
        return self._number_of_publications
    
    
class Magister(Scientist):
    pass

class PhD(Scientist):
    pass

class PhPointD(Scientist):
    pass


