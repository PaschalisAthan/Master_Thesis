package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("Profiling", 4)

	// Glob Trained Models
	globTrainedModels := spc.NewFileGlobber(wf, "glob_trained_models", "./models/*.cpsign")

	// Glob Files to Predict
	globFilesToPredict := spc.NewFileGlobber(wf, "glob_file_to_predict", "./files_toPredict/*.json")

	// Predict
	predict := wf.NewProc("Predict", `java -jar /Users/paat9648/Desktop/Project/Go/src/cpsign-0.7.8.jar predict \
												--license /Users/paat9648/Desktop/Project/Go/src/cpsign0x-std-building.license \
												--model-in {i:trainedmodel} \
												--predict-file {i:predictFile} \
												--output-format 1 \
												--output {o:resultFile} \
												--logfile {o:logs} 2> {o:statusfile} && echo 'Succeeded' > {o:statusfile}; echo 'Foo'`)

	predict.In("trainedmodel").From(globTrainedModels.Out())
	predict.In("predictFile").From(globFilesToPredict.Out())
	predict.SetOut("resultFile", "results/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}")
	predict.SetOut("logs", "logs/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}.log")
	predict.SetOut("statusfile", "process/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}.done")


	//Run workflow
	wf.Run()
}