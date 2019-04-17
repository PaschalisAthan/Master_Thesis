package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("DS_CPSign", 4)

	// Create target datasets
	pythonProc1 := wf.NewProc("Proc1", "python3 ../db_targets.py ../database ../targets_folder; echo 'done' > {o:donefile}")
	pythonProc1.SetOut("donefile", "log1")

	// Glob target datasets
	targetsDirectory := spc.NewFileGlobberDependent(wf, "Targets_in_Dir", "./targets_folder/*.json")
	targetsDirectory.InDependency().From(pythonProc1.Out("donefile"))

	// Balance datasets
	pythonProc2 := wf.NewProc("Proc2", "python3 ../balancing_targets.py {i:inpfiles} ../targets_folder; echo 'done' > {o:done2file}")
	pythonProc2.In("inpfiles").From(targetsDirectory.Out())
	pythonProc2.SetOut("done2file", "{i:inpfiles|%.json}_done")

	wf.Run()
}
