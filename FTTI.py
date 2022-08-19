import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage
import requests
import argparse
import sys
import os

styleDict = ["油画","水彩画","卡通","粉笔画","儿童画","蜡笔画"]

imglist = ['https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0ceex', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cei4', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0ce5q', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0ce30', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cev9', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cea2', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cebf', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cems', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0ceu7', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/efb2f442f09a5e19aeeb22de8971b0cect']

class MV:
    def __init__(self):
        pass
        
    def getImageDict(self, text):
        input_dict = {
            "text": text,
            "style": self.style,
        }
        return TextToImage.create(**input_dict)

    def readAndSave(self, imgDict, text=None, ind=0):
        for index, url in enumerate(imgDict['imgUrls']):
            r = requests.get(url)
            imgName = ""
            if text is None:
                imgName = imgName + url.split('/')[-1]+'.png'
            else:
                imgName = imgName + str(ind) + "_" + text + "_" + str(index) + '.png'
            out_ii = os.path.join(self.songName , imgName)
            with open(out_ii, 'wb') as f:
                f.write(r.content)
            f.close()

    def make(self, lrc=None, songName=None, style=0, startindex=0):
        if style < 6 and style >= 0:
            self.style = styleDict[style]
        else:
            try:
                sys.exit(0)
            except:
                print("Wrong Style")

        self.lrcs = []

        if os.path.exists(lrc):
            with open(lrc, 'r', encoding='UTF-8') as fp:
                lines = fp.readlines()
                for line in lines:
                    self.lrcs.append(line)
        else:
            self.lrcs.append(lrc)

        print(self.lrcs)

        if songName is not None:
            self.songName = songName
        else:
            if os.path.exists(lrc):
                self.songName = os.path.basename(lrc).split(".")[0]
            else:
                self.songName = lrc
        os.makedirs(self.songName, exist_ok=True)
        
        for index, txt in enumerate(self.lrcs):
            print(index, txt)
            if index >= startindex:
                textlist = txt.split("@:")
                if len(textlist) > 1 and textlist[-1] is not '':
                    txt = textlist[-1]
                txt = txt.replace("\n", "")
                idict = self.getImageDict(txt)
                self.readAndSave(idict, text=txt, ind=index)

wenxin_api.ak = "********************************"
wenxin_api.sk = "********************************"

mv = MV()

def main(args):
    mv.make(args.lrc, args.songName, args.style, args.startindex)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lrc', type=str, required=True)
    parser.add_argument('--songName', type=str, required=False)
    parser.add_argument('--style', type=int, default=0, required=False)
    parser.add_argument('--startindex', type=int, default=0, required=False)
    args = parser.parse_args()
    main(args)