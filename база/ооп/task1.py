# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 23:01:08 2020

@author: ВАЛЕРИЙ
"""
from person import *

magister1 = Magister()
magister1.SetName('Marie')
magister1.SetSurname('Smith')
magister1.SetAge(25)
magister1.SetNationality('UK')
magister1.SetAddress('London, XYZ street, 1')
magister1.SetCompanyName('Facebook')
magister1.SetCompanyAddress('London, YXZ street, 1')
magister1.SetWorkPhone('1-111-111-11-11')
magister1.SetScientific_field('Math')
magister1.SetType_of_scientist('theorist')
magister1.SetNumber_of_publications(3)


candidat1 = PhD()
candidat1.SetName('John')
candidat1.SetSurname('Dog')
candidat1.SetAge(35)
candidat1.SetNationality('Ukraine')
candidat1.SetAddress('Kiev, Park street, 1')
candidat1.SetCompanyName('Kashtan')
candidat1.SetCompanyAddress('Kiev, Les street, 2')
candidat1.SetWorkPhone('2-111-111-11-11')
candidat1.SetScientific_field('Physics')
candidat1.SetType_of_scientist('experimenter')
candidat1.SetNumber_of_publications(10)


doctor = PhPointD()
doctor.SetName('Anna')
doctor.SetSurname('Smith')
doctor.SetAge(23)
doctor.SetNationality('UK')
doctor.SetAddress('London, XYZ street, 1')
doctor.SetCompanyName('Pharmacy')
doctor.SetCompanyAddress('London, Bal street, 11')
doctor.SetWorkPhone('1-111-111-11-12')
doctor.SetScientific_field('Chemistry')
doctor.SetType_of_scientist('calculator')
doctor.SetNumber_of_publications(13)


scientists = [magister1, candidat1, doctor] 

for s in scientists:
    print(s.GetName(), ';', s.GetSurname(), ';', s.GetAge(), ';', s.GetNationality(), ';', s.GetAddress(), ';', s.GetCompanyName(), ';', s.GetWorkPhone(), ';', s.GetScientific_field(), ';', s.GetType_of_scientist(), ';', s.GetNumber_of_publications())
    print(' ')
    