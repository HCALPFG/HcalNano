# HcalNano
An EDM analyer for analyzing HCAL digis and RecHits. This supercedes https://github.com/HCALPFG/HcalTupleMaker, replacing the custom output module with CMSSW NanoAODOutputModule. 

Setup instructions:
```
scram project -n "CMSSW_12_3_0_HcalNano" CMSSW_12_3_0
cd CMSSW_12_3_0_HcalNano/src
cmsenv
git cms-init
git clone git@github.com:HCALPFG/HcalNano.git HCALPFG/HcalNano
## Optional, if you want to study or modify NanoAOD in some way:
# git cms-addpkg PhysicsTools/NanoAOD
# git cms-addpkg DataFormats/NanoAOD
scram b -j8
```

Example:
```
cd $CMSSW_BASE/src/HCALPFG/HcalNano/test
cmsRun test_cfg.py inputFiles=root:///store/group/dpg_hcal/comm_hcal/Splashes2022/splashes_350968_FEVT.root outputFile=hcalnano_test.root nThreads=4 compressionAlgorithm=ZLIB compressionLevel=5
```

