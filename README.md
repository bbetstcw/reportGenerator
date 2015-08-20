# reportGenerator
Generate bugfix and deploy reports from the log file

### Preprocessing
1. The log file can be generated from:

    `git log --encoding GBK --since=2015-07-01 --until=2015-08-01 --stat --name-status | out-file log.txt -Encoding utf8`

2. The encoding mothods under windows are confusing and frustrating. If you get a encoding error, please open the log file, copy the content to a new file, and save the new file with utf8.

3. The script is writen in python 3.4, so please intall at least python 3.0. If you want to edit it with Visual Studio 2013/2015, please install the python plugin for Visual Studio.

4. Input and output file names are hardcoded.

### Output format

1. For bugfix:

	<table border="1">
	<tr>
	<td>Date Report</td>
	<td>Date Fixed</td>
	<td>Service</td>
	<td>Fixed by</td>
	<td>Count</td>
	<td>Issue</td>
</tr>
<tr>
<td>unknown</td>
<td>2015-07-29</td>
<td>Mysql Database: 1m 1- , </td>
<td>Eric Chen</td>
<td>2</td>
<td>content</td>
</tr>
<tr>
<td>unknown</td>
<td>2015-07-29</td>
<td>Mysql Database: 1m , </td>
<td>Eric Chen</td>
<td>1</td>
<td>content</td>
</tr>
<tr>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</table>

2. For deploy:

	<table border="1">
<tr>
<td>Date Modified</td>
<td>Modified by</td>
<td>Type</td>
<td>Services</td>
</tr>
<tr>
<td>2015-07-30</td>
<td>jierong</td>
<td>unknown</td>
<td>Virtual Networks: 2m , Load Balancer: 1+ , </td>
</tr>
<tr>
<td>2015-07-29</td>
<td>Eric Chen</td>
<td>unknown</td>
<td>Mysql Database: 1+ 1m , </td>
</tr>
<tr>
<td>...</td>
<td>...</td>
<td>...</td>
<td>...</td>
</tr>
</table>