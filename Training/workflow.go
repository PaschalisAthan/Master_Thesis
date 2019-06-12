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
	

	wf2 := sp.NewWorkflow("Training_Models", 4)

	// Glob balanced target datasets
	globBalancedDatasets := spc.NewFileGlobber(wf2, "glob_balanced_datasets", "./balanced_targets/*.tsv")

	// Train Models using CPSign
	trainModels := wf2.NewProc("train_models", `java -jar /Users/paat9648/Desktop/Desk/Project/CPSign/cpsign-0.7.8.jar train \
												--license /Users/paat9648/Desktop/Desk/Project/CPSign/cpsign0x-std-building.license \
												--train-data {i:traindata} \
												--endpoint "FLAG" \
												--labels [0,1] \
												--predictor-type 5 \
												--sampling-strategy 4 \
												--nr-models 10 \
												--impl 2 \
												--duplicates 5 \
												--logfile {o:logfile} \
												--model-out {o:modelout} \
												--model-name {o:modelname} 2> {o:statusfile} && echo 'Succeeded' > {o:statusfile}; echo 'Foo'`)
	trainModels.In("traindata").From(globBalancedDatasets.Out())
	trainModels.SetOut("logfile", "training_log/{i:traindata|basename|%.balanced.tsv}.log")
	trainModels.SetOut("modelout", "models/{i:traindata|basename|%.balanced.tsv}.cpsign")
	trainModels.SetOut("modelname", "{i:traindata|basename|%.balanced.tsv}")
	trainModels.SetOut("statusfile", "models/log_files/{i:traindata|basename|%.balanced.tsv}.done")

	//Run workflow 2
	wf2.Run()
}


