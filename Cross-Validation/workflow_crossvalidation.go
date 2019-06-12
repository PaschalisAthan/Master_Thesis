package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("Cross_Validating", 4)

	// Glob Precomputed Data
	globPrecomputedData := spc.NewFileGlobber(wf, "glob_precomputed_data", "./precomputed/*.precomp")

	// Crossvalidate Data
	crossval := wf.NewProc("Crossvalidate", `java -jar /home/paat9648/After_mistake/cpsign-0.7.8.jar crossvalidate \
												--license /home/paat9648/After_mistake/cpsign0x-std-building.license \
												--model-in {i:precompdata} \
												--endpoint "FLAG" \
												--labels [0,1] \
												--predictor-type 5 \
												--sampling-strategy 4 \
												--nr-models 10 \
												--seed 1558636145182 \
												--impl 1 \
												-rf 1 \
												--logfile {o:logout} \
												-o {o:resultFile} 2> {o:statusfile} && echo 'Succeeded' > {o:statusfile}; echo 'Foo'`)
	crossval.In("precompdata").From(globPrecomputedData.Out())
	crossval.SetOut("logout", "log_files/{i:precompdata|basename|%.precomp}.log")
	crossval.SetOut("resultFile", "result_files/{i:precompdata|basename|%.precomp}")
	crossval.SetOut("statusfile", "process_logfiles/{i:precompdata|basename|%.precomp}.done")

	//Run workflow 2
	wf.Run()
}


