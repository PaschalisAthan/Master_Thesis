package main

import (
	sp "github.com/scipipe/scipipe"
	spc "github.com/scipipe/scipipe/components"
)

func main() {
	wf := sp.NewWorkflow("Editing File", 4)

	// Glob file to predict
	globPredictFile := spc.NewFileGlobber(wf, "glob_pred_file", "*.csv")

	// Change the form of the predicting dataset to a correct one
	changeForm := wf.NewProc("Change_Form", "python3 ../pred_file.py --in_file={i:inputFile} --outp_smiles={o:outputFile}")
	changeForm.In("inputFile").From(globPredictFile.Out())
	changeForm.SetOut("outputFile", "files_toPredict/{i:inputFile|basename|%.csv}.tsv")


	wf.Run()


	wf1 := sp.NewWorkflow("Profiling", 4)

	// Glob Trained Models
	globTrainedModels := spc.NewFileGlobber(wf1, "glob_trained_models", "./models/*.cpsign")

	// Glob Files to Predict
	globFilesToPredict := spc.NewFileGlobber(wf1, "glob_file_to_predict", "./files_toPredict/*.tsv")

	// Add a combinator that ensures all combinations of the files on the
	// incoming streams are created and sent to the downstream process
	combineGlobbers := spc.NewFileCombinator(wf1, "combine_globbers")
	combineGlobbers.In("models").From(globTrainedModels.Out())
	combineGlobbers.In("datasets").From(globFilesToPredict.Out())

	// Predict
	predict := wf1.NewProc("Predict", `java -jar /Users/paat9648/Desktop/Desk/Project/CPSign/cpsign-0.7.8.jar predict \
												--license /Users/paat9648/Desktop/Desk/Project/CPSign/cpsign0x-std-building.license \
												--model-in {i:trainedmodel} \
												--predict-file {i:predictFile} \
												--output-format 1 \
												--output {o:resultFile} \
												--logfile {o:logs} 2> {o:statusfile} && echo 'Succeeded' > {o:statusfile}; echo 'Foo'`)

	predict.In("trainedmodel").From(combineGlobbers.Out("models"))
	predict.In("predictFile").From(combineGlobbers.Out("datasets"))
	predict.SetOut("resultFile", "results/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}")
	predict.SetOut("logs", "logs/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}.log")
	predict.SetOut("statusfile", "process/{i:predictFile|basename|%_smiles.json}/{i:trainedmodel|basename|%.cpsign}.done")

	//Run workflow
	wf1.Run()
}