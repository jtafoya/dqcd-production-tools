# Some README file

This repository contains tools that complement sample generation with

[https://github.com/ic-dqcd/dqcd-production/tree/2023](https://github.com/ic-dqcd/dqcd-production/tree/2023)

and other general CRAB tools.





# Useful other tools

Sometimes sample processing can fail because of an unfortunate particular event (e.g. a SIM-level event that falls in the incorrect geometrical region and thus the GEANT4 processin in the GENSIM step fails). 
It is possible to continue the processing by skipping such particular event.

Fot the case of a problematic event at the GENSIM step giving the error
```
Error while running CMSSW:
                Fatal Exception
                An exception of category 'Geant4 fatal exception' occurred while
                   [0] Processing  Event run: 1 lumi: 9692 event: 969194 stream: 0
                   [1] Running path 'RAWSIMoutput_step'
                   [2] Prefetching for module PoolOutputModule/'RAWSIMoutput'
                   [3] Calling method for module OscarMTProducer/'g4SimHits'
```

You must:

- Modify the configuration card so that it runs on the missing file (see `./submit_missing_files/`)
 you can force processing ONLY on the

- Add the following line of the `gensim_cfg.py` file (e.g. below the `process.source.bypassVersionCheck=cms.untracked.bool(True)`):
```
process.source.eventsToSkip = cms.untracked.VEventRange("1:9692:969194")
```

Note that you MUST remove this line before submiting other jobs (although its unlikely to propagate tpo undesired events since it acts in a specific lumi block).
