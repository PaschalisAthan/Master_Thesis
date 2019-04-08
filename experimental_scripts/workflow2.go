package main

import (
		sp "github.com/scipipe/scipipe"
		spc "github.com/scipipe/scipipe/components"
		)
		
func main() {

wf := sp.NewWorkflow("DS_CPSign", 4)

pythonProc1 := wf.NewProc("pythonProc1", "python3 ../db_targets.py ../database; echo 'done' > {o:donefile}")
targetsDirectory := spc.NewFileGlobberDependent(wf, "Targets_in_Dir", "*.json")
pythonProc2 := wf.NewProc("pythonProc2", "python3 ../more_nonbinders.py {i:inpfiles}; echo 'done' > {o:done2file}")
targetsDirectory2 := spc.NewFileGlobberDependent(wf, "Targets_in_Dir2", "*.json")
pythonProc3 := wf.NewProc("pythonProc3", "python3 ../more_binders.py {i:inpfiles2}; echo 'done' > {o:done3file}")

pythonProc1.SetOut("donefile", "log1.txt")
targetsDirectory.InDependency().From(pythonProc1.Out("donefile"))
pythonProc2.In("inpfiles").From(targetsDirectory.Out())
pythonProc2.SetOut("done2file", "log2.txt")
targetsDirectory2.InDependency().From(pythonProc2.Out("done2file"))
pythonProc3.In("inpfiles2").From(targetsDirectory2.Out())
pythonProc3.SetOut("done3file", "log3.txt")

wf.Run()
}