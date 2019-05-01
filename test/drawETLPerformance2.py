import ROOT as R
import math as M
import argparse
import subprocess

def goodTrack(evt, itrack , chi2cut):
    #acceptance cuts
    if (evt.track_pt[itrack]<0.7):
        return False
    if (abs(evt.track_eta[itrack])>3.):
        return False
    #for the moment use matching with mc gen particle
    if (abs(evt.track_mcMatch_DR[itrack])>0.05):
        return False
    if (abs(evt.track_pt[itrack]/evt.track_mcMatch_genPt[itrack]-1.)>0.1):
        return False
#    if (evt.track_normalizedChi2[itrack] > chi2cut):
#        return False
#    if (evt.track_eta_atBTL[itrack]<-100 and evt.track_eta_atETL[itrack]<-100):
#        return False
    return True

parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')
parser.add_argument('--inputDir',dest='inputDir')
parser.add_argument('--pattern',dest='pattern')
parser.add_argument('--output',dest='output')
parser.add_argument('--layout',dest='layout')
parser.add_argument('--chi2cut',dest='chi2cut')
parser.add_argument('--events',dest='events',default='-1')
parser.add_argument('--dumpHits',dest='dumpHits',action='store_true',default=False)
parser.add_argument('--dumpAll',dest='dumpAll',action='store_true',default=False)

args = parser.parse_args()

if (args.inputDir != ""):
    print args.inputDir
    dh=R.TChain("DumpHits")
    files = []
    if args.inputDir[-1] != '/':
        args.inputDir += '/'
    print('>> Creating list of files from: \n'+args.inputDir)
    command = '/bin/find '+args.inputDir+' -type f | grep root | grep -v failed | grep '+args.pattern
    str_files = subprocess.check_output(command,shell=True).splitlines()
    #print str_files
    files.extend(['file:'+ifile for ifile in str_files])
    for file in files:
        print ">> Adding "+file
        dh.Add(file)
else:
    print('>> Opening: '+args.input)
    f=R.TFile(args.input)
    dh=f.Get("DumpHits")

histos = {}

# time offset introduced in mtd2 due to light collection time (pitch.z()/2 * 7.5ps for bars)
t_offset={}
t_offset['ETL']=-0.0066
t_offset['BTL']=0.
if args.layout == "barzflat":
    t_offset['BTL']=0.226875-0.0115
elif args.layout == "barphi":
    t_offset['BTL']=0.160
elif args.layout == "tile":
    t_offset['BTL']=0.200

histos["track_pt"]=R.TH1F("track_pt","track_pt",100,0.,10.)
histos["track_eta"]=R.TH1F("track_eta","track_eta",100,0.,3,)
histos["track_eta_lowPt"]=R.TH1F("track_eta_lowPt","track_eta_lowPt",100,0.,3,)
histos["track_phi"]=R.TH1F("track_phi","track_phi",1000,-M.pi,M.pi)
#histos["track_eta_1"]=R.TH1F("track_eta_1","track_eta_1",100,0.,3,)
histos["track_eta_sel"]=R.TH1F("track_eta_sel","track_eta_sel",100,0.,3,)
histos["track_phi_sel"]=R.TH1F("track_phi_sel","track_phi_sel",1000,-M.pi,M.pi)
histos["eff_eta"]=R.TH1F("eff_eta","eff_eta",100,0.,3,)
histos["eff_phi"]=R.TH1F("eff_phi","eff_phi",1000,-M.pi,M.pi)

histos["mtdTrack_pt"]=R.TH1F("mtdTrack_pt","mtdTrack_pt",100,0.,10.)
histos["mtdTrack_eta"]=R.TH1F("mtdTrack_eta","mtdTrack_eta",100,0.,3,)
histos["mtdTrack_eta_lowPt"]=R.TH1F("mtdTrack_eta_lowPt","mtdTrack_eta_lowPt",100,0.,3,)
histos["mtdTrack_phi"]=R.TH1F("mtdTrack_phi","mtdTrack_phi",100,-M.pi,M.pi)
histos["mtdTrack_dt"]=R.TH1F("mtdTrack_dt","mtdTrack_dt",100,-0.2,0.2)
histos["mtdTrack_dt_vs_pt"]=R.TH2F("mtdTrack_dt_vs_pt","mtdTrack_dt_vs_pt",50,0,10,100,-0.2,0.2)
histos["mtdTrack_dt_vs_eta"]=R.TH2F("mtdTrack_dt_vs_eta","mtdTrack_dt_vs_eta",80,0,3,100,-0.2,0.2)
histos["mtdTrack_dz"]=R.TH1F("mtdTrack_dz","mtdTrack_dz",200,-0.05,0.05)
histos["mtdTrack_dz_vs_pt"]=R.TH2F("mtdTrack_dz_vs_pt","mtdTrack_dz_vs_pt",50,0,10,200,-0.05,0.05)
histos["mtdTrack_dz_vs_eta"]=R.TH2F("mtdTrack_dz_vs_eta","mtdTrack_dz_vs_eta",80,0,3,200,-0.05,0.05)
histos["mtdTrack_ptRes"]=R.TH1F("mtdTrack_ptRes","mtdTrack_ptRes",200,-0.05,0.05)
histos["mtdTrack_ptRes_vs_pt"]=R.TH2F("mtdTrack_ptRes_vs_pt","mtdTrack_ptRes_vs_pt",50,0,10,200,-0.05,0.05)
histos["mtdTrack_ptRes_vs_eta"]=R.TH2F("mtdTrack_ptRes_vs_eta","mtdTrack_ptRes_vs_eta",80,0,3,200,-0.05,0.05)
#create hist to draw energy distribution plot
#histos["h_recHit_energy"]=R.TH1F("h_recHit_energy","h_recHit_energy")

