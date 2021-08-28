import re


class App:
    def __init__(self):
        self.spamorham = dict()
        self.messages = dict()
        self.words = list()
        self.wordcounts = dict()
        self.NUMOFMESSAGES = 0
        self.ids = list()
        self.load_data()
        self.print_data()
        self.create_cluster()

    def load_data(self):  # Loads data from 'SMSSpamCollection.txt'
        """ This method is used to load the SMS data from SMSSPAMCollection file. """
        with open('SMSSpamCollection.txt') as sms_data:
            i = 0
            for line in sms_data:
                line = line.split("\t")
                message_id = "SMS" + str(i)
                self.spamorham[message_id] = line[0]
                self.messages[message_id] = line[1].strip()
                self.ids.append(message_id)
                self.wordcounts[message_id] = self.split_messages(line[1])
                i += 1
            self.NUMOFMESSAGES = i

    def split_messages(self, line):
        """ This method is used to split sentences into words from messages in the data. """
        count = [0] * len(self.words)
        words = re.compile(r'[^A-Z^a-z]+').split(line)
        for word in words:
            word = word.lower()
            if word not in self.words:
                self.words.append(word)
                count.append(1)
            else:
                for i in range(len(count)):
                    if self.words[i] == word:
                        count[i] += 1
                        break
            return count

    def print_data(self):
        """ This method is used to create a new dataset file named 'present_data.txt' using
            data that comes from specified path. """
        dataset = open('present_data.txt', 'w')
        header = 'Messages  '
        i = 0
        for _ in self.words:
            header += "word" + str(i) + '   '
            i += 1
        dataset.write(header)
        n = 0
        for _ in self.messages:
            i_d = self.ids[n]
            line = i_d + '\t\t'
            for count in self.wordcounts[i_d]:
                line += str(count) + '\t\t'
            for j in range(len(self.words) - len(self.wordcounts[i_d])):
                self.wordcounts[i_d].append(0)
                line += str(0) + '\t\t'
            n += 1
            dataset.write(line)
        dataset.close()

    def create_cluster(self):
        pass
        # messages, words, data = clusters.readfile('C:/Users/Sinan/PycharmProjects/ENGR-102/MP3/present_data.txt')
        # kclust = clusters.kcluster(data, k=2)
        # self.print_cluster(kclust[0], 'first')
        # self.print_cluster(kclust[1], 'second')

    def print_cluster(self, cluster, value):
        """ This method is used to print clusters created from the data loaded. """
        total = 0
        ham = 0
        spam = 0
        for message in cluster:
            if self.spamorham[self.ids[message]] == 'ham':
                ham += 1
            elif self.spamorham[self.ids[message]] == 'spam':
                spam += 1
            else:
                print("ERROR!")
            total += 1

        print("Total number of messages in the {0} cluster: {1}\n"
              "Percentage of SPAM messages in the {2} cluster: {3}\n"
              "Percentage of HAM messages in the {4} cluster: {5}".format(value, total, value,
                                                                          str((float(spam) / total) * 100), value,
                                                                          str((float(ham) / total) * 100)))


if __name__ == '__main__':
    app = App()
