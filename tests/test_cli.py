import quakeio
from quakeio.__main__ import main
import subprocess


def test_summarize_zip():
    main(["-S", "dat/58658_007_20210426_10.09.54.P.zip"])

def test_rotate():
    p = subprocess.Popen([
            "quakeio", 
            "-r", "2.0", 
            "-m", "station_channel=20",
            "dat/58658_007_20210426_10.09.54.P.zip"
        ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
    )

    #stdout,stderr = p.communicate()
    motion = quakeio.read(p.stdout, format="json")
    print(len(list(motion.keys())))

if __name__=="__main__":
    #test_summarize_zip()
    test_rotate()
