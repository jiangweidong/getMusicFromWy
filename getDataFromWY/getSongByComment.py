# encoding: utf-8
import requests
import re
import time
from bs4 import BeautifulSoup
import codecs
import json
from getDataFromWY import loginWY


class speader_main(object):
    def __init__(self):
        self.Default_Header = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate'
        }
        self._session = requests.session()
        self._session.headers.update(self.Default_Header)
        self.BASE_URL = "http://music.163.com"
        self.lsitinfo = []
        self.count = 0
        self.loginwy = loginWY.loginWY()

    def getPlayList(self, pageIndex):
        playListUrl = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%8D%8E%E8%AF%AD&limit=35&offset=" + pageIndex
        playListRes = self._session.get(playListUrl).content
        soup = BeautifulSoup(playListRes, 'html.parser', from_encoding='utf-8')
        playList = soup.findAll('a', href=re.compile(r"/playlist\?id=\d"), class_='msk')
        for i in playList:
            res = self.getPlayListInfo(self.BASE_URL + i['href'])
            if res != 'not':
                print("=======>开始输出html")
                fout = codecs.open('output.html', 'w', 'utf-8')
                fout.write("<html>")
                fout.write("<head><meta http-equiv='content-type' content='text/html;charset=utf8'></head>")
                fout.write("<body>")
                fout.write(
                    "<table width='1080' height='1080' border='1px solid #F00' cellpadding='0' cellspacing='0'>")
                fout.write("<thead>")
                fout.write("<td>歌曲名称</td>")
                fout.write("<td>评论数</td>")
                # fout.write("<td>播放数</td>")
                fout.write("</thead>")
                for data in self.lsitinfo:
                    fout.write("<tr>")
                    fout.write(u"<td><a href='" + data['href'] + "' target='view_window'>%s</a></td>"
                               % (data['name'].encode(encoding='utf-8').decode('utf-8')))
                    fout.write("<td>%s</td>" % data['total'])
                    # fout.write("<td>%s</td>" % data['playcount'].encode(encoding='gbk', errors='strict').decode())
                    fout.write("</tr>")
                fout.write("</table>")
                fout.write("</body>")
                fout.write("</html>")
        pass

    # 获取歌单列表
    def getPlayListInfo(self, href):
        playlistinfo = self._session.get(href).content
        soup = BeautifulSoup(playlistinfo, 'html.parser', from_encoding='utf-8')
        songlist = soup.findAll('a', href=re.compile(r'/song\?id=\d'))
        for i in songlist:
            songinfo = self.getSongInfo(i['href'])
            name = i.get_text()
            if songinfo.get('iscraw') == 'true':
                songinfo['name'] = name
                self.lsitinfo.append(songinfo)
                print("当前抓取==》" + name + "已经抓取=========             " + str(len(self.lsitinfo)) + "     首")
                if len(self.lsitinfo) > 100:
                    return 'begin'
                else:
                    return 'not'
            else:
                print("评论数为======>" + str(songinfo['total']) + "歌曲名为===》" + str(name) + "===============" + str(
                    len(self.lsitinfo)))

        pass

    # 获取歌曲评论
    def getSongInfo(self, songid):
        # commentUrl
        headers = {
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://music.163.com/song?id=' + songid,
            'Cookie': 'appver=1.5.0.75771;',
            'Connection': 'keep-alive'
        }
        songinfo = {}
        song_id = songid[songid.find('=') + 1:]
        commentUrl = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(song_id) + "/?csrf_token="
        data = self.loginwy.loginwy('a1627060419@163.com', '.zcy1314')
        result = requests.post(commentUrl, headers=headers, data=data)
        jsonstr = result.json()['total']
        songinfo['href'] = self.BASE_URL + songid
        songinfo['total'] = jsonstr
        if int(jsonstr) > 20 and int(jsonstr) < 15000:
            print(result.json())
            songinfo['iscraw'] = 'true'
        return songinfo

    # ========================================================
    # 根据发布歌单的人
    def getPlayListForSheet(self, pageIndex):
        playListUrl = "http://music.163.com/discover/playlist/?order=hot&cat=%E6%AC%A7%E7%BE%8E&limit=35&offset=" + pageIndex
        playListRes = self._session.get(playListUrl).content
        soup = BeautifulSoup(playListRes, 'html.parser', from_encoding='utf-8')
        playList = soup.findAll('a', href=re.compile(r"/playlist\?id=\d"), class_='msk')
        for i in playList:
            self.getSignerHomeUrl(self.BASE_URL + i['href'])

            # 获取歌手信息

    def getSignerHomeUrl(self, playListhref):
        playListInfo = self._session.get(playListhref).content
        soup = BeautifulSoup(playListInfo, 'html.parser', from_encoding='utf-8')
        singerList = soup.findAll('a', href=re.compile(r'/user/home\?id=\d'))
        for i in singerList:
            self.getSignerInfo(self.BASE_URL + i['href'])
        pass

    def getSignerInfo(self, href):
        userinfo = self._session.get(href).content
        soup = BeautifulSoup(userinfo, 'html.parser', from_encoding='utf-8')
        fanscount = soup.find('strong', attrs={'id': 'fan_count'}).get_text()
        signerid = href[href.find('=') + 1:]
        if 1000 > int(fanscount):
            self.getrankInfo(signerid)

    def getrankInfo(self, signerid):
        signerurl = 'http://music.163.com/user/songs/rank?id=' + signerid
        usermulist = self._session.get(signerurl).content
        soup = BeautifulSoup(usermulist, 'html.parser', from_encoding='utf-8')
        listlink=soup.find('a',href=re.compile(r'/song\?id=\d'))
        print(listlink)
        pass



if __name__ == "__main__":
    sm = speader_main()
    for i in range(0, 41):
        sm.getPlayList(str(i * 35))  # 根据评论数量

    # for i in range(0, 41):
    #         sm.getPlayListForSheet(str(i * 35))
