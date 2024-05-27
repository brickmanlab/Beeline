import glob
import os
import warnings
from pathlib import Path

import anndata
import pandas as pd
import scanpy as sc

warnings.simplefilter(action="ignore", category=FutureWarning)


def generateInputs(RunnerObj):
    if not RunnerObj.inputDir.joinpath("CCMNET").exists():
        print("Input folder for CCMNET does not exist, creating input folder...")
        RunnerObj.inputDir.joinpath("CCMNET").mkdir(exist_ok=False)

    ds = anndata.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.exprData)).T
    ds.obs = pd.read_csv(RunnerObj.inputDir.joinpath(RunnerObj.cellData), index_col=0)

    # if str(RunnerObj.params["scale"]) == "True":
    if RunnerObj.params["scale"]:
        print("Scaling as requested ...")
        sc.pp.scale(ds)

    for idx, pseudotime in enumerate(ds.obs.columns):
        subset = ds[ds.obs[pseudotime].dropna().index, :].copy()
        subset.obs["pseudotime"] = subset.obs[pseudotime]
        subset.write(f'{RunnerObj.inputDir.joinpath("CCMNET")}/data-{idx}.h5ad')


def run(RunnerObj):

    # make output dirs if they do not exist:
    outDir = "outputs/" + str(RunnerObj.inputDir).split("inputs/")[1] + "/CCMNET/"
    Path(outDir).mkdir(parents=True, exist_ok=True)

    inputPath = "." + str(RunnerObj.inputDir).split(str(Path.cwd()))[1] + "/CCMNET"
    for idx, dataset in enumerate(glob.glob(f"{inputPath}/*.h5ad")):
        timePath = f"/data/{outDir}time{idx}.txt"
        outFolder = f"/data/{outDir}"

        h5ad_file = (
            "/data"
            + str(RunnerObj.inputDir).split(str(Path.cwd()))[1]
            + "/CCMNET/"
            + Path(dataset).name
        )
        params = "--skip_filtering" if RunnerObj.params["skip_filtering"] else ""
        cmdToRun = " ".join(
            [
                "podman run --rm --device nvidia.com/gpu=1 --security-opt=label=disable --shm-size=20GB",
                f"-v {Path.cwd()}:/data localhost/ccmnet:base /bin/sh -c",
                f'"/usr/bin/time -v -o {timePath} ccmnet run {params} {h5ad_file} {outFolder}"',
            ]
        )
        print(cmdToRun)
        os.system(cmdToRun)


def parseOutput(RunnerObj):
    outDir = "outputs/" + str(RunnerObj.inputDir).split("inputs/")[1] + "/CCMNET/"

    # ccms = [pd.read_csv(ccm_file) for ccm_file in glob.glob(f'{outDir}/*.full.csv')]
    ccms = [pd.read_csv(ccm_file) for ccm_file in glob.glob(f"{outDir}/*_None.csv")]

    outDF = pd.concat(ccms)
    outDF = outDF[["Gene1", "Gene2", "ccm"]]
    outDF.columns = ["Gene1", "Gene2", "EdgeWeight"]
    FinalDF = outDF[
        outDF["EdgeWeight"]
        == outDF.groupby(["Gene1", "Gene2"])["EdgeWeight"].transform("max")
    ].copy()
    FinalDF.sort_values(["EdgeWeight"], ascending=False, inplace=True)
    FinalDF.to_csv(outDir + "rankedEdges.csv", sep="\t", index=False)
