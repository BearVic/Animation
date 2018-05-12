import re
import urllib.request
import os

def main():

    if not os.path.exists('data'):
        os.mkdir('data')
    os.chdir('data')

    mocap_url = "http://mocap.cs.cmu.edu/search.php?subjectnumber=%&motion=%"
    response = urllib.request.urlopen(mocap_url)
    mocap_html = response.read().decode('utf-8')
    # print(type(mocap_html))
    # print("raw html length:", len(mocap_html))
    # print(mocap_html[:1000])

    subjects = findAllSubjects(mocap_html)

    for subject in subjects[-2:]:
        downloadASFandAMC(subject)

    print("done!")
    

def findAllSubjects(html):
    subject_pattern = r'<TD COLSPAN=3><CENTER>Subject (.*?)<TR BGCOLOR=#909090>'
    subjects = re.findall(subject_pattern, html, re.S|re.M)

    last_pat = r'Subject #144(.*?)</TD></TR>'
    last_sub = re.findall(last_pat, html, re.S|re.M)

    last_sub[0] = '#144' + last_sub[0]

    subjects.append(last_sub[0])
    
    # print("subjects type: ", type(subjects))
    # print("subjects len: " ,len(subjects))

    return subjects

def downloadASFandAMC(html):
    name_index_pattern = r'#(\d+) \((.*?)\) <A HREF=(.*?)>file index</A>'
    name_index = re.findall(name_index_pattern, html, re.S)
    if not name_index:
        return

    no = name_index[0][0]
    name = no + name_index[0][1].strip().replace('(','#')
    index_url = "http://mocap.cs.cmu.edu" + name_index[0][2]

    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)

    downloadFile(index_url, name+'.txt')

    asf_pattern = r'<A HREF="(.*?)">asf</A>'
    asf_url = re.findall(asf_pattern, html, re.S)
    # print(type(asf_url))
    # print(asf_url)
    downloadFile(asf_url[0], name+'.asf')

    print("Subject:", name)

    amcs_pattern = r'<TR BGCOLOR=#(.*?)Feedback'
    amcs = re.findall(amcs_pattern, html, re.S|re.M)
    for amc in amcs:
        downloadAMC(amc)

    os.chdir('..')

def downloadFile(url, name):
    response = urllib.request.urlopen(url)
    file = response.read().decode('utf-8')
    temp = url.split('/')[-1]
    temp = temp.split('.')[0]
    name = temp + '$' + name.replace('/','')
    with open(name, "w") as f:
        f.write(file)
        f.close()

def downloadAMC(html):
    no_name_url_frame_pattern = r'<TD>(\d+)</TD><TD>(.*?)</TD><TD><A(.*?)>c3d</A></TD><TD><A HREF="(.*?)">amc<(.*?)<TD>(\d+)</TD>'
    res = re.findall(no_name_url_frame_pattern, html, re.S|re.M)
    if not res:
        return

    # print(res)

    no = res[0][0]
    name = res[0][1]
    url = res[0][3]
    frame = res[0][5]
    downloadFile(url, no+'#'+frame+'#'+name+'.amc')
    # print(no+'#'+frame+'#'+name+'.amc')
    # print(url)

    print("amc:", no)

def test():
    content = '<TD></TD><TD>10</TD><TD>playground - climb, swing, lean back, drop</TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_10.tvd">tvd</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_10.c3d">c3d</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_10.amc">amc</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_10.mpg">mpg</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_10.avi">Animated</A></TD><TD>120</TD><TD><A HREF="badtrial.php?subjectnumber=1&motion=10">'
    content1 = '<TD></TD><TD>1</TD><TD>nursery rhyme - "I\'m a little teapot..."</TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/25/25_01.tvd">tvd</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/25/25_01.c3d">c3d</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/25/25_01.amc">amc</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/25/25_01.mpg">mpg</A></TD><TD></TD><TD>120</TD><TD><A HREF="badtrial.php?subjectnumber=25&motion=1">Feedback</A></TD></TR>          <TR><TD COLSPAN=3><BR></TD></TR>'
    content2 = '<TD></TD><TD>1</TD><TD>playground - forward jumps, turn around</TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_01.tvd">tvd</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_01.c3d">c3d</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_01.amc">amc</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_01.mpg">mpg</A></TD><TD><A HREF="http://mocap.cs.cmu.edu:80/subjects/01/01_01.avi">Animated</A></TD><TD>120</TD><TD><A HREF="badtrial.php?subjectnumber=1&motion=1">'
    downloadAMC(content)

    # downloadFile(index_url, name+'.txt')
    # print(name, index_file)

if __name__=='__main__':
    # test()
    main()
