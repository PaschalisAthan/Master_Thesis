package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("DS_CPSign", 4)

	// Create target datasets
	createDatasets := wf.NewProc("create_datasets", "python3 ../db_targets.py --database=../database --outdir={o:outdir}")
	createDatasets.SetOut("outdir", "targets_folder")

	// Glob target datasets
	globDatasets := spc.NewFileGlobberDependent(wf, "glob_datasets", "./targets_folder/*.json")
	globDatasets.InDependency().From(createDatasets.Out("outdir"))

	// Balance datasets
	balanceDatasets := wf.NewProc("balance_datasets", "python3 ../balancing_targets.py {i:inpfiles} ../targets_folder; echo 'done' > {o:done2file}")
	balanceDatasets.In("inpfiles").From(globDatasets.Out())
	balanceDatasets.SetOut("done2file", "{i:inpfiles|%.json}.done")

	wf.Run()
}
