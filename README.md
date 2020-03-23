# Studies of BTL behaviour in CMSSW simulation

Exactly like it sounds like. To setup necessary environment, first checkout

`git clone -b CMSSW https://github.com/simonepigazzini/DynamicTTree.git ExternalTools/DynamicTTree/`

then checkout this package.

To run code do:

`cmsRun runHits_cfg.py eosdirs=/afs/cern.ch/work/b/btannenw/MTD/DPG/positionReco/v2/CMSSW_11_1_0_pre4/src/uvaCheckout_23303/ pattern='step3.root' output='./output.root' geometry=D49 useMTDTrack=False dumpRecHits=True`

To get plots after running code, do:

`python drawBTLresidual.py --inputDir=input/path --pattern='input pattern' --output=output.root`
