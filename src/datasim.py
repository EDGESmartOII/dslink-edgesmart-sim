from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys
import json
import random
import threading

from time import sleep
from userints import dsimui
from icecream import ic


class Worker(QObject):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.continue_run = True  # provide a bool run condition for the class

    def run(self):

        while self.continue_run:  # give the loop a stoppable condition
            try:
                ic('Doing work')
                result = self.fn(*self.args, **self.kwargs)

            except:
                ic("Didn't work", result)

            QThread.sleep(5)

        self.finished.emit()  # emit the finished signal when the loop is done

    def stop(self):
        ic('Stopping work')
        self.continue_run = False  # set the run condition to false on stop


class DataSim(QWidget, dsimui.Ui_DataSim):

    def __init__(self):
        super(DataSim, self).__init__()
        self.continue_sim = True
        self.setupUi(self)
        self.retranslateUi(self)
        self.initUI()
        self.initThread()
        self.signal = SimSignal()
        self.signal.sig_sim.connect(self.refresh)

    def initThread(self):
        self.thread = QThread()
        self.worker = Worker(self.refresh)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)

    def initUI(self):
        self.pushButton_addTag.clicked.connect(self.add_tag)
        self.pushButton_remTag.clicked.connect(self.rem_tag)
        self.pushButton_startSim.clicked.connect(self.start_sim)
        self.pushButton_stopSim.clicked.connect(self.stop_sim)
        self.pushButton_refresh.clicked.connect(self.refresh)
        self.comboBox_tagType.activated.connect(self.refresh)

        self.data = self.read_json()
        self.tag_type = 'bools'
        self.tag_temp = {
                "id": 0,
                "name": "tagname",
                "type": "tagtype",
                "range": [0, 0],
                "value": 0
            }
        self.strings = ['ENERGIZED', 'ACTIVE', 'DE-ENERGIZED', 'INACTIVE', 'ON', 'OFF', 'POTATO']

        self.counter = 0

    def testfn(self):
        ic('Cleared')
        self.refresh()

    def clearBrowsers(self):
        try:
            self.textBrowser_tagList.clear()
            self.textBrowser_dataDisp.clear()

        except:
            ic('Didnt work')

    def add_tag(self):
        try:
            data = self.read_json()     # Open data json file

        except:
            ic("Can't open file")

        try:
            tag_ind = len(data[self.tag_type])
            tag_temp = self.tag_temp.copy()
            tag_temp['id'] = tag_ind
            tag_temp['name'] = "tag{}".format(tag_ind)
            tag_temp['type'] = self.tag_type[:-1]

            ic(tag_temp)

        except:
            ic("Can't modify data")

        try:
            if self.tag_type == 'ints' or self.tag_type == 'floats':
                tag_temp['range'] = [0, 999999999]

            elif self.tag_type == 'bools':
                tag_temp['range'] = [0, 1]

            else:
                tag_temp['range'] = self.strings

            data[self.tag_type].append(tag_temp)
            self.write_json(data)
            self.data = data

        except:
            ic("Can't write file")

        self.refresh()

    def refresh(self):
        ic('User Refresh')

        self.tag_type = self.comboBox_tagType.currentText()
        ic(self.tag_type)

        # Populate tagvals structure and assign initial values
        # This is not the JSON tagvals
        for type in self.data:
            for tag in range(len(self.data[type])):
                r_min, r_max = self.data[type][tag]['range']
                if type == 'strings':
                    tag_val = self.strings[random.randint(r_min, r_max - 1)]
                else:
                    tag_val = random.randint(r_min, r_max)
                # ic(type, tag, tag_val)
                self.data[type][tag]['value'] = tag_val

        self.textBrowser_tagList.clear()
        self.textBrowser_dataDisp.clear()

        # Update the text brows tag list with ID and Name
        for tag in self.data[self.tag_type]:
            try:
                tagdata = "id: {}, name: {}, type: {}".format(tag['id'], tag['name'], tag['type'])

            except:
                ic("No data}")
                tagdata = 'None'

            self.textBrowser_tagList.append(tagdata)

        # Update data display
        for tag in self.data[self.tag_type]:
            try:
                tagdata = "name: {}, value: {}".format(tag['name'], tag['value'])

            except:
                ic("No data: {}".format(tagdata))
                tagdata = 'None'

            self.textBrowser_dataDisp.append(tagdata)

        return 'Updated values'

    def rem_tag(self):
        data = self.read_json()
        data[self.tag_type].pop()
        self.write_json(data)
        self.data = data
        self.refresh()

    def start_sim(self):
        ic('start sim')
        self.continue_sim = True

    def stop_sim(self):
        ic('stop sim')
        self.continue_sim = False

    def update_tagvals(self, data, strings, tag_type, tb_tag, tb_data):
        ic('updating data')
        # Populate tagvals structure and assign initial values
        for type in data:
            for tag in range(len(data[type])):
                r_min, r_max = data[type][tag]['range']
                if type == 'strings':
                    tag_val = strings[random.randint(r_min, r_max - 1)]
                else:
                    tag_val = random.randint(r_min, r_max)
                # ic(type, tag, tag_val)
                data[type][tag]['value'] = tag_val

        for tag in data[tag_type]:
            try:
                tagdata = "id: {}, name: {}, type: {}".format(tag['id'], tag['name'], tag['type'])

            except:
                ic("No data}")
                tagdata = 'None'

            tb_tag.append(tagdata)

        # Update data display
        for tag in data[tag_type]:
            try:
                tagdata = "name: {}, value: {}".format(tag['name'], tag['value'])

            except:
                ic("No data: {}".format(tagdata))
                tagdata = 'None'

            tb_data.append(tagdata)

        return 'Updated values'

    def read_json(self):
        with open('tag-list.json', "r") as file:
            json_object = json.load(file)
        return json_object

    def write_json(self, data):
        with open('tag-list.json', "w") as file:
            json.dump(data, file, sort_keys=True, indent=4)


class SimSignal(QObject):
    ''' Why a whole new class? See here:
    https://stackoverflow.com/a/25930966/2441026 '''
    sig_sim = pyqtSignal()


def sim_thread(simclass):
    while True:
        if simclass.continue_sim == True:
            ic("Simulating")
            simclass.signal.sig_sim.emit()
        time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dsm = DataSim()
    t = threading.Thread(target=sim_thread, args=(dsm,))
    t.daemon = True  # otherwise the 'Exit' from the systray menu will not work
    t.start()

    dsm.show()
    app.exec()
