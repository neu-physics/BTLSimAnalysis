import ROOT as R
import math as M
import argparse
import subprocess
import numpy as np
import os
from array import array

def goodTrack(evt, itrack , chi2cut, skipMCmatching):
    #acceptance cuts
    if (evt.track_pt[itrack]<0.7):
        return False
    if (abs(evt.track_eta[itrack])>3.):
        return False
    #for the moment use matching with mc gen particle
    if (abs(evt.track_mcMatch_DR[itrack])>0.05 and not skipMCmatching):
        return False
    if (abs(evt.track_pt[itrack]/evt.track_mcMatch_genPt[itrack]-1.)>0.1 and not skipMCmatching):
        return False
#    if (evt.track_eta_atBTL[itrack]<-100 and evt.track_eta_atETL[itrack]<-100):
#        return False
    return True

def goodSim(l,isim):
  over = True
  for i in range (0,len(l)):
    if (isim==l[i]):
      #print ("aha %f is excluded E: %f" %(l[i]))
      over = False
  if (over): 
    return True
  elif (not over):
    return False


def goodHit(evt, iHit, l):
  max_sim_E = 0
  idx = -1
  matched = False
  n_sim = 0
  if ((evt.recHits_det[iHit]!=1) or (evt.recHits_energy[iHit]<3)): 
    return False
  for iSim in range (0,evt.simHits_n):
    if ((evt.simHits_det[iSim]!=1) or (evt.simHits_energy[iSim]<3)): continue
    if (not goodSim(l, iSim)): continue
    dR = M.sqrt((evt.recHits_eta[iHit]-evt.simHits_eta[iSim])**2+(evt.recHits_phi[iHit]-evt.simHits_phi[iSim])**2)
    if ( (dR < 0.05) and (evt.simHits_energy[iSim]>max_sim_E)):
      max_sim_E = evt.simHits_energy[iSim]
      idx = iSim
      matched = True
  l.append(idx)
  #print ("exluded %f: E: %f" %(idx,max_sim_E))
  if (matched):
    histos["n_match_sim"].Fill(1)
    return True
  elif (not matched):
    histos["n_match_sim"].Fill(0)
    return False

parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')
parser.add_argument('--inputDir',dest='inputDir')
parser.add_argument('--pattern',dest='pattern')
parser.add_argument('--output',dest='output')
parser.add_argument('--chi2cut',dest='chi2cut')
parser.add_argument('--events',dest='events',default='-1')

args = parser.parse_args()

if (args.inputDir != "" and args.inputDir !=None):
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
    f=R.TFile.Open(args.input)
    dh=f.Get("DumpHits")

histos = {}

histos["eta_clus_hits"]=R.TH1F("eta_clus_hits","eta_clus_hits",300,-3,3)
histos["phi_clus_hits"]=R.TH1F("phi_clus_hits","phi_clus_hits",320,-3.2,3.2)
histos["E_clus_hits"]=R.TH1F("E_clus_hits","E_clus_hits",20,0,20)
histos["n_match_sim"]=R.TH1F("n_match_sim","n_match_sim",10,0,10)
histos["n_match_rec"]=R.TH1F("n_match_rec","n_match_rec",10,0,10)
histos["n_good_hit"]=R.TH1F("n_good_hit","n_good_hit",10,0,10)
histos["n_break_1"]=R.TH1F("n_break_1","n_break_1",20,0,20)
histos["num_clus"]=R.TH1F("num_clus","num_clus",10,0,10)
histos["clus_sim_eta"]=R.TH1F("clus_sim_eta","clus_sim_eta",80,-1.6,1.6)
histos["clus_sim_phi"]=R.TH1F("clus_sim_phi","clus_sim_phi",160,-3.2,3.2)
histos["clus_hit_eta"]=R.TH1F("clus_hit_eta","clus_hit_eta",80,-1.6,1.6)
histos["clus_hit_phi"]=R.TH1F("clus_hit_phi","clus_hit_phi",160,-3.2,3.2)
histos["dR_sim_gen"]=R.TH1F("dR_sim_gen","dR_sim_gen",100,0,0.101)
histos["dR_sim_hit"]=R.TH1F("dR_sim_hit","dR_sim_hit",200,0,10)
histos["dR_ele_sim"]=R.TH1F("dR_ele_sim","dR_ele_sim",100,0,5)
histos["dR_clus_gen"]=R.TH1F("dR_clus_gen","dR_clus_gen",200,0,6)
histos["clus_size"]=R.TH1F("clus_size","clus_size",7,0,7)
histos["clus_size_matched"]=R.TH1F("clus_size_matched","clus_size_matched",7,0,7)
histos["n_mat_clus_gen"]=R.TH1F("n_mat_clus_gen","n_mat_clus_gen",40,0,40)

