package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("DS_CPSign", 4)

	// Create target datasets
	createDatasets := wf.NewProc("create_datasets", "python3 ../db_targets.py --database=../database --outdir={o:outdir}")
	createDatasets.SetOut("outdir", "all_targets")

	// Glob target datasets
	globDatasets := spc.NewFileGlobberDependent(wf, "glob_datasets", "./all_targets/*.tsv")
	globDatasets.InDependency().From(createDatasets.Out("outdir"))

	// Balance datasets
	balanceDatasets := wf.NewProc("balance_datasets", "python3 ../balancing_targets.py --dbfile=../database --infile={i:infile} --outfile={o:outfile} --nonbinders-dir={o:nonbinders_dir}")
	balanceDatasets.In("infile").From(globDatasets.Out())
	balanceDatasets.SetOut("outfile", "balanced_targets/{i:infile|basename|%.tsv}.balanced.tsv")
	balanceDatasets.SetOut("nonbinders_dir", "only_non_binding_targets")

	// Run workflow
	wf.Run()
}
