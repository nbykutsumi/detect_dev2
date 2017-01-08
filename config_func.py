import os

def config_func(prj, model, run):
    cfg = {}
    #rootDir = "/home/utsumi/mnt/well.share/WS"
    rootDir = "/home/utsumi/mnt/temp/WS"
    baseDir = os.path.join(rootDir, prj, model, run)

    cfg["rootDir"] = rootDir
    cfg["baseDir"] = baseDir
    cfg["prj"    ] = prj
    cfg["model"  ] = model
    cfg["run"    ] = run

    return cfg
