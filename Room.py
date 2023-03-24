
class Room:

    def __init__(self, data):
        self.corpus = data[0]
        self.fidelio = data[1]
        self.room = data[2]
        self.tem = data[3]
        self.hum = data[4]
        self.date = data[5]
        self.time = data[6]
        self.standartTime = ""
        self.color = ""

        if data[6]//60 > 9:
            self.standartTime += str(data[6]//60)
        else:
            self.standartTime += "0" + str(data[6] // 60)

        self.standartTime += ":"

        if data[6]%60 > 9:
            self.standartTime += str(data[6]%60)
        else:
            self.standartTime += "0" + str(data[6]%60)