histos["n_mat_hit_gen"]=R.TH1F("n_mat_hit_gen","n_mat_hit_gen",30,0,30)
histos["eff_per_bin"]=R.TH1F("eff_per_bin","eff_per_bin",10,0,10)

histos["n_true_hits"]=R.TH1F("n_true_hits","n_true_hits",10,0,10)
histos["n_good_hits"]=R.TH1F("n_good_hits","n_good_hits",10,0,10)


num_good_clus = 0  
num_tot_clus = 0
num_mat_clus = 0
n_true_hits = 0
n_good_hits = 0
break_1 = 0
break_2 = 0
n_false_hits = 0
n_bad_hits = 0
n_h = 0
n_h_m = 0
all_hit = 0
mat_list = array('d',[0,0,0,0,0,0,0,0,0,0])
all_list = array('d',[0,0,0,0,0,0,0,0,0,0])
for ievent,event in enumerate(dh):
    if (int(args.events) != -1 and ievent>int(args.events)):
        break
    if (ievent%100==0):
        print "Analysing event %d"%ievent
    '''  
    for nrec in range(0,event.recHits_n):
      if ( (event.recHits_det[nrec]!=1) or (event.recHits_energy[nrec]<3)): continue
      n_matched_sim = 0
      for nsim in range(0,event.simHits_n):
        if ( (event.simHits_det[nsim]!=1) or (event.simHits_energy[nsim]<3) ): continue
        dR_rs = M.sqrt((event.recHits_eta[nrec]-event.simHits_eta[nsim])**2+(event.recHits_phi[nrec]-event.simHits_phi[nsim])**2)
        if (dR_rs<0.02):
          n_matched_sim += 1
      histos["n_match_sim"].Fill(n_matched_sim)


    for nsim in range(0,event.simHits_n):
      if ( (event.simHits_det[nsim]!=1) or (event.simHits_energy[nsim]<3) ): continue
      n_matched_rec = 0
      for nrec in range(0,event.recHits_n):
        if ( (event.recHits_det[nrec]!=1) or (event.recHits_energy[nrec]<3)): continue
        dR_rs = M.sqrt((event.recHits_eta[nrec]-event.simHits_eta[nsim])**2+(event.recHits_phi[nrec]-event.simHits_phi[nsim])**2)
        if (dR_rs<0.02):
          n_matched_rec += 1
      histos["n_match_rec"].Fill(n_matched_rec)
      '''

    exc = []      #simHits idx that is already matched (excluded)
    for iRec in range(0,event.recHits_n):
      #if ( (event.recHits_det[iRec]!=1) or (event.recHits_energy[iRec]<3)): continue
      #max_sim_pT = 0
      #for iSim in range(0,event.simHits_n):
      #  if ( (event.simHits_det[iSim]!=1) or (event.simHits_energy[iSim]<3) ): continue
      #  dR_rec_sim = M.sqrt((event.recHits_eta[iRec]-event.simHits_eta[iSim])**2+(event.recHits_phi[iRec]-event.simHits_phi[iSim])**2)
      #  if ((dR_rec_sim<0.05) and (event.simHits_pT[iSim] > max_sim_pT)):
      #    max_sim_pT = event.simHits_pT[iSim]
      if (event.recHits_det[iRec]==1):
        all_hit += 1
      if (not goodHit(event,iRec,exc)): 
        #histos["n_match_sim"].Fill(0)
        n_false_hits += 1
        continue    
      n_true_hits += 1
      #histos["n_match_sim"].Fill(1)
      #break
    #for n in range(0,len(exc)):
      #print ("id: %f E: %f" %(exc[n],event.simHits_energy[exc[n]]))
    
    for nGen in range (0,len(event.GenPart_eta)):
      n_mat_clus_gen = 0
      n_mat_hit_gen = 0

      for nHits in range (0,event.recHits_n):
        dR_hit_gen = M.sqrt((event.GenPart_eta[nGen]-event.recHits_eta[nHits])**2+(event.GenPart_phi[nGen]-event.recHits_phi[nHits])**2)
        if (dR_hit_gen<0.05):
          n_mat_hit_gen += 1

      for nClus in range (0,event.clusters_n):
        dR_clu_gen = M.sqrt((event.GenPart_eta[nGen]-event.clusters_eta[nClus])**2+(event.GenPart_phi[nGen]-event.clusters_phi[nClus])**2)
        if (dR_clu_gen<0.3):
          n_mat_clus_gen += 1
      histos["n_mat_clus_gen"].Fill(n_mat_clus_gen)
      histos["n_mat_hit_gen"].Fill(n_mat_hit_gen)
    
    used = []
    #for iGen in range(0,len(event.GenPart_eta)):
    #num_tot_clus += event.clusters_n
    for iClus in range (0,event.clusters_n):
      n_matched_hits = 0
      if (event.clusters_det[iClus]!=1):  continue
      num_tot_clus += 1
      n_h += event.clusters_size[iClus]
      for iGen in range(0,len(event.GenPart_eta)):
        dR_clu_gen = M.sqrt((event.GenPart_eta[iGen]-event.clusters_eta[iClus])**2+(event.GenPart_phi[iGen]-event.clusters_phi[iClus])**2)
        histos["dR_clus_gen"].Fill(dR_clu_gen)
        if (dR_clu_gen>0.3): continue
        num_mat_clus += 1
        n_h_m += event.clusters_size[iClus]
        histos["clus_size"].Fill(event.clusters_size[iClus])
        for ihit in range (0,event.clusters_size[iClus]):
          #n_h += 1
          max_E = 0
          sim_idx = -1
          good_hit = False
          if ( (event.clusters_hit_energy[iClus][ihit]<3) ): 
            n_bad_hits += 1
            continue
          for isim in range (0,event.simHits_n):
            if ( event.simHits_energy[isim]<3 ): continue
            if (not goodSim(used,isim)): continue
            dR_sim_gen = M.sqrt((event.simHits_eta[isim]-event.GenPart_eta[iGen])**2+(event.simHits_phi[isim]-event.GenPart_phi[iGen])**2)
            dR_hit_sim = M.sqrt((event.clusters_hit_eta[iClus][ihit]-event.simHits_eta[isim])**2+(event.clusters_hit_phi[iClus][ihit]-event.simHits_phi[isim])**2)
            if (dR_hit_sim>0.05): continue
            
            right_sim = True
            for iele in range(0,len(event.GenPart_eta)):
              dR_com = M.sqrt((event.simHits_eta[isim]-event.GenPart_eta[iele])**2+(event.simHits_phi[isim]-event.GenPart_phi[iele])**2)
              if ((event.GenPart_id[iGen]!=event.GenPart_id[iele]) and (dR_com < dR_sim_gen)):
                right_sim = False
                break
            if (not right_sim): continue
            if (max_E<event.simHits_energy[isim]):
              good_hit = True
              max_E = event.simHits_energy[isim]
              sim_idx = isim
          used.append(sim_idx)
          if(good_hit):
            n_matched_hits += 1
            n_good_hits += 1
          else:
            n_bad_hits += 1
        if (event.clusters_size[iClus]<10):
          all_list[event.clusters_size[iClus]] += event.clusters_size[iClus]
          mat_list[event.clusters_size[iClus]] += n_matched_hits
        histos["clus_size_matched"].Fill(n_matched_hits)

