#------------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------------
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

#------------------------------------------------------------------------------------
# Options
#------------------------------------------------------------------------------------
options = VarParsing.VarParsing()

options.register('skipEvents',
                 0, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to skip")

options.register('processEvents',
                 -1, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of events to process")

options.register('inputFiles',
                 "file:inputFile.root",
                 VarParsing.VarParsing.multiplicity.list,
                 VarParsing.VarParsing.varType.string,
                 "Input files")

options.register('outputFile',
                 "file:hcalnano.root", # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output file")

options.parseArguments()

print(" ")
print("Using options:")
print(" skipEvents    =", options.skipEvents)
print(" processEvents =", options.processEvents)
print(" inputFiles    =", options.inputFiles)
print(" outputFile    =", options.outputFile)
print(" ")

#------------------------------------------------------------------------------------
# Declare the process and input variables
#------------------------------------------------------------------------------------
process = cms.Process('PFG', eras.Run3)

#------------------------------------------------------------------------------------
# Get and parse the command line arguments
#------------------------------------------------------------------------------------
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.processEvents) )

process.source = cms.Source(
    "PoolSource",
    fileNames  = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents)
    )

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
    )

#------------------------------------------------------------------------------------
# import of standard configurations
#------------------------------------------------------------------------------------

# Reduce message log output
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10)

#process.load('Configuration.StandardSequences.Services_cff')
#process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')

#process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
##process.load("RecoLocalCalo.Configuration.RecoLocalCalo_Cosmics_cff")
#process.load('Configuration.StandardSequences.EndOfProcess_cff')
#process.load('RecoMET.METProducers.hcalnoiseinfoproducer_cfi')
#process.load("CommonTools.RecoAlgos.HBHENoiseFilter_cfi")
#process.load("CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi")
#process.load("CondCore.CondDB.CondDB_cfi")

#------------------------------------------------------------------------------------
# Set up our analyzer
#------------------------------------------------------------------------------------
#process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
## set desired parameters, for example:
#process.hcalTupleHBHERecHits.source = cms.untracked.InputTag("hbheplan1")
#process.hcalTupleHODigis.DoEnergyReco = cms.untracked.bool(False)

#------------------------------------------------------------------------------------
# QIE11 and QIE10 Unpacker
#------------------------------------------------------------------------------------

# Note: these lines create additional QIE digi collections with different NSamples, I think...
#process.hcalDigis.saveQIE11DataNSamples = cms.untracked.vint32(8) 
#process.hcalDigis.saveQIE11DataTags = cms.untracked.vstring( "MYDATAQIE11" )
#process.hcalDigis.saveQIE10DataNSamples = cms.untracked.vint32(8) 
#process.hcalDigis.saveQIE10DataTags = cms.untracked.vstring( "MYDATAQIE10" )

#------------------------------------------------------------------------------------
# Specify Global Tag
#------------------------------------------------------------------------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '122X_dataRun3_HLT_v3'
print("GlobalTag = ", str(process.GlobalTag.globaltag).split("'")[1])
print(" ")

#------------------------------------------------------------------------------------
# HcalTupleMaker sequence definition
#------------------------------------------------------------------------------------
#from PhysicsTools.NanoAOD.common_cff import *
process.load("PhysicsTools.NanoAOD.nano_cff")
process.load("HCALPFG.HcalNano.hcaldigitable_cff") # loads all modules


process.nano_step = cms.Sequence(
    process.hcalDigiTable
)

#-----------------------------------------------------------------------------------
# Path and EtagQIE11ndPath definitions
#-----------------------------------------------------------------------------------
process.preparation = cms.Path(
    # Digis
    process.hcalDigis*

    ## reconstruction
    process.L1Reco*
    process.reconstruction*
    process.hcalLocalRecoSequence*

    ## Do energy reconstruction
    process.horeco*
    process.hfprereco*
    process.hfreco*
    process.hbheprereco*
    process.hbhereco*

    ## Make the ntuples
    process.nano_step
)


process.out = cms.OutputModule("NanoAODOutputModule",
    fileName = cms.untracked.string('hcalnano.root'),
    outputCommands = process.NanoAODEDMEventContent.outputCommands,
    compressionLevel = cms.untracked.int32(9),
    compressionAlgorithm = cms.untracked.string("LZMA"),

)
process.end = cms.EndPath(process.out)  

#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange('293765:264-293765:9999')