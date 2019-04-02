package main

import (
		sp "github.com/scipipe/scipipe"
		spc "github.com/scipipe/scipipe/components"
		)
		
func main() {

wf1 := sp.NewWorkflow("DS_CPSign", 4)

pythonProc1 := wf1.NewProc("pythonProc1", "python3 ../db_targets.py ../database; echo 'done' > {o:donefile}")
pythonProc1.SetOut("donefile", "log1.txt")
wf1.Run()



wf2 := sp.NewWorkflow("DS_CPSign", 4)
targetsDirectory := spc.NewFileGlobber(wf2, "Targets_in_Dir", "*.json")

pythonProc2 := wf2.NewProc("pythonProc2", "python3 ../more_nonbinders.py {i:inpfiles}; echo 'done' > {o:done2file}")
pythonProc2.In("inpfiles").From(targetsDirectory.Out())
pythonProc2.SetOut("done2file", "log2.txt")
wf2.Run()



wf3 := sp.NewWorkflow("DS_CPSign", 4)
targetsDirectory2 := spc.NewFileGlobber(wf3, "Targets_in_Dir2", "*.json")

pythonProc3 := wf3.NewProc("pythonProc3", "python3 ../more_binders.py {i:inpfiles2}; echo 'done' > {o:done3file}")
pythonProc3.In("inpfiles2").From(targetsDirectory2.Out())
pythonProc3.SetOut("done3file", "log3.txt")
wf3.Run()

}