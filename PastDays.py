from calendar import Calendar
from datetime import datetime

class PastDays:

    def __init__(self):

        self.year = int(str(datetime.now())[:4])
        self.month = int(str(datetime.now())[5:7])
        self.day = int(str(datetime.now())[8:10])

        self.cal = Calendar(0)

    def __normalizationDate(self, year: int, month: int, day: int):

        normDate = str(year)

        if month > 9:
            normDate += "-" + str(month)
        else:
            normDate += "-0" + str(month)

        if day > 9:
            normDate += "-" + str(day)
        else:
            normDate += "-0" + str(day)

        return normDate

    def __getListMonth(self, year: int, month: int, flag: bool):

        list = self.cal.monthdatescalendar(year, month)
        list1 = []
        for i in list:
            for j in i:
                if j.month == month:
                    if flag:
                        if j.day <= self.day:
                            list1.append(self.__normalizationDate(j.year,j.month,j.day))
                    else:
                        list1.append(self.__normalizationDate(j.year, j.month, j.day))
        return list1

    def __unification(self, year, month, number, numberDate):

        list = self.__getListMonth(year, month, False)
        list.reverse()

        if len(list) + number > numberDate:
            return list[:numberDate - number]
        else:
            return list


    def getListDate(self, numberDate):

        list = self.__getListMonth(self.year, self.month, True)
        list.reverse()
        month = self.month
        year = self.year

        while True:
            number = len(list)

            if number < numberDate:
                if month > 1:
                    month -= 1
                    list.extend(self.__unification(year, month, number, numberDate))
                else:
                    year -= 1
                    month = 13
            else:
                break

        list.reverse()

        if list == numberDate:
            return list
        else:
            list.reverse()
            list = list[:numberDate]
            list.reverse()
            return list