for det in ["BTL","ETL"]:
    # BBT, 01-25-19
    # Fig 1.6
    #histos["recHit_readoutEnergy_"+det]=R.TH1F("track__readoutEnergy_"+det,"track_readoutEnergy_"+det,40,0,10)
    #histos["recHit_readoutEnergy_"+det]=R.TH1F("track__readoutEnergy_"+det,"track_readoutEnergy_"+det,40,0,10)

    # Fig 1.7
    minEta = 0 if det == 'BTL' else 1.6
    maxEta = 1.4 if det == 'BTL' else 2.5
    histos["track_eta_at"+det]=R.TH1F("track_eta_at"+det,"track_eta_at"+det,30,minEta,maxEta)
    histos["track_eta_at"+det+"_overThreshE"]=R.TH1F("track_eta_at"+det+"_overThreshE","track_eta_at"+det+"_overThreshE",30,minEta,maxEta)
    histos["track_phi_at"+det]=R.TH1F("track_phi_at"+det,"track_phi_at"+det,30,0,M.pi)
    histos["track_phi_at"+det+"_overThreshE"]=R.TH1F("track_phi_at"+det+"_overThreshE","track_phi_at"+det+"_overThreshE",30,0,M.pi)
    # Fig 1.8
    histos["track_pt_at"+det]=R.TH1F("track_pt_at"+det,"track_pt_at"+det,30,0.,10)
    histos["track_pt_at"+det+"_overThreshE"]=R.TH1F("track_pt_at"+det+"_overThreshE","track_pt_at"+det+"_overThreshE",30,0.,10)
    # Fig 1.7
    maxE = 50 if det == 'BTL' else 0.5
    histos["recHit_energy_dR05_withTrack"+det]=R.TH1F("recHit_energy_dR05_withTrack"+det,"recHit_energy_dR05_withTrack"+det,50,0.,maxE)
    histos["recHit_energy_dR05_withTrack"+det+"_fixedRange"]=R.TH1F("recHit_energy_dR05_withTrack"+det+"_fixedRange","recHit_energy_dR05_withTrack"+det+"_fixedRange",50,0.,5)
    maxHitE = 19 if det == 'BTL' else 10
    histos["recHit_maxEnergy_withTrack"+det]=R.TH1F("recHit_maxEnergy_withTrack"+det,"recHit_maxEnergy_withTrack"+det,50,0.,maxHitE)
    histos["recHit_maxEnergy_dRpass_withTrack"+det]=R.TH1F("recHit_maxEnergy_dRpass_withTrack"+det,"recHit_maxEnergy_dRpass_withTrack"+det,50,0.,maxHitE)
    
    # Fig. Occupancy
    maxE = 10 if det == 'BTL' else 2.5

    # occupancy for all rings
    histos["recHit_energy_allHitsAllRings_"+det]=R.TH1F("recHit_energy_allHitsAllRings_"+det,"recHit_energy_allHitsAllRings_"+det, int(maxE*100), 0., maxE)
    histos["h_occupancy_numerator_allHitsAllRings_"+det] = R.TH1F("h_occupancy_numerator_allHitsAllRings_"+det,"h_occupancy_numerator_allHitsAllRings_"+det, int(100*maxE), 0, maxE)
    histos["h_occupancy_denominator_allHitsAllRings_"+det] = R.TH1F("h_occupancy_denominator_allHitsAllRings_"+det,"h_occupancy_denominator_allHitsAllRings_"+det, int(100*maxE), 0, maxE)
    # occupancy split by ring
    for iRing in range(1,12):
        histos["recHit_energy_allHitsRing"+str(iRing)+"_"+det]=R.TH1F("recHit_energy_allHitsRing"+str(iRing)+"_"+det,"recHit_energy_allHitsRing"+str(iRing)+"_"+det, int(100*maxE), 0, maxE)
        histos["h_occupancy_numerator_allHitsRing"+str(iRing)+"_"+det] = R.TH1F("h_occupancy_numerator_allHitsRing"+str(iRing)+"_"+det,"h_occupancy_numerator_allHitsRing"+str(iRing)+"_"+det, int(100*maxE), 0, maxE)
        histos["h_occupancy_denominator_allHitsRing"+str(iRing)+"_"+det] = R.TH1F("h_occupancy_denominator_allHitsRing"+str(iRing)+"_"+det,"h_occupancy_denominator_allHitsRing"+str(iRing)+"_"+det, int(100*maxE), 0, maxE)



    # Paolo + Ang
    histos[det+"track_pt"]= R.TH1F (det+"track_pt" ,det+"track_pt",100,0.,10.)
    histos[det+"track_eta"]=R.TH1F(det+"track_eta",det+"track_eta",100,0.,3,)
    histos[det+"track_eta_lowPt"]=R.TH1F(det+"track_eta_lowPt",det+"track_eta_lowPt",100,0.,3,)
    histos[det+"track_phi"]=R.TH1F(det+"track_phi",det+"track_phi",5000,-M.pi,M.pi)
    histos[det+"track_eta_sel"]=R.TH1F(det+"track_eta_sel",det+"track_eta_sel",100,0.,3,)
    histos[det+"track_phi_sel"]=R.TH1F(det+"track_phi_sel",det+"track_phi_sel",5000,-M.pi,M.pi)
    histos[det+"eff_eta"]=R.TH1F(det+"eff_eta",det+"eff_eta",100,0.,3,)
    histos[det+"eff_phi"]=R.TH1F(det+"eff_phi",det+"eff_phi",5000,-M.pi,M.pi)
    
    
    histos[det+"matchedTrack_nCluster"]=R.TH1F(det+"matchedTrack_nCluster",det+"matchedTrack_nCluster",10,0.,10.)
    histos[det+"matchedTrack_nRecHits"]=R.TH1F(det+"matchedTrack_nRecHits",det+"matchedTrack_nRecHits",10,0.,10.)

    histos[det+"cluster_energy"]=R.TH1F(det+"cluster_energy",det+"cluster_energy",100,0.,20.)
    histos[det+"cluster_time"]=R.TH1F(det+"cluster_time",det+"cluster_time",100,0.,25.)
    histos[det+"cluster_size"]=R.TH1F(det+"cluster_size",det+"cluster_size",20,0.,20.)
    histos[det+"cluster_sizeX"]=R.TH1F(det+"cluster_sizeX",det+"cluster_sizeX",20,0.,20.)
    histos[det+"cluster_sizeY"]=R.TH1F(det+"cluster_sizeY",det+"cluster_sizeY",20,0.,20.)
    histos[det+"cluster_seedEnergyRatio"]=R.TH1F(det+"cluster_seedEnergyRatio",det+"cluster_seedEnergyRatio",110,0.,1.1)
    
    histos[det+"recHit_energy"]=R.TH1F(det+"recHit_energy",det+"recHit_energy",100,0.,20.)
    histos[det+"recHit_time"]=R.TH1F(det+"recHit_time",det+"recHit_time",100,0.,25.)
    histos[det+"recHit_energy_h"]=R.TH1F(det+"recHit_energy_h",det+"recHit_energy_h",200,0.,100.)

    histos[det+"matchedClusterTrack_pt"]=R.TH1F(det+"matchedClusterTrack_pt",det+"matchedClusterTrack_pt",100,0.,10.)
    histos[det+"matchedClusterTrack_eta"]=R.TH1F(det+"matchedClusterTrack_eta",det+"matchedClusterTrack_eta",100,0.,3,)
    histos[det+"matchedClusterTrack_phi"]=R.TH1F(det+"matchedClusterTrack_phi",det+"matchedClusterTrack_phi",100,-M.pi,M.pi)
    histos[det+"matchedBestClusterTrack_pt"]=R.TH1F(det+"matchedBestClusterTrack_pt",det+"matchedBestClusterTrack_pt",100,0.,10.)
    histos[det+"matchedBestClusterTrack_eta"]=R.TH1F(det+"matchedBestClusterTrack_eta",det+"matchedBestClusterTrack_eta",100,0.,3,)
    histos[det+"matchedBestClusterTrack_eta_lowPt"]=R.TH1F(det+"matchedBestClusterTrack_eta_lowPt",det+"matchedBestClusterTrack_eta_lowPt",100,0.,3,)
    histos[det+"matchedBestClusterTrack_phi"]=R.TH1F(det+"matchedBestClusterTrack_phi",det+"matchedBestClusterTrack_phi",100,-M.pi,M.pi)

    histos[det+"matchedRecHitTrack_pt"]=R.TH1F(det+"matchedRecHitTrack_pt",det+"matchedRecHitTrack_pt",100,0.,10.)
    histos[det+"matchedRecHitTrack_eta"]=R.TH1F(det+"matchedRecHitTrack_eta",det+"matchedRecHitTrack_eta",100,0.,3,)
    histos[det+"matchedRecHitTrack_phi"]=R.TH1F(det+"matchedRecHitTrack_phi",det+"matchedRecHitTrack_phi",100,-M.pi,M.pi)
    histos[det+"matchedBestRecHitTrack_pt"]=R.TH1F(det+"matchedBestRecHitTrack_pt",det+"matchedBestRecHitTrack_pt",100,0.,10.)
    histos[det+"matchedBestRecHitTrack_eta"]=R.TH1F(det+"matchedBestRecHitTrack_eta",det+"matchedBestRecHitTrack_eta",100,0.,3,)
    histos[det+"matchedBestRecHitTrack_phi"]=R.TH1F(det+"matchedBestRecHitTrack_phi",det+"matchedBestRecHitTrack_phi",100,-M.pi,M.pi)

    histos[det+"matchedCluster_energy"]=R.TH1F(det+"matchedCluster_energy",det+"matchedCluster_energy",100,0.,20.)
    histos[det+"matchedCluster_time"]=R.TH1F(det+"matchedCluster_time",det+"matchedCluster_time",100,0.,25.)
    histos[det+"matchedCluster_DR"]=R.TH1F(det+"matchedCluster_DR",det+"matchedCluster_DR",100,0.,0.05)
    histos[det+"matchedCluster_size"]=R.TH1F(det+"matchedCluster_size",det+"matchedCluster_size",20,0.,20.)
    histos[det+"matchedCluster_size_vs_pt"]=R.TH2F(det+"matchedCluster_size_vs_pt",det+"matchedCluster_size_vs_pt",100,0.,10.,20,-0.5,19.5)
    histos[det+"matchedCluster_size_vs_eta"]=R.TH2F(det+"matchedCluster_size_vs_eta",det+"matchedCluster_size_vs_eta",100,0.,3,20,-0.5,19.5)
    histos[det+"matchedCluster_sizeX"]=R.TH1F(det+"matchedCluster_sizeX",det+"matchedCluster_sizeX",20,0.,20.)
    histos[det+"matchedCluster_sizeY"]=R.TH1F(det+"matchedCluster_sizeY",det+"matchedCluster_sizeY",20,0.,20.)

    histos[det+"bestCluster_energy"]=R.TH1F(det+"bestCluster_energy",det+"bestCluster_energy",100,0.,20.)
    histos[det+"bestCluster_time"]=R.TH1F(det+"bestCluster_time",det+"bestCluster_time",100,0.,25.)
    histos[det+"bestCluster_time_vs_pt"]=R.TH2F(det+"bestCluster_time_vs_pt",det+"bestCluster_time_vs_pt",50,0,10,100,0,25)
    histos[det+"bestCluster_time_vs_eta"]=R.TH2F(det+"bestCluster_time_vs_eta",det+"bestCluster_time_vs_eta",80,0,3,100,0,25)
    histos[det+"bestCluster_DR"]=R.TH1F(det+"bestCluster_DR",det+"bestCluster_DR",100,0.,0.05)
    histos[det+"bestCluster_DEta"]=R.TH1F(det+"bestCluster_DEta",det+"bestCluster_DEta",100,0.,0.05)
    histos[det+"bestCluster_DPhi"]=R.TH1F(det+"bestCluster_DPhi",det+"bestCluster_DPhi",100,0.,0.05)
    histos[det+"bestCluster_hasMTD_DR"]=R.TH1F(det+"bestCluster_hasMTD_DR",det+"bestCluster_hasMTD_DR",100,0.,0.05)
    histos[det+"bestCluster_hasMTD_DEta"]=R.TH1F(det+"bestCluster_hasMTD_DEta",det+"bestCluster_hasMTD_DEta",100,0.,0.05)
    histos[det+"bestCluster_hasMTD_DPhi"]=R.TH1F(det+"bestCluster_hasMTD_DPhi",det+"bestCluster_hasMTD_DPhi",100,0.,0.05)
    histos[det+"bestCluster_size"]=R.TH1F(det+"bestCluster_size",det+"bestCluster_size",20,0.,20.)
    histos[det+"bestCluster_size_vs_pt"]=R.TH2F(det+"bestCluster_size_vs_pt",det+"bestCluster_size_vs_pt",100,0.,10.,20,-0.5,19.5)
    histos[det+"bestCluster_size_vs_eta"]=R.TH2F(det+"bestCluster_size_vs_eta",det+"bestCluster_size_vs_eta",100,0.,3,20,-0.5,19.5)
    histos[det+"bestCluster_sizeX"]=R.TH1F(det+"bestCluster_sizeX",det+"bestCluster_sizeX",20,0.,20.)
    histos[det+"bestCluster_sizeY"]=R.TH1F(det+"bestCluster_sizeY",det+"bestCluster_sizeY",20,0.,20.)

    histos[det+"matchedRecHit_energy"]=R.TH1F(det+"matchedRecHit_energy",det+"matchedRecHit_energy",100,0.,20.)
    histos[det+"matchedRecHit_time"]=R.TH1F(det+"matchedRecHit_time",det+"matchedRecHit_time",100,0.,25.)
    histos[det+"matchedRecHit_DR"]=R.TH1F(det+"matchedRecHit_DR",det+"matchedRecHit_DR",100,0.,0.05)

    histos[det+"bestRecHit_energy"]=R.TH1F(det+"bestRecHit_energy",det+"bestRecHit_energy",100,0.,20.)
    histos[det+"bestRecHit_time"]=R.TH1F(det+"bestRecHit_time",det+"bestRecHit_time",100,0.,25.)
    histos[det+"bestRecHit_DR"]=R.TH1F(det+"bestRecHit_DR",det+"bestRecHit_DR",100,0.,0.05)
    histos[det+"bestRecHit_time_vs_pt"]=R.TH2F(det+"bestRecHit_time_vs_pt",det+"bestRecHit_time_vs_pt",50,0,10,100,0,25)
    histos[det+"bestRecHit_time_vs_eta"]=R.TH2F(det+"bestRecHit_time_vs_eta",det+"bestRecHit_time_vs_eta",80,0,3,100,0,25)

