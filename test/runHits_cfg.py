import subprocess
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('analysis')
options.register('datasets',
                 '',
                 VarParsing.multiplicity.list,
                 VarParsing.varType.string,
                 "Input dataset(s)")
options.register('eosdirs',
                 '',
                 VarParsing.multiplicity.list,
                 VarParsing.varType.string,
                 "files location(s) on EOS")
options.register('eosusdirs',
                 '',
                 VarParsing.multiplicity.list,
                 VarParsing.varType.string,
                 "files location(s) on EOS-US")
options.register('pattern',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "pattern of file names to be processed")
options.register('antipattern',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "pattern of file names not to be processed")
options.register('output',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "output file name")
options.register('debug',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Print debug messages")
options.register('runMTDReco',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Run MTD Reco")
options.register('useMTDTrack',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Use MTD Track")
options.register('crysLayout',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "crystal layout (tile, barphi, barzflat)")
options.register('nThreads',
                 1,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "# threads")
options.register('dumpRecHits',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Dump ETL/BTL recHits")
options.register('dumpSimHits',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "Dump ETL/BTL simHits")

options.maxEvents = -1
options.parseArguments()

from Configuration.StandardSequences.Eras import eras
if 'tile' in options.crysLayout:
    myera=eras.Phase2_timing_layer_tile
if 'barphi' in options.crysLayout:
    myera=eras.Phase2_timing_layer_bar
if 'barzflat' in options.crysLayout:
    myera=eras.Phase2C4_timing_layer_bar
process = cms.Process('FTLDumpHits',myera)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    numberOfThreads=cms.untracked.uint32(options.nThreads),
    numberOfStreams=cms.untracked.uint32(0),
    wantSummary = cms.untracked.bool(True)
    )

process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Global tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# import of standard configurations
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

# Geometry
if 'tile' in options.crysLayout:
    process.load('Configuration.Geometry.GeometryExtended2023D24Reco_cff')
    process.load('Configuration.Geometry.GeometryExtended2023D24_cff')
if 'barphi' in options.crysLayout:
    process.load('Configuration.Geometry.GeometryExtended2023D25Reco_cff')
    process.load('Configuration.Geometry.GeometryExtended2023D25_cff')
if 'barzflat' in options.crysLayout:
    process.load('Configuration.Geometry.GeometryExtended2023D35Reco_cff')
    process.load('Configuration.Geometry.GeometryExtended2023D35_cff')
    
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')

process.load("Geometry.MTDNumberingBuilder.mtdNumberingGeometry_cfi")
process.load("Geometry.MTDNumberingBuilder.mtdTopology_cfi")
process.load("Geometry.MTDGeometryBuilder.mtdGeometry_cfi")
process.load("Geometry.MTDGeometryBuilder.mtdParameters_cfi")
process.mtdGeometry.applyAlignment = cms.bool(False)

process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

files = []
files2 = []
for dataset in options.datasets:
    print('>> Creating list of files from: \n'+dataset)
    query = "-query='file dataset="+dataset+"'"
    if options.debug:
        print(query)
    lsCmd = subprocess.Popen(['dasgoclient '+query+' -limit=0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    str_files, err = lsCmd.communicate()
    files.extend(['root://cms-xrd-global.cern.ch/'+ifile for ifile in str_files.split("\n")])
    files = [k for k in files if options.pattern in k]
    files.pop()

for eosdir in options.eosdirs:
    if eosdir[-1] != '/':
        eosdir += '/'
    print('>> Creating list of files from: \n'+eosdir)
    
    command = '/bin/find '+eosdir+' -type f | grep root | grep -v failed | grep '+options.pattern
    str_files = subprocess.check_output(command,shell=True).splitlines()
    print str_files
    files.extend(['file:'+ifile for ifile in str_files])

for eosusdir in options.eosusdirs:
    if eosusdir[-1] != '/':
        eosusdir += '/'
    print('>> Creating list of files from: \n'+eosusdir)
    
    command = 'eos root://cmseos.fnal.gov ls '+eosusdir+' | grep root | grep -v failed | grep '+options.pattern+' | grep -v '+options.antipattern
    str_files = subprocess.check_output(command,shell=True).splitlines()
    print str_files
    files.extend(['root://cms-xrd-global.cern.ch/'+eosusdir+'/'+ifile for ifile in str_files])
        
if options.debug:
    for ifile in files:
        print(ifile)

# Input source
process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(files)
    )
process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
                            
process.load('PrecisionTiming.FTLAnalysis.FTLDumpHits_cfi')
FTLDumper = process.FTLDumpHits
if (options.useMTDTrack):
    FTLDumper.tracksTag = cms.untracked.InputTag("trackExtenderWithMTD")

if 'tile' in options.crysLayout:
    FTLDumper.crysLayout = cms.untracked.int32(1)
if 'barphi' in options.crysLayout:
    FTLDumper.crysLayout = cms.untracked.int32(2)
if 'barzflat' in options.crysLayout:
    FTLDumper.crysLayout = cms.untracked.int32(3)

#BBT 01-22-19
if (options.dumpRecHits):
    FTLDumper.dumpRecHits = cms.bool(True)
if (options.dumpSimHits):
    FTLDumper.dumpSimHits = cms.bool(True)

# Output TFile
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.output)
    )

if (options.runMTDReco):
    process.load("Configuration.StandardSequences.Reconstruction_cff")
    process.load("RecoLocalFastTime.Configuration.RecoLocalFastTime_cff")
    process.load("RecoMTD.Configuration.RecoMTD_cff")


## Track-MC association
#process.load("SimGeneral.TrackingAnalysis.simHitTPAssociation_cfi")
#process.load("SimTracker.TrackAssociatorProducers.trackAssociatorByHits_cfi")
#process.load("SimTracker.TrackAssociation.trackMCMatch_cfi")
#
#process.simHitTPAssocProducer.simHitSrc = ["g4SimHits:TrackerHitsPixelBarrelLowTof", "g4SimHits:TrackerHitsPixelEndcapLowTof"]
#process.trackMCMatch.associator = cms.string('trackAssociatorByHits')
#process.path = cms.Path(process.simHitTPAssocProducer*process.trackAssociatorByHits*process.trackMCMatch*FTLDumper)

process.runseq = cms.Sequence()
if options.runMTDReco:
    process.runseq += cms.Sequence(process.mtdClusters*process.mtdTrackingRecHits)
    process.runseq += cms.Sequence(process.trackExtenderWithMTD)
process.runseq += FTLDumper

process.path = cms.Path(process.runseq)
process.schedule = cms.Schedule(process.path)
