!python -m pip install --upgrade pip setuptools wheel
!python -m pip install lbry-libtorrent
#https://anonymiz.com/magnet2torrent/
import libtorrent as lt
from google.colab import drive
from google.colab import files
ses = lt.session()
ses.listen_on(6881, 6891)
downloads = []
drive.mount('/content/drive')
magnet_link = input("Enter Magnet Link Or just hit enter uploading torrent: ")
if magnet_link.lower() == "":
  source = files.upload()
  params = {
      "save_path": "/content/drive/My Drive/Torrent",
      "ti": lt.torrent_info(list(source.keys())[0]),
  }
  downloads.append(ses.add_torrent(params))
else :
  params = {"save_path": "/content/drive/My Drive/Torrent"}
  downloads.append(lt.add_magnet_uri(ses, magnet_link, params))

import time
from IPython.display import display
import ipywidgets as widgets

state_str = [
    "queued",
    "checking",
    "downloading metadata",
    "downloading",
    "finished",
    "seeding",
    "allocating",
    "checking fastresume",
]

layout = widgets.Layout(width="auto")
style = {"description_width": "initial"}
download_bars = [
    widgets.FloatSlider(
        step=0.01, disabled=True, layout=layout, style=style
    )
    for _ in downloads
]
display(*download_bars)

while downloads:
    next_shift = 0
    for index, download in enumerate(downloads[:]):
        bar = download_bars[index + next_shift]
        if not download.is_seed():
            s = download.status()

            bar.description = " ".join(
                [
                    download.name(),
                    str(s.download_rate / 1000),
                    "kB/s",
                    state_str[s.state],
                ]
            )
            bar.value = s.progress * 100
        else:
            next_shift -= 1
            ses.remove_torrent(download)
            downloads.remove(download)
            bar.close() # Seems to be not working in Colab (see https://github.com/googlecolab/colabtools/issues/726#issue-486731758)
            download_bars.remove(bar)
            print(download.name(), "complete")
    time.sleep(1)