det_id = { 'BTL':1  , 'ETL':2 }
etaCut = { 'BTL':[0,1.5]  , 'ETL':[1.5,3] }

if (args.dumpAll):
    print "Dumping also non matched MTD hits"

if (args.dumpHits):
    print "Dumping RecHits"

for ievent,event in enumerate(dh):
    if (int(args.events) != -1 and ievent>int(args.events)):
        break
    if (ievent%100==0):
        print "Analyzing event %d"%ievent
    
    if (args.dumpAll):    
        for det in ["BTL","ETL"]:
            for iclus in range(0,event.clusters_n):
                if ( event.clusters_det[iclus] !=  det_id[det] ):
                    continue 
                histos[det+"cluster_energy"].Fill(event.clusters_energy[iclus])
                histos[det+"cluster_time"].Fill(event.clusters_time[iclus])
                histos[det+"cluster_size"].Fill(event.clusters_size[iclus])
                histos[det+"cluster_sizeX"].Fill(event.clusters_size_x[iclus])
                histos[det+"cluster_sizeY"].Fill(event.clusters_size_y[iclus])
                histos[det+"cluster_seedEnergyRatio"].Fill(event.clusters_seed_energy[iclus]/event.clusters_energy[iclus])

            if (args.dumpHits):    
                for ihit in range(0,event.recHits_n):
                    if ( event.recHits_det[ihit] !=  det_id[det] ):
                        continue 
                    histos[det+"recHit_energy"].Fill(event.recHits_energy[ihit])
                    histos[det+"recHit_time"].Fill(event.recHits_time[ihit])


    for itrack in range(0,len(event.track_idx)):
        recHit_energy_totalval_BTL = 0   #the total value of recHit energy from BTL
        recHit_energy_totalval_ETL = 0   #from ETL
        n_recHits_BTL = 0
        n_recHits_ETL = 0

        if (not goodTrack(event,itrack,args.chi2cut)):
            continue

        ############################################################################################3
        # BBT, 01-25-19
        cut_dR = 0.05
        threshold_depositE = 0 # MeV
        if (event.track_eta_atBTL[itrack]>-100.):  #if the extrapolated track hits the BTL
            threshold_depositE = 3 # MeV
            recHit_matched_totalE_BTL = 0
            maxRecHitEnergy = 0
            maxRecHitEnergy_dRpass = 0
            histos["track_eta_atBTL"].Fill(abs(event.track_eta_atBTL[itrack]))
            histos["track_phi_atBTL"].Fill(abs(event.track_phi_atBTL[itrack]))
            histos["track_pt_atBTL"].Fill(event.track_pt[itrack])
            for iRecHit in range(0,event.recHits_n):   #loop over all recHits
                dR= M.sqrt(pow((event.track_eta_atBTL[itrack]-event.recHits_eta[iRecHit]),2)+pow(event.track_phi_atBTL[itrack]-event.recHits_phi[iRecHit],2))
                if (event.recHits_det[iRecHit]!=1):
                    continue

                histos["recHit_energy_allHitsAllRings_BTL"].Fill(event.recHits_energy[iRecHit])
                #histos["recHit_energy_allHitsRing"+str(event.recHits_rr[iRecHit])+"_BTL"].Fill(event.recHits_energy[iRecHit])
                
                if (event.recHits_energy[iRecHit] > maxRecHitEnergy):
                    maxRecHitEnergy = event.recHits_energy[iRecHit]
                if(dR < cut_dR):
                    recHit_matched_totalE_BTL += event.recHits_energy[iRecHit]
                    if (event.recHits_energy[iRecHit] > maxRecHitEnergy_dRpass):
                        maxRecHitEnergy_dRpass = event.recHits_energy[iRecHit]
            histos["recHit_energy_dR05_withTrackBTL"].Fill(recHit_matched_totalE_BTL)
            histos["recHit_maxEnergy_withTrackBTL"].Fill(maxRecHitEnergy)
            histos["recHit_maxEnergy_dRpass_withTrackBTL"].Fill(maxRecHitEnergy_dRpass)
            if(recHit_matched_totalE_BTL > threshold_depositE ):
                histos["track_eta_atBTL_overThreshE"].Fill(abs(event.track_eta_atBTL[itrack]))
                histos["track_phi_atBTL_overThreshE"].Fill(abs(event.track_phi_atBTL[itrack]))
                histos["track_pt_atBTL_overThreshE"].Fill(event.track_pt[itrack])
            
        if (event.track_eta_atETL[itrack]>-100): # extrapolated track hits the ETL
            threshold_depositE = 0.03 # MeV
            recHit_matched_totalE_ETL = 0 
            maxRecHitEnergy = 0
            maxRecHitEnergy_dRpass = 0
            histos["track_eta_atETL"].Fill(abs(event.track_eta_atETL[itrack]))
            histos["track_phi_atETL"].Fill(abs(event.track_phi_atETL[itrack]))
            histos["track_pt_atETL"].Fill(event.track_pt[itrack])
            for iRecHit in range(0,event.recHits_n):   #loop over all recHits
                dR= M.sqrt(pow((event.track_eta_atETL[itrack]-event.recHits_eta[iRecHit]),2)+pow(event.track_phi_atETL[itrack]-event.recHits_phi[iRecHit],2))
                if (event.recHits_det[iRecHit]!=2):
                    continue

                histos["recHit_energy_allHitsAllRings_ETL"].Fill(event.recHits_energy[iRecHit])
                histos["recHit_energy_allHitsRing"+str(event.recHits_rr[iRecHit])+"_ETL"].Fill(event.recHits_energy[iRecHit])

                if (event.recHits_energy[iRecHit] > maxRecHitEnergy):
                    maxRecHitEnergy = event.recHits_energy[iRecHit]
                if (dR < cut_dR):
                    recHit_matched_totalE_ETL += event.recHits_energy[iRecHit]
                    if (event.recHits_energy[iRecHit] > maxRecHitEnergy_dRpass):
                        maxRecHitEnergy_dRpass = event.recHits_energy[iRecHit]
            histos["recHit_energy_dR05_withTrackETL"].Fill(recHit_matched_totalE_ETL)
            histos["recHit_energy_dR05_withTrackETL_fixedRange"].Fill(recHit_matched_totalE_ETL)
            histos["recHit_maxEnergy_withTrackETL"].Fill(maxRecHitEnergy)
            histos["recHit_maxEnergy_dRpass_withTrackETL"].Fill(maxRecHitEnergy_dRpass)
            if(recHit_matched_totalE_ETL > threshold_depositE ):
                histos["track_eta_atETL_overThreshE"].Fill(abs(event.track_eta_atETL[itrack]))
                histos["track_phi_atETL_overThreshE"].Fill(abs(event.track_phi_atETL[itrack]))
                histos["track_pt_atETL_overThreshE"].Fill(event.track_pt[itrack])

        ############################################################################################3


        # Ang
        if (event.track_eta_atBTL[itrack]>-100.):  #if the track is from BTL
            for irecHit in range(0,event.recHits_n):   #loop over all recHits
                if (M.sqrt(pow((event.track_eta[itrack]-event.recHits_eta[irecHit]),2)+pow(event.track_phi[itrack]-event.recHits_phi[irecHit],2))<0.5):
                    recHit_energy_totalval_BTL+=event.recHits_energy[irecHit]
                    n_recHits_BTL+=1
                    #print "For BTL and %d th track, energy: %f" % (itrack,event.recHits_energy[irecHit])
            histos["BTLrecHit_energy_h"].Fill(recHit_energy_totalval_BTL)
            if(n_recHits_BTL>0):
                histos["BTLtrack_eta_sel"].Fill(abs(event.track_eta[itrack]))
                histos["BTLtrack_phi_sel"].Fill(event.track_phi[itrack])
            
        else :
            for irecHit in range(0,event.recHits_n):   #loop over all recHits
                if (M.sqrt(pow((event.track_eta[itrack]-event.recHits_eta[irecHit]),2)+pow(event.track_phi[itrack]-event.recHits_phi[irecHit],2))):
                    recHit_energy_totalval_ETL+=event.recHits_energy[irecHit]
                    n_recHits_ETL+=1
                    #print "For ETL and %d th track, energy: %f" % (itrack,event.recHits_energy[irecHit])
            histos["ETLrecHit_energy_h"].Fill(recHit_energy_totalval_ETL)
            if(n_recHits_ETL>0):
                histos["ETLtrack_eta_sel"].Fill(abs(event.track_eta[itrack]))
                histos["ETLtrack_phi_sel"].Fill(event.track_phi[itrack])
            
        histos["track_pt"].Fill(event.track_pt[itrack])
        histos["track_eta"].Fill(abs(event.track_eta[itrack]))
        if ((n_recHits_BTL+n_recHits_ETL)>0):
            histos["track_eta_sel"].Fill(abs(event.track_eta[itrack]))
            histos["track_phi_sel"].Fill(event.track_phi[itrack])
        if (event.track_pt[itrack]<1.):
            histos["track_eta_lowPt"].Fill(abs(event.track_eta[itrack]))
        histos["track_phi"].Fill(event.track_phi[itrack])
        
        if (event.track_hasMTD[itrack]>0):
            t_off = t_offset['BTL'] if event.track_eta_atBTL[itrack]>-100. else t_offset['ETL']
            histos["mtdTrack_pt"].Fill(event.track_pt[itrack])
            histos["mtdTrack_eta"].Fill(abs(event.track_eta[itrack]))
            if (event.track_pt[itrack]<1.):
                histos["mtdTrack_eta_lowPt"].Fill(abs(event.track_eta[itrack]))
            histos["mtdTrack_phi"].Fill(event.track_phi[itrack])
            histos["mtdTrack_dt"].Fill(event.track_t[itrack]-event.track_mcMatch_genVtx_t[itrack]-t_off)
            histos["mtdTrack_dt_vs_pt"].Fill(event.track_pt[itrack],event.track_t[itrack]-event.track_mcMatch_genVtx_t[itrack]-t_off)
            histos["mtdTrack_dt_vs_eta"].Fill(abs(event.track_eta[itrack]),event.track_t[itrack]-event.track_mcMatch_genVtx_t[itrack]-t_off)
            histos["mtdTrack_dz"].Fill(event.track_z[itrack]-event.track_mcMatch_genVtx_z[itrack])
            histos["mtdTrack_dz_vs_pt"].Fill(event.track_pt[itrack],event.track_z[itrack]-event.track_mcMatch_genVtx_z[itrack])
            histos["mtdTrack_dz_vs_eta"].Fill(abs(event.track_eta[itrack]),event.track_z[itrack]-event.track_mcMatch_genVtx_z[itrack])
            histos["mtdTrack_ptRes"].Fill(event.track_pt[itrack]/event.track_mcMatch_genPt[itrack]-1.)
            histos["mtdTrack_ptRes_vs_pt"].Fill(event.track_pt[itrack],event.track_pt[itrack]/event.track_mcMatch_genPt[itrack]-1.)
            histos["mtdTrack_ptRes_vs_eta"].Fill(abs(event.track_eta[itrack]),event.track_pt[itrack]/event.track_mcMatch_genPt[itrack]-1.)

        for det in ["BTL","ETL"]:
            if ( 
                abs(event.track_eta[itrack]) < etaCut[det][0] or
                abs(event.track_eta[itrack]) > etaCut[det][1]
                ):
                continue
            
            histos[det+"track_pt"].Fill(event.track_pt[itrack])
            histos[det+"track_eta"].Fill(abs(event.track_eta[itrack]))
            #if( (det=="BTL") and (n_recHits_BTL>0)):
            #    histos[det+"track_eta_sel"].Fill(abs(event.track_eta[itrack]))
            #    histos[det+"track_phi_sel"].Fill(event.track_phi[itrack])
            #if( (det=="ETL") and (n_recHits_ETL>0)):
            #    histos[det+"track_eta_sel"].Fill(abs(event.track_eta[itrack]))
            #    histos[det+"track_phi_sel"].Fill(event.track_phi[itrack])
            if (event.track_pt[itrack]<1.):
                histos[det+"track_eta_lowPt"].Fill(abs(event.track_eta[itrack]))
            histos[det+"track_phi"].Fill(event.track_phi[itrack])

            goodClusters=0
            bestClus=-1
            bestDR=9999
            for iclus in range(0,event.matchedClusters_n[itrack]):
                if (event.matchedClusters_time[itrack][iclus]>20):
                    continue
                if (event.matchedClusters_det[itrack][iclus]!=det_id[det]):
                    continue
                goodClusters=goodClusters+1
                if (event.matchedClusters_track_DR[itrack][iclus]<bestDR):
                    bestDR=event.matchedClusters_track_DR[itrack][iclus]
                    bestClus=iclus
                histos[det+"matchedCluster_energy"].Fill(event.matchedClusters_energy[itrack][iclus])
                histos[det+"matchedCluster_time"].Fill(event.matchedClusters_time[itrack][iclus])
                histos[det+"matchedCluster_DR"].Fill(event.matchedClusters_track_DR[itrack][iclus])
                histos[det+"matchedCluster_size"].Fill(event.matchedClusters_size[itrack][iclus])
                histos[det+"matchedCluster_size_vs_pt"].Fill(event.track_pt[itrack],event.matchedClusters_size[itrack][iclus])
                histos[det+"matchedCluster_size_vs_eta"].Fill(event.track_eta[itrack],event.matchedClusters_size[itrack][iclus])
                histos[det+"matchedCluster_sizeX"].Fill(event.matchedClusters_size_x[itrack][iclus])
                histos[det+"matchedCluster_sizeY"].Fill(event.matchedClusters_size_y[itrack][iclus])

            if (goodClusters>0):
                histos[det+"matchedClusterTrack_pt"].Fill(event.track_pt[itrack])
                histos[det+"matchedClusterTrack_eta"].Fill(abs(event.track_eta[itrack]))
                histos[det+"matchedClusterTrack_phi"].Fill(event.track_phi[itrack])

            if (bestClus>=0):
                histos[det+"bestCluster_energy"].Fill(event.matchedClusters_energy[itrack][bestClus])
                histos[det+"bestCluster_time"].Fill(event.matchedClusters_time[itrack][bestClus])
                histos[det+"bestCluster_time_vs_pt"].Fill(event.track_pt[itrack],event.matchedClusters_time[itrack][bestClus])
                histos[det+"bestCluster_time_vs_eta"].Fill(abs(event.track_eta[itrack]),event.matchedClusters_time[itrack][bestClus])
                histos[det+"bestCluster_DR"].Fill(event.matchedClusters_track_DR[itrack][bestClus])
                histos[det+"bestCluster_DEta"].Fill(event.matchedClusters_track_Deta[itrack][bestClus])
                histos[det+"bestCluster_DPhi"].Fill(event.matchedClusters_track_Dphi[itrack][bestClus])
                if (event.track_hasMTD[itrack]>0):
                    histos[det+"bestCluster_hasMTD_DR"].Fill(event.matchedClusters_track_DR[itrack][bestClus])
                    histos[det+"bestCluster_hasMTD_DEta"].Fill(event.matchedClusters_track_Deta[itrack][bestClus])
                    histos[det+"bestCluster_hasMTD_DPhi"].Fill(event.matchedClusters_track_Dphi[itrack][bestClus])
                histos[det+"bestCluster_size"].Fill(event.matchedClusters_size[itrack][bestClus])
                histos[det+"bestCluster_size_vs_pt"].Fill(event.track_pt[itrack],event.matchedClusters_size[itrack][bestClus])
                histos[det+"bestCluster_size_vs_eta"].Fill(event.track_eta[itrack],event.matchedClusters_size[itrack][bestClus])
                histos[det+"bestCluster_sizeX"].Fill(event.matchedClusters_size_x[itrack][bestClus])
                histos[det+"bestCluster_sizeY"].Fill(event.matchedClusters_size_y[itrack][bestClus])
                histos[det+"matchedBestClusterTrack_pt"].Fill(event.track_pt[itrack])
                histos[det+"matchedBestClusterTrack_eta"].Fill(abs(event.track_eta[itrack]))
                if (event.track_pt[itrack]<1.):
                    histos[det+"matchedBestClusterTrack_eta_lowPt"].Fill(abs(event.track_eta[itrack]))
                histos[det+"matchedBestClusterTrack_phi"].Fill(event.track_phi[itrack])

            histos[det+"matchedTrack_nCluster"].Fill(goodClusters)

            if (args.dumpHits):    
                goodRecHits=0
                bestHit=-1
                bestDR=9999
                for ihit in range(0,event.matchedRecHits_n[itrack]):
                    if (event.matchedRecHits_time[itrack][ihit]>20):
                        continue
                    if (event.matchedRecHits_det[itrack][ihit]!=det_id[det]):
                        continue
                    goodRecHits=goodRecHits+1
                    if (event.matchedRecHits_track_DR[itrack][ihit]<bestDR):
                        bestDR=event.matchedRecHits_track_DR[itrack][ihit]
                        bestHit=ihit
                    histos[det+"matchedRecHit_energy"].Fill(event.matchedRecHits_energy[itrack][ihit])
                    histos[det+"matchedRecHit_time"].Fill(event.matchedRecHits_time[itrack][ihit])
                    histos[det+"matchedRecHit_DR"].Fill(event.matchedRecHits_track_DR[itrack][ihit])
                
                    if (goodRecHits>0):
                        histos[det+"matchedRecHitTrack_pt"].Fill(event.track_pt[itrack])
                        histos[det+"matchedRecHitTrack_eta"].Fill(abs(event.track_eta[itrack]))
                        histos[det+"matchedRecHitTrack_phi"].Fill(event.track_phi[itrack])
                    
                    if (bestHit>=0):
                        histos[det+"bestRecHit_energy"].Fill(event.matchedRecHits_energy[itrack][bestHit])
                        histos[det+"bestRecHit_time"].Fill(event.matchedRecHits_time[itrack][bestHit])
                        histos[det+"bestRecHit_DR"].Fill(event.matchedRecHits_track_DR[itrack][bestHit])
                        histos[det+"bestRecHit_time_vs_pt"].Fill(event.track_pt[itrack],event.matchedRecHits_time[itrack][bestHit])
                        histos[det+"bestRecHit_time_vs_eta"].Fill(abs(event.track_eta[itrack]),event.matchedRecHits_time[itrack][bestHit])
                        histos[det+"matchedBestRecHitTrack_pt"].Fill(event.track_pt[itrack])
                        histos[det+"matchedBestRecHitTrack_eta"].Fill(abs(event.track_eta[itrack]))
                        histos[det+"matchedBestRecHitTrack_phi"].Fill(event.track_phi[itrack])

                histos[det+"matchedTrack_nRecHits"].Fill(goodRecHits)
    