eff_bins = array('d',[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.])
for n in range (0,10):
  #print mat_list[n]
  #print all_list[n]
  nbin = histos["eff_per_bin"].FindBin(n)
  histos["eff_per_bin"].SetBinContent(nbin,mat_list[n])
  if (all_list[n]!=0):
    eff_bins[n] = (1.0*mat_list[n])/n_true_hits
    #print eff_bins[n]
  else:
    eff_bins[n] = 0.

eff_x = array('d',[0,1,2,3,4,5,6,7,8,9])
histos["eff_bins"] = R.TGraph(10,eff_x,eff_bins)
histos["n_good_hits"].SetBinContent(1,n_good_hits)
histos["n_true_hits"].SetBinContent(1,n_true_hits)
eff_t = (1.0*n_good_hits)/n_true_hits
ineff = (1.0*n_bad_hits)/n_false_hits
print ("%f  %f  eff_total: %f " % (n_good_hits, n_true_hits, eff_t))
print ("%f  %f  eff_bad: %f" % (n_false_hits, n_bad_hits, ineff))
#print (n_h)
print ("%d    %d    %d    %d    %d    %d" % (num_tot_clus, num_mat_clus, all_hit, n_true_hits, n_good_hits, n_h_m))
#print (num_tot_clus)
#print (num_mat_clus)
print (all_hit)
#print (n_true_hits)
#print (n_good_hits)
#print (n_h_m)
#print ((1.0*n_h)/num_tot_clus)
#print ((1.0*n_h_m)/num_mat_clus)
#print ((1.0*n_good_hits)/num_mat_clus)
#print ((1.0*all_hit)/num_tot_clus)
#print ((1.0*all_hit)/num_mat_clus)
#print ((1.0*n_true_hits)/num_mat_clus)
#





#Check to see if output directory exists. if not, create it
outputDir = args.output.split('/')[0]
if (not os.path.exists("./"+outputDir)):
    os.system("mkdir "+outputDir)

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
