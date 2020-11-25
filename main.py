import os
import time
from stat import ST_MTIME
from gif_resize import resize_gif
import shutil
import sys
import getopt

whatsAppPath = './wa-sticker'
pathToStickers = './stickers'
duration = 3600


def getRecentStickerFiles(duration=3):
    if(not whatsAppPath or not os.path.exists(whatsAppPath)):
        raise ValueError('input whatsapp directory doesnt exist!')
    recentFiles = []
    recentDuration = time.time()
    for file in os.listdir(whatsAppPath):
        try:
            st = os.stat(os.path.join(whatsAppPath, file))
        except Exception as e:
            print('[!] couldnt get the file info,skipping ', file)
        else:
            lastModified = st[ST_MTIME]
            if((recentDuration - lastModified) < duration):
                recentFiles.append(file)
    return recentFiles


def replaceWithSticker(listOfFiles, pathToStickers='./stickers', resize_to=(512, 512)):
    if(not os.path.exists(pathToStickers)):
	   	raise ValueError('input Stickers directory doesnt exist!')
    stickers = os.listdir(pathToStickers)
    print('[!] found {} stickers to add'.format(min(len(stickers), len(listOfFiles))))
    for file in zip(stickers, listOfFiles):
        copy_From = os.path.join(pathToStickers, file[0])
        copy_To = os.path.join(whatsAppPath, file[1])
        print('[+] adding {} to Whatsapp Sticker'.format(file[0]))
        if(os.path.splitext(copy_From)[1] == '.gif'):
            resize_gif(copy_From, copy_To, resize_to=resize_to)
        elif(os.path.splitext(copy_From)[1] == '.webp'):
            shutil.copyfile(copy_From, copy_To)
        else:
            print('[-] format doesnt match ! skipping ', file[0])


def main(argv):
    global duration,pathToStickers,whatsAppPath
    help_msg = 'Usage: python main.py -s <path-to-sticker-folder> -w <path-to-whatsapp-folder> -t <time-in-seconds>'
    try:
        opts, args = getopt.getopt(argv,"hs:w:t:",["stdir=","wadir=","time"])
    except getopt.GetoptError:
        print(help_msg)
    for opt,arg in opts:
        if(opt=='-h'):
            print(help_msg)
            sys.exit()
        if(opt in ["-s","--stdir="]):
            pathToStickers = arg
            continue
        if(opt in ['-w','--wadir=']):
            whatsAppPath = arg
            continue
        if(opt in ['-t','--time=']):
            duration = int(arg)

    print('Parameters set to -- \n Whatsapp Folder -> {} \n Sticker Folder >- {} \n Time -> {}s'.format(whatsAppPath,pathToStickers,duration))
    usr = input('this will replace recent whatsapp stickers with new one , still want to do this? (y|Y to continue) ')
    if(usr.lower()=='y'):
        replaceWithSticker(getRecentStickerFiles(duration=duration),pathToStickers=pathToStickers)


if __name__ == '__main__':
    main(sys.argv[1:])
