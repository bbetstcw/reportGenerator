from datetime import datetime
import re

class Commit:
    BUGFIX_KEYWORD = ['fix', 'bug', '修复', '解决', '处理', 'handle', 'broken link', '错误', '清除'];
    DEPLOY_KEYWORD = ['refresh', '更新', '添加', 'add', '增加', '新增', 'update', 'updating', ];
    REPORTED_DATE_REGS = [r".*根据.*((?P<year>[0-9]{4})年)?(?P<month>[0-9]{1,2})月(?P<day>[0-9]{1,2})日.*",
                          r".*((?P<year>[0-9]{4})年)?(?P<month>[0-9]{1,2})月(?P<day>[0-9]{1,2})日.*提[到|及|出].*"]

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
            m = re.match(r"\[(?P<commitType>[a-z]+)\]-(?P<message>.+)", self.message.title, re.I)
            if m == None:
                self.__fuzzyGetType()
            else:
                md = m.groupdict()
                self.type = md["commitType"].strip().lower()
        return self.type

    def __fuzzyGetType(self):
        for keyword in Commit.BUGFIX_KEYWORD:
            if re.match(r'.*'+keyword+'.*', self.message.title, re.I):
                self.type = 'bugfix'
                return

        for keyword in Commit.DEPLOY_KEYWORD:
            if re.match(r'.*'+keyword+'.*', self.message.title, re.I):
                self.type = 'deploy'
                return
        self.type = 'unknown'

    def getReportedDate(self):
        if self.reportedDate == None:
            m = re.match(r"\[(?P<commitType>[a-z]+)\]-(?P<date>[0-9]{4}\/[0-9]{2}\/[0-9]{2})-(?P<message>.+)", self.message.title, re.I)
            if m == None:
                self.__fuzzyGetReportedDate()
            else:
                md = m.groupdict()
                self.type = md["commitType"]
                self.reportedDate = datetime.strptime(md["date"], "%Y/%m/%d")
        return self.reportedDate
    
    def __fuzzyGetReportedDate(self):
        for reg in Commit.REPORTED_DATE_REGS:
            m = re.match(reg, self.message.description.replace("\n", " "))
            if m!=None:
                dict = m.groupdict()
                if dict["year"]==None:
                    year = self.date.year
                else:
                    year = int(dict["year"])
                month = int(dict["month"])
                day = int(dict["day"])
                self.reportedDate = datetime(year, month, day)
                return

    def getServices(self):
        if self.services == None:
            self.services = {};
            for file in self.files_involved:
                service = file.getServiceInvolved();
                if service == 'unknown':
                    continue;
                if service not in self.services.keys():
                    self.services[service] = ServiceInvolved(service)
                self.services[service].addFile(file)
        return self.services

    def getDeployType(self):
        if self.deployType == None:
            self.deployType = 'unknown'
        return self.deployType


class ServiceInvolved:

    def __init__(self, name):
        self.name = name
        self.added = 0
        self.modified = 0
        self.deleted = 0

    def __str__(self):
        result = self.name+": "
        if self.added>0:
            result += str(self.added) + "+ "
        if self.modified>0:
            result += str(self.modified) + "m "
        if self.deleted>0:
            result += str(self.deleted) + "- "
        return result

    def addFile(self, file):
        if file.type == "A":
            self.added+=1;
        elif file.type == "D":
            self.deleted+=1;
        elif file.type == "M":
            self.modified+=1


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
    FULL_SERVICE_LIST = {"active-directory":"AD","api-management":"API Management","application-gateway":"Application Gateway",
                         "architecture":"Architecture","automation":"Automation","backup":"Backup","cache":"Cache","cdn":"CDN",
                         "cloud-services":"Cloud Services","hdinsight":"HD Insight","insights":"HD Insight","azure-sdk":"Azure SDK",
                         "media-services":"Media Services","mobile-services":"Mobile Services","mysql-database":"Mysql Database",
                         "notification-hubs":"Notification Hubs","scheduler":"Scheduler","service-bus":"Service Bus",'powershell':"Powershell",
                         "site-recovery":"Site Recovery","sql-database":"SQL Database","storage":"Storage","load-balancer":"Load Balancer",
                         "traffic-manager":"Traffic Manager","virtual-machines":"Virtual Machines","resources":"Resources","vpn-gateway":"VPN gateway",
                         "virtual-networks":"Virtual Networks","web-sites":"Web Sites","websites":"Web Sites","xplat":"Xplat","biztalk":"Biztalk"}
    SECONDARY_KEY_WORD = {"web-site":"Web Sites","cloud-service":"Cloud Services","virtual-network":"Virtual Network",
                          "networking":"Virtual Network","service-bus":"Service Bus","scheduler":"Scheduler",
                          "virtual-machine":"Virtual Machines","mobile-services":"Mobile Services","active-directory":"AD",
                          "storage":"Storage","mysql":"Mysql Database", "example":"Example"}
    def __init__(self, type, path):
        self.type = type
        self.path = path

    def __str__(self):
        return self.type + '\t' + self.path

    def getServiceInvolved(self):
        for k,v in File_involved.FULL_SERVICE_LIST.items():
            m = re.match(r'.*\/'+k+'.*\.md', self.path, re.I)
            if m!=None:
                return v
        for k,v in File_involved.SECONDARY_KEY_WORD.items():
            m = re.match(r'.*'+k+'.*\.md', self.path, re.I)
            if m!=None:
                return v
        return "unknown"


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
        services = ""
        for service in commit.getServices().values():
            services += str(service)+", "
        reportedDate = commit.getReportedDate()
        if reportedDate == None:
            dateString = "unknown"
        else:
            dateString = datetime.strftime(reportedDate, "%Y-%m-%d")
        bugFixOutput.writelines('<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%d</td>\n<td>%s</td>\n</tr>\n' % (dateString, datetime.strftime(commit.date, "%Y-%m-%d"), services, commit.author.name, len(commit.files_involved), "content"))
    elif commitType=='deploy':
        services = ""
        for service in commit.getServices().values():
            services += str(service)+", "
        deployOutput.writelines('<tr>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n<td>%s</td>\n</tr>\n' % (datetime.strftime(commit.date, "%Y-%m-%d"), commit.author.name, commit.getDeployType(), services))
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
bugFixOutput = open('bugFix.md', 'w')
deployOutput = open('deploy.md', 'w')
handleLogFile(logFile)
bugFixOutput.close()
deployOutput.close()
logFile.close()
