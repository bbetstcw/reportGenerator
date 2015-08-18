from datetime import datetime
import re

class Commit:
    def __init__(self, sha, author, date, message, files_involved):
        self.sha = sha
        self.author = author
        self.date = date
        self.message = message
        self.files_involved = files_involved
        self.type = None
        self.reportedDate = None
        self.services = None
        self.deployType = None

    def __str__(self):
        result = "commit " + self.sha + "\n" +\
               "Author: " + str(self.author) +"\n" +\
               "Date: " + datetime.strftime(self.date, "%a %b %d %H:%M:%S %Y %z") + "\n" +\
               "\n" +\
               "    " + str(self.message) + '\n'
        for file in self.files_involved:
            result += str(file) + '\n'
        return result

    def getType(self):
        if self.type==None:
            self.type='unknown'

        return self.type

    def getReportedDate(self):
        if self.reportedDate == None:
            self.reportedDate = 'unknown'
        return self.reportedDate

    def getServices(self):

        return self.services

    def getDeployType(self):

        return self.deployType


class Author:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return self.name + " <" + self.email+">"

class Message:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __str__(self):
        return self.title + '\n' + self.description

class File_involved:
    def __init__(self, type, path):
        self.type = type
        self.path = path

    def __str__(self):
        return self.type + '\t' + self.path


def initStat():
    bugFixOutput.writelines('<table border="1">\n' +\
	                            '<tr>\n' +\
		                        '<td>Date Report</td>\n' +\
		                        '<td>Date Fixed</td>\n' +\
		                        '<td>Service</td>\n' +\
		                        '<td>Fixed by</td>\n' +\
		                        '<td>Count</td>\n' +\
		                        '<td>Issue</td>\n' +\
	                        '</tr>\n')
    deployOutput.writelines('<table border="1">\n' +\
	                            '<tr>\n' +\
		                        '<td>Date Modified</td>\n' +\
		                        '<td>Modified by</td>\n' +\
		                        '<td>Type</td>\n' +\
		                        '<td>Services</td>\n' +\
	                        '</tr>\n')

def getStat(commit):
    commitType = commit.getType()
    if commitType=='bugfix':
        bugFixOutput.writelines('<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%d</td>\n<td>%s</td>\n</tr>\n' % (commit.getReportedDate(), datetime.strftime(commit.date, "%Y-%m-%d"), commit.getServices(), commit.author.name, len(commit.files_involved), "content"))
    elif commitType=='deploy':
        deployOutput.writelines('<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n' % (datetime.strftime(commit.date, "%Y-%m-%d"), commit.author.name, commit.getDeployType(), commit.getServices()))
    elif commitType=='unknown':
        print(commit)

def closeStat():
    bugFixOutput.writelines("</table>")
    deployOutput.writelines("</table>")

def handleLogFile(logFile):
    initStat()
    line = logFile.readline()
    while line!='':
        if line[:6]=='commit':
            sha = line[6:].strip()
            line = logFile.readline()
            if line[:6]=='Merge:':
                line = logFile.readline()
                continue
            else:
                author = Author(line[7:line.index('<')-1].strip(), line[line.index('<')+1:line.index('>')])
                line = logFile.readline()
                date = datetime.strptime(line[5:].strip(), "%a %b %d %H:%M:%S %Y %z")
                line = logFile.readline()
                line = logFile.readline()
                if line[:4]=='    ':
                    message_title = line.strip()
                else:
                    print(line)
                line = logFile.readline()
                message_description = ''
                while line[:4]=='    ':
                    message_description += line
                    line = logFile.readline()
                message = Message(message_title, message_description)
                line = logFile.readline()
                files_involved = []
                while line!='' and (line[0]=='A' or line[0]=='M' or line[0]=='D'):
                    files_involved.append(File_involved(line[0], line[1:].strip()))
                    line = logFile.readline()
                commit = Commit(sha, author, date, message, files_involved)
                getStat(commit)
        else:
            line = logFile.readline()
    closeStat()

logFile = open('log.txt', 'r')
bugFixOutput = open('bugFix.html', 'w')
deployOutput = open('deploy.html', 'w')
handleLogFile(logFile)
bugFixOutput.close()
deployOutput.close()
logFile.close()