histos["eff_eta"].Divide(histos["track_eta_sel"],histos["track_eta"])
histos["eff_phi"].Divide(histos["track_phi_sel"],histos["track_phi"])
histos["ETLeff_eta"].Divide(histos["ETLtrack_eta_sel"],histos["ETLtrack_eta"])
histos["ETLeff_phi"].Divide(histos["ETLtrack_phi_sel"],histos["ETLtrack_phi"])
histos["BTLeff_eta"].Divide(histos["BTLtrack_eta_sel"],histos["BTLtrack_eta"])
histos["BTLeff_phi"].Divide(histos["BTLtrack_phi_sel"],histos["BTLtrack_phi"])

for det in ["BTL","ETL"]:
    histos[det+"effCluster_pt"]=R.TGraphAsymmErrors( histos[det+"matchedClusterTrack_pt"], histos[det+"track_pt"])
    histos[det+"effCluster_eta"]=R.TGraphAsymmErrors(histos[det+"matchedClusterTrack_eta"],histos[det+"track_eta"])
    histos[det+"effCluster_phi"]=R.TGraphAsymmErrors(histos[det+"matchedClusterTrack_phi"],histos[det+"track_phi"])

    histos[det+"effBestCluster_pt"]=R.TGraphAsymmErrors( histos[det+"matchedBestClusterTrack_pt"], histos[det+"track_pt"])
    histos[det+"effBestCluster_eta"]=R.TGraphAsymmErrors(histos[det+"matchedBestClusterTrack_eta"],histos[det+"track_eta"])
    histos[det+"effBestCluster_eta_lowPt"]=R.TGraphAsymmErrors(histos[det+"matchedBestClusterTrack_eta_lowPt"],histos[det+"track_eta_lowPt"])
    histos[det+"effBestCluster_phi"]=R.TGraphAsymmErrors(histos[det+"matchedBestClusterTrack_phi"],histos[det+"track_phi"])

    histos[det+"effMtd_DR"]=R.TGraphAsymmErrors( histos[det+"bestCluster_hasMTD_DR"], histos[det+"bestCluster_DR"])
    histos[det+"effMtd_DEta"]=R.TGraphAsymmErrors( histos[det+"bestCluster_hasMTD_DEta"], histos[det+"bestCluster_DEta"])
    histos[det+"effMtd_DPhi"]=R.TGraphAsymmErrors( histos[det+"bestCluster_hasMTD_DPhi"], histos[det+"bestCluster_DPhi"])

    histos[det+"effRecHit_pt"]=R.TGraphAsymmErrors( histos[det+"matchedRecHitTrack_pt"],histos [det+"track_pt"])
    histos[det+"effRecHit_eta"]=R.TGraphAsymmErrors(histos[det+"matchedRecHitTrack_eta"],histos[det+"track_eta"])
    histos[det+"effRecHit_phi"]=R.TGraphAsymmErrors(histos[det+"matchedRecHitTrack_phi"],histos[det+"track_phi"])

    histos[det+"effBestRecHit_pt"]=R.TGraphAsymmErrors( histos[det+"matchedBestRecHitTrack_pt"], histos[det+"track_pt"])
    histos[det+"effBestRecHit_eta"]=R.TGraphAsymmErrors(histos[det+"matchedBestRecHitTrack_eta"],histos[det+"track_eta"])
    histos[det+"effBestRecHit_phi"]=R.TGraphAsymmErrors(histos[det+"matchedBestRecHitTrack_phi"],histos[det+"track_phi"])

    #BBT
    histos["track_pt_at"+det]=R.TGraphAsymmErrors( histos["track_pt_at"+det+"_overThreshE"], histos["track_pt_at"+det])
    histos["track_eta_at"+det]=R.TGraphAsymmErrors( histos["track_eta_at"+det+"_overThreshE"], histos["track_eta_at"+det])
    histos["track_phi_at"+det]=R.TGraphAsymmErrors( histos["track_phi_at"+det+"_overThreshE"], histos["track_phi_at"+det])

    # still BBT, but occupancy stuff now
    for bin in range(0, histos["recHit_energy_allHitsAllRings_"+det].GetXaxis().GetNbins()):        
        histos["h_occupancy_numerator_allHitsAllRings_"+det].SetBinContent( bin, histos["recHit_energy_allHitsAllRings_"+det].Integral(bin, histos["recHit_energy_allHitsAllRings_"+det].GetXaxis().GetNbins()+1) )
        histos["h_occupancy_denominator_allHitsAllRings_"+det].SetBinContent( bin, histos["recHit_energy_allHitsAllRings_"+det].Integral(0, histos["recHit_energy_allHitsAllRings_"+det].GetXaxis().GetNbins()+1) )
        if det == "ETL": # occupancy split by ring
            for iRing in range(1,12):
                histos["h_occupancy_numerator_allHitsRing"+str(iRing)+"_"+det].SetBinContent( bin, histos["recHit_energy_allHitsRing"+str(iRing)+"_"+det].Integral(bin, histos["recHit_energy_allHitsRing"+str(iRing)+"_"+det].GetXaxis().GetNbins()+1) )
                histos["h_occupancy_denominator_allHitsRing"+str(iRing)+"_"+det].SetBinContent( bin, histos["recHit_energy_allHitsRing"+str(iRing)+"_"+det].Integral(0, histos["recHit_energy_allHitsRing"+str(iRing)+"_"+det].GetXaxis().GetNbins()+1) )

    histos["recHit_occupancy_VS_energy_allRings_"+det]=R.TGraphAsymmErrors( histos["h_occupancy_numerator_allHitsAllRings_"+det], histos["h_occupancy_denominator_allHitsAllRings_"+det] )
    histos["recHit_occupancy_VS_energy_allRings_"+det].SetTitle("recHit_occupancy_VS_energy_allRings_"+det)
    histos["recHit_occupancy_VS_energy_allRings_"+det].SetName("recHit_occupancy_VS_energy_allRings_"+det)
    if det == "ETL": # occupancy split by ring
        for iRing in range(1,12):
            histos["recHit_occupancy_VS_energy_Ring"+str(iRing)+"_"+det]=R.TGraphAsymmErrors( histos["h_occupancy_numerator_allHitsRing"+str(iRing)+"_"+det], histos["h_occupancy_denominator_allHitsRing"+str(iRing)+"_"+det] )
            histos["recHit_occupancy_VS_energy_Ring"+str(iRing)+"_"+det].SetTitle("recHit_occupancy_VS_energy_Ring"+str(iRing)+"_"+det)
            histos["recHit_occupancy_VS_energy_Ring"+str(iRing)+"_"+det].SetName("recHit_occupancy_VS_energy_Ring"+str(iRing)+"_"+det)

histos["effMtd_pt"]= R.TGraphAsymmErrors(histos["mtdTrack_pt"],histos["track_pt"])
histos["effMtd_eta"]=R.TGraphAsymmErrors(histos["mtdTrack_eta"],histos["track_eta"])
histos["effMtd_eta_lowPt"]=R.TGraphAsymmErrors(histos["mtdTrack_eta_lowPt"],histos["track_eta_lowPt"])
histos["effMtd_phi"]=R.TGraphAsymmErrors(histos["mtdTrack_phi"],histos["track_phi"])

fOut=R.TFile(args.output,"RECREATE")
for hn, histo in histos.iteritems():
    if isinstance(histo,R.TH1F):
        histo.SetMinimum(0.)
    if isinstance(histo,R.TGraphAsymmErrors):
        histo.SetMinimum(0.)
        histo.SetMaximum(1.1)
    histo.Write()
fOut.Close()
print "Saved histos in "+args.output
