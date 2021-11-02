from icecream import ic

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