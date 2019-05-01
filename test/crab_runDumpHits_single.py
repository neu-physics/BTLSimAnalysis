from WMCore.Configuration import Configuration 
config = Configuration() 
config.section_("General") 
config.General.requestName = 'runHitsRelValSingleMuFlatPt0p7to10noPU-v2V7_r3' ## change//Name of the directory that crab will create

config.section_("JobType") 
config.JobType.pluginName = 'Analysis' 
config.JobType.psetName = 'runHits_cfg.py' ###Config file that crab will use for the job
config.JobType.pyCfgParams = ['useMTDTrack=True','crysLayout=barzflat','output=DumpHits.root','dumpRecHits=True'] # BBT, 01-22-19
config.General.transferOutputs = True
config.General.transferLogs = False

#config.JobType.allowUndistributedCMSSW = False

config.section_("Data") ###Might need to chance to MC
config.Data.inputDataset = None
#config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.outLFNDirBase = '/store/user/btannenw/MTD/10_4_0_mtd3/SingleMu_FlatPt_BTL_barz_v2/'
config.Data.outLFNDirBase = '/store/user/btannenw/'
config.Data.publication = False
config.Data.outputDatasetTag = '10_4_0_mtd3_runHitsRelValSingleMuFlatPt0p7to10noPU-v2V7_r3'
config.Data.allowNonValidInputDataset = True
config.Data.useParent = True
config.Data.inputDataset = '/RelValSingleMuFlatPt_0p7to10_pythia8/meridian-RelValSingleMuFlatPt0p7to10pythia8CMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v2V7-45dc70b98f9b98b0807197db02f5776e/USER'
### V7 chi2=500, use only bestChi2, clusterTimeThreshold=10
#             '/RelValSingleProtonFlatPt_0p7to10/meridian-RelValSingleProtonFlatPt0p7to10CMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValSinglePiFlatPt_0p7to10_pythia8_cfi/meridian-RelValSinglePiFlatPt0p7to10pythia8cfiCMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v2V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValSingleMuFlatPt_0p7to10/meridian-RelValSingleMuFlatPt0p7to10CMSSW1040mtd2patch1-PU25ns103Xupgrade2023realisticv22023D35PU200-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValSingleKaonFlatPt_0p7to10/meridian-RelValSingleKaonFlatPt0p7to10CMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValNuGun/meridian-RelValNuGunCMSSW1040mtd2patch1-PU25ns103Xupgrade2023realisticv22023D35PU200-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValMinBias_14TeV/meridian-RelValMinBias14TeVCMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/RelValDYToLL_M_50_14TeV/meridian-RelValDYToLLM5014TeVCMSSW1040mtd2patch1-103Xupgrade2023realisticv22023D35noPU-v1V7-45dc70b98f9b98b0807197db02f5776e/USER',
#             '/DYToLL_M-50_14TeV_pythia8/meridian-DYToLLM-5014TeVpythia8PhaseIIMTDTDRAutumn18DR-PU200pilot103Xupgrade2023realisticv2ext2-v2V7-45dc70b98f9b98b0807197db02f5776e/USER',
###Add the full Dataset you find from CMSDAS site here.


#config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader/' ###Probably wont need to change
config.Data.inputDBS = 'phys03'

#config.Data.splitting = 'Automatic' ###Can be changed to Automatic, FileBased, LumiBased
#config.Data.unitsPerJob = 10
#Commented OUT Feb13  
	#config.Data.publication = True 
config.Data.publishDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSWriter/' ###More a factor if generating MC samples, usually just fine.
#Commented OUT Feb13
	#config.Data.publishDataName = 'Validation_v1'
### change user Space 
#onfig.Data.outLFNDirBase = '/store/group/lpctthrun2/analysis2017Data/triggerSF/MC/'
#config.Data.outLFNDirBase = '/store/user/btannenw/'

#'/store/group/lpcmj/data/UVa/2018Data'###Wherever we can find space and start after '/eos/uscms' in the directory path.
#'/store/user/lwming/'

config.section_("Data") ###Might need to chance to MC
config.Data.ignoreLocality = False #Changed from True Feb 13

#config.section_("User") ### relic from paolo... do i need? [BBT, 01-22-19]
#config.User.voRole = 'priorityuser'

config.section_("Site") 
#config.Site.storageSite = 'T2_CH_CERN'
config.Site.storageSite = 'T3_US_FNALLPC'
