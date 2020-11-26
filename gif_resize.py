import subprocess
def resize_gif(path, save_as=None, quality=75):
    if not save_as:
        save_as = path
    subprocess.run(['gif2webp',path,'-o',save_as,'-q',str(quality)])











