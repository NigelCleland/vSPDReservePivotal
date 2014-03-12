if exist report.txt                    erase report.txt /q
if exist vSPDcase.inc                  erase vSPDcase.inc /q
if exist runvSPDsetupProgress.txt      erase runvSPDsetupProgress.txt /q
if exist runvSPDsolveProgress.txt      erase runvSPDsolveProgress.txt /q
if exist runvSPDmergeProgress.txt      erase runvSPDmergeProgress.txt /q
if exist runvSPDreportProgress.txt     erase runvSPDreportProgress.txt /q
if exist "Z:\home\nigel\python\vSPDReservePivotal\Programs\..\Output\\SinglePer"      rmdir "Z:\home\nigel\python\vSPDReservePivotal\Programs\..\Output\\SinglePer" /s /q
if exist "Z:\home\nigel\python\vSPDReservePivotal\Programs\\lst"           rmdir "Z:\home\nigel\python\vSPDReservePivotal\Programs\\lst" /s /q
mkdir "Z:\home\nigel\python\vSPDReservePivotal\Programs\..\Output\\SinglePer"
mkdir "Z:\home\nigel\python\vSPDReservePivotal\Programs\\lst"
