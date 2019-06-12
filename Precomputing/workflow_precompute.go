package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("Forming_Datasets", 4)

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
	

	wf2 := sp.NewWorkflow("Precomputing", 4)

	// Glob balanced target datasets
	globBalancedDatasets := spc.NewFileGlobber(wf2, "glob_balanced_datasets", "./balanced_targets/*.tsv")

	// Precompute Data using CPSign
	precomp := wf2.NewProc("Precompute", `java -jar /home/paat9648/Precompute/cpsign-0.7.8.jar precompute \
												--license /home/paat9648/Precompute/cpsign0x-std-building.license \
												--model-type 1 \
												--train-data {i:traindata} \
												--endpoint "FLAG" \
												--labels [0,1] \
												--duplicates 5 \
												--logfile {o:logout}
												--model-out {o:modelout} \
												--model-name {o:modelname} 2> {o:statusfile} && echo 'Succeeded' > {o:statusfile}; echo 'Foo'`)
	precomp.In("traindata").From(globBalancedDatasets.Out())
	precomp.SetOut("logout", "precomputed/precomp_logfiles/{i:traindata|basename|%.balanced.tsv}.log")
	precomp.SetOut("modelout", "precomputed/{i:traindata|basename|%.balanced.tsv}.precomp")
	precomp.SetOut("modelname", "{i:traindata|basename|%.balanced.tsv}")
	precomp.SetOut("statusfile", "precomputed/process_logfiles/{i:traindata|basename|%.balanced.tsv}.done")

	//Run workflow 2
	wf2.Run()
}


