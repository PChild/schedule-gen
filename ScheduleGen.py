from multiprocessing import Pool
import subprocess
import os.path
import csv


def genSchedule(teams, rounds, allianceSize, force=False):
    f_name = '_'.join(str(i) for i in [allianceSize, teams, rounds]) + '.csv'
    
    if force or not os.path.isfile(f_name):
        proc = subprocess.Popen(
            ["MatchMaker.exe", "-t", str(teams), "-r", str(rounds), "-b", "-s", "-a", str(allianceSize)],
            stdout=subprocess.PIPE,
            text=True
        )

        with open(f_name, 'w', newline='') as outfile:
            outwriter = csv.writer(outfile, delimiter=',')
            
            for line in proc.stdout:
                if len(line) > 1:
                    outwriter.writerow(line.rstrip().split(' ', 1)[1].split(' '))
            
            outfile.close()
        proc.kill()


def buildStarMapTuples(teamsMin, teamsMax, matchesMin, matchesMax, allianceSize):
    tuplesList = []        
    for teamCnt in range(teamsMin, teamsMax + 1):
        for matchCnt in range(matchesMin, matchesMax + 1):
            tuplesList.append((teamCnt, matchCnt, allianceSize))

    return tuplesList


def main():
    tuplesList = buildStarMapTuples(teamsMin=41, teamsMax=80, matchesMin=1, matchesMax=20, allianceSize=2)
    
    with Pool() as pool:
        pool.starmap(genSchedule, tuplesList)
        
    pool.close()
    pool.join()
        

if __name__ == "__main__":
    main()
    