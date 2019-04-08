package main

import (
		sp "github.com/scipipe/scipipe"
		spc "github.com/scipipe/scipipe/components"
		)
		
func main() {

wf := sp.NewWorkflow("DS_CPSign", 4)

pythonProc1 := wf.NewProc("pythonProc1", "python3 ../script1_2.py ../database; echo 'done' > {o:donefile}")
targetsDirectory := spc.NewFileGlobberDependent(wf, "Targets_in_Dir", "*.json")
pythonProc2 := wf.NewProc("pythonProc2", "python3 ../delete_nonbinders_2.py {i:inpfiles}; echo 'done' > {o:done2file}")


pythonProc1.SetOut("donefile", "log1.txt")
targetsDirectory.InDependency().From(pythonProc1.Out("donefile"))
pythonProc2.In("inpfiles").From(targetsDirectory.Out())
pythonProc2.SetOut("done2file", "done2file.txt")

wf.Run()


wf2 := sp.NewWorkflow("DS_CPSign2", 4)

targetsDirectory2 := spc.NewFileGlobber(wf2, "Targets_in_Dir2", "*.json")
pythonProc3 := wf2.NewProc("pythonProc3", "python3 ../add_nonbinders_2.py {i:inpfiles2}; echo 'done' > {o:done3file}")

pythonProc3.In("inpfiles2").From(targetsDirectory2.Out())
pythonProc3.SetOut("done3file", "{i:inpfiles2|%.json}_done2.txt")

wf2.Run()
}