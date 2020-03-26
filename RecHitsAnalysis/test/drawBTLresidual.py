import ROOT as R
import math as M
import argparse
import subprocess
import numpy as np
import os

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

parser = argparse.ArgumentParser()
parser.add_argument('--input',dest='input')
parser.add_argument('--inputDir',dest='inputDir')
parser.add_argument('--pattern',dest='pattern')
parser.add_argument('--output',dest='output')
parser.add_argument('--layout',dest='layout')
parser.add_argument('--chi2cut',dest='chi2cut')
parser.add_argument('--events',dest='events',default='-1')
parser.add_argument('--firstEvent',dest='firstEvent', default='0')
parser.add_argument('--dumpHits',dest='dumpHits',action='store_true',default=False)
parser.add_argument('--dumpAll',dest='dumpAll',action='store_true',default=False)

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


histos["BTLrecHits_length1_minus_length2"]=R.TH1F("BTLrecHits_length1_minus_length2","BTLrecHits_length1_minus_length2",50,-0.5,0.5)
histos["BTLrecHits_total_length"]=R.TH1F("BTLrecHits_total_length","BTLrecHits_total_length",150,-500,1000)
histos["BTLrecHits_length_1"]=R.TH1F("BTLrecHits_length_1","BTLrecHits_length_1",300,-100,200)
histos["BTLrecHits_length_2"]=R.TH1F("BTLrecHits_length_2","BTLrecHits_length_2",300,-100,200)  
histos["BTLrecHits_length_1_inside"]=R.TH1F("BTLrecHits_length_1_inside","BTLrecHits_length_1_inside",300,-100,200)
histos["BTLrecHits_length_2_inside"]=R.TH1F("BTLrecHits_length_2_inside","BTLrecHits_length_2_inside",300,-100,200)
histos["BTLrecHits_length_1_outside"]=R.TH1F("BTLrecHits_length_1_outside","BTLrecHits_length_1_outside",300,-100,200)
histos["BTLrecHits_length_2_outside"]=R.TH1F("BTLrecHits_length_2_outside","BTLrecHits_length_2_outside",300,-100,200)
histos["BTLrecHits_t1_travel_vs_t2_travel"]=R.TH2F("BTLrecHits_t1_travel_vs_t2_travel","BTLrecHits_t1_travel_vs_t2_travel",50,-2.,3.,50,-2.,3.)
histos["BTLrecHits_x1_vs_x2"]=R.TH2F("BTLrecHits_x1_vs_x2","BTLrecHits_x1_vs_x2",80,-50,120,80,-50,120)
histos["BTLrecHits_average_time"]=R.TH2F("BTLrecHits_average_time","BTLrecHits_average_time",300,0,60,300,0,60)
histos["BTLrecHits_t_travel_track_t0"]=R.TH2F("BTLrecHits_t_travel_track_t0","BTLrecHits_t_travel_track_t0",50,0,10,50,0,10)
histos["BTLrecHits_t_travel"]=R.TH2F("BTLrecHits_t_travel","BTLrecHits_t_travel",50,0,10,50,0,10)
histos["BTLrecHits_t_calc_minus_t_true"]=R.TH1F("BTLrecHits_t_calc_minus_t_true","BTLrecHits_t_calc_minus_t_true",2000,-2,2)
histos["BTLsimHits_z_local"]=R.TH1F("BTLsimHits_z_local","BTLsimHits_z_local",400,-10,10)
histos["BTLx1_calc_minus_x_true"]=R.TH1F("BTLx1_calc_minus_x_true","BTLx1_calc_minus_x_true",120,-30,30)
histos["BTLx2_calc_minus_x_true"]=R.TH1F("BTLx2_calc_minus_x_true","BTLx2_calc_minus_x_true",120,-30,30)
histos["BTLx1_calc_minus_x_true_inside"]=R.TH1F("BTLx1_calc_minus_x_true_inside","BTLx1_calc_minus_x_true_inside",120,-30,30)
histos["BTLx2_calc_minus_x_true_inside"]=R.TH1F("BTLx2_calc_minus_x_true_inside","BTLx2_calc_minus_x_true_inside",120,-30,30)
histos["BTLx1_calc_minus_x_true_outside"]=R.TH1F("BTLx1_calc_minus_x_true_outside","BTLx1_calc_minus_x_true_outside",120,-30,30)
histos["BTLx2_calc_minus_x_true_outside"]=R.TH1F("BTLx2_calc_minus_x_true_outside","BTLx2_calc_minus_x_true_outside",120,-30,30)
histos["BTL_total_length_"]=R.TH1F("BTL_total_length_","BTL_total_length_",40,-100,300)
histos["x_true_vs_t"]=R.TProfile("x_true_vs_t","x_true_vs_t",60,-30,30)
histos["res_x2_ave"]=R.TH1F("res_x2_ave","res_x2_ave",120,-30,30)
histos["res_x2_ave_inside"]=R.TH1F("res_x2_ave_inside","res_x2_ave_inside",120,-30,30)
histos["res_x2_ave_outside"]=R.TH1F("res_x2_ave_outside","res_x2_ave_outside",120,-30,30)
histos["res_x1_ave"]=R.TH1F("res_x1_ave","res_x1_ave",120,-30,30)
histos["res_x1_ave_inside"]=R.TH1F("res_x1_ave_inside","res_x1_ave_inside",120,-30,30)
histos["res_x1_ave_outside"]=R.TH1F("res_x1_ave_outside","res_x1_ave_outside",120,-30,30)


histos["BTLrecHits_total_length_tree"]=R.TH1F("BTLrecHits_total_length_tree","BTLrecHits_total_length_tree",150,-500,1000)
histos["BTLrecHits_length_1_tree"]=R.TH1F("BTLrecHits_length_1_tree","BTLrecHits_length_1_tree",300,-100,200)
histos["BTLrecHits_length_2_tree"]=R.TH1F("BTLrecHits_length_2_tree","BTLrecHits_length_2_tree",300,-100,200)
histos["BTLx1_calc_minus_x_true_tree"]=R.TH1F("BTLx1_calc_minus_x_true_tree","BTLx1_calc_minus_x_true_tree",120,-30,30)
histos["BTLx2_calc_minus_x_true_tree"]=R.TH1F("BTLx2_calc_minus_x_true_tree","BTLx2_calc_minus_x_true_tree",120,-30,30)




det_id = { 'BTL':1  , 'ETL':2 }
etaCut = { 'BTL':[0,1.5]  , 'ETL':[1.5,3] }

if (args.dumpAll):
    print "Dumping also non matched MTD hits"

if (args.dumpHits):
    print "Dumping RecHits"

for ievent,event in enumerate(dh):
    if (int(args.events) != -1 and ievent>int(args.events)):
        break
    if (ievent%500==0):
        print "Analysing event %d"%ievent
    
    speed_of_light = 0.13846235    
    #speed_of_light = 0.145
    #speed_of_light = 0.16472113 #in units of 1e+09		unit of time is ps(1e-12s)
    c = 0.299792458			#in units of 1e+09
    radius_of_BTL = 1.148
    Length_of_bar = 0.057

	
    #loop over uncalibrated recHits
    for iuncalRecHit in range(0,len(event.recHits_uncal_time1)):
        matchiTrack = -999.
        recHitMatched = False
        calibrateMatched = False
        #calculate the time it takes for the track to reach BTL
        angle = M.pi/2.0-2.0*M.atan(M.exp(-event.recHits_uncal_eta[iuncalRecHit]))
        distance_travelled = 100.0*radius_of_BTL/M.cos(angle)
        #t_travel = distance_travelled/c
        for nhit in range(0,event.recHits_n):
            if((event.recHits_uncal_eta[iuncalRecHit]==event.recHits_eta[nhit]) and (event.recHits_uncal_phi[iuncalRecHit]==event.recHits_phi[nhit])):
                calibrateMatched = True
                break
            if(not calibrateMatched):
                continue
        for iTrack in range(0,len(event.track_idx)):
            isNuGun_uncal = True if args.inputDir.find("NuGun")>0 else False
            if(not goodTrack(event,iTrack,args.chi2cut,isNuGun_uncal)):
                continue
            if(not event.track_eta_atBTL[iTrack]>-100.):
                continue
            if((event.track_velocity[iTrack]==0) or (event.track_length[iTrack]==0)):
                continue
            deltaR = M.sqrt(pow((event.track_eta_atBTL[iTrack]-event.recHits_uncal_eta[iuncalRecHit]),2)+pow(event.track_phi_atBTL[iTrack]-event.recHits_uncal_phi[iuncalRecHit],2))   
            if(deltaR<0.05):
                #distance_ref_to_recHit = M.sqrt((event.recHits_uncal_x[iuncalRecHit]-event.track_x[iTrack])*(event.recHits_uncal_x[iuncalRecHit]-event.track_x[iTrack])+(event.recHits_uncal_y[iuncalRecHit]-event.track_y[iTrack])*(event.recHits_uncal_y[iuncalRecHit]-event.track_y[iTrack])+(event.recHits_uncal_z[iuncalRecHit]-event.track_z[iTrack])*(event.recHits_uncal_z[iuncalRecHit]-event.track_z[iTrack]))
                #t_travelled = distance_ref_to_recHit*0.01/(event.track_velocity[iTrack]*c)+event.track_t[iTrack]
                t0 = event.track_mcMatch_genVtx_t[iTrack]
                t_travelled = (event.track_length[iTrack])*0.01/(event.track_velocity[iTrack]*c)+t0
                histos["BTLrecHits_t_travel"].Fill(t_travelled,event.track_tmtd[iTrack])
                #histos["BTLrecHits_t_travel_track_t0"].Fill(event.track_t[iTrack],t_travel)
                #histos["BTLrecHits_length_1"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[iuncalRecHit]-t_travelled))
                #histos["BTLrecHits_length_2"].Fill(1000.*speed_of_light*(event.recHits_uncal_time2[iuncalRecHit]-t_travelled))
                histos["BTLrecHits_t1_travel_vs_t2_travel"].Fill(event.recHits_uncal_time2[iuncalRecHit]-t_travelled,event.recHits_uncal_time1[iuncalRecHit]-t_travelled)
                histos["BTLrecHits_x1_vs_x2"].Fill(1000.*speed_of_light*(event.recHits_uncal_time2[iuncalRecHit]-t_travelled),1000.*speed_of_light*(event.recHits_uncal_time1[iuncalRecHit]-t_travelled))
                histos["BTLrecHits_length1_minus_length2"].Fill(speed_of_light*(event.recHits_uncal_time1[iuncalRecHit]-event.recHits_uncal_time2[iuncalRecHit]))
                histos["BTLrecHits_total_length"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[iuncalRecHit]+event.recHits_uncal_time2[iuncalRecHit]-2.0*t_travelled))
                matchiTrack = iTrack
                recHitMatched = True
                break
        if(not (recHitMatched == True)):
            continue
    
    for i_Track in range(0,len(event.track_idx)):
        t_calc = -999.
        t_true = -999.
        match_recHit = -999.
        match_simHit = -999.
        max_simHit_energy = 0.
        isNuGun_si = True if args.inputDir.find("NuGun")>0 else False
        if(not goodTrack(event,i_Track,args.chi2cut,isNuGun_si)):
            continue
        if(not event.track_eta_atBTL[i_Track]>-100.):
                continue
        if((event.track_velocity[i_Track]==0) or (event.track_length[i_Track]==0)):
                continue
        for i_RecHit in range(0,len(event.recHits_uncal_time1)):
            deltaR_rec = M.sqrt(pow((event.track_eta_atBTL[i_Track]-event.recHits_uncal_eta[i_RecHit]),2)+pow(event.track_phi_atBTL[i_Track]-event.recHits_uncal_phi[i_RecHit],2))
            if(deltaR_rec<0.05):
                t_calc = (event.recHits_uncal_time1[i_RecHit]+event.recHits_uncal_time2[i_RecHit]-(Length_of_bar/speed_of_light))/2.
                t_travelled_calc = (event.track_length[i_Track])*0.01/(event.track_velocity[i_Track]*c)+event.track_mcMatch_genVtx_t[i_Track]
                #t_travelled_calc = (event.track_length[i_Track])*0.01/(event.track_velocity[i_Track]*c)
                #t_travelled_calc = event.track_tmtd[i_Track]
                x1_calc = 2.85-100.*speed_of_light*(event.recHits_uncal_time1[i_RecHit]-t_travelled_calc)
                x2_calc = 100.*speed_of_light*(event.recHits_uncal_time2[i_RecHit]-t_travelled_calc)-2.85
                x1_ave = 28.5-0.5*((57.0-1000.*speed_of_light*(event.recHits_uncal_time2[i_RecHit]-t_travelled_calc))+1000.*speed_of_light*(event.recHits_uncal_time1[i_RecHit]-t_travelled_calc))
                x2_ave = 0.5*((57.0-1000.*speed_of_light*(event.recHits_uncal_time1[i_RecHit]-t_travelled_calc))+1000.*speed_of_light*(event.recHits_uncal_time2[i_RecHit]-t_travelled_calc))-28.5
                #x2_ave = 0.5*(1000.*speed_of_light*(event.recHits_uncal_time2[i_RecHit]-event.recHits_uncal_time1[i_RecHit]))
                match_recHit = i_RecHit
                histos["BTL_total_length_"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[i_RecHit]+event.recHits_uncal_time2[i_RecHit]-2.0*t_travelled_calc))
                histos["BTLrecHits_total_length_tree"].Fill(event.recHits_uncal_position_left[i_RecHit]+event.recHits_uncal_position_right[i_RecHit])
                break
        if(t_calc==-999.):
            continue
        for i_SimHit in range(0,event.simHits_n):
            deltaR_sim = M.sqrt(pow((event.track_eta_atBTL[i_Track]-event.simHits_eta[i_SimHit]),2)+pow(event.track_phi_atBTL[i_Track]-event.simHits_phi[i_SimHit],2))
            if(deltaR_sim<0.05):
                if(event.simHits_energy[i_SimHit]>max_simHit_energy):
                    match_simHit = i_SimHit
        if(match_simHit>=0 and match_recHit>=0):
            t_true = event.simHits_time[match_simHit]
            x_true = event.simHits_entry_local_x[match_simHit]
            
            histos["BTLx1_calc_minus_x_true"].Fill(10.*(x1_calc-x_true))
            histos["BTLx2_calc_minus_x_true"].Fill(10.*(x2_calc-x_true))
            histos["x_true_vs_t"].Fill(10.*x_true,1000.*(event.recHits_uncal_time2[match_recHit]-t_travelled_calc))
            histos["BTLrecHits_length_1"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[match_recHit]-t_travelled_calc))
            histos["BTLrecHits_length_2"].Fill(1000.*speed_of_light*(event.recHits_uncal_time2[match_recHit]-t_travelled_calc))
            histos["res_x2_ave"].Fill(x2_ave-10.*x_true)
            histos["res_x1_ave"].Fill(x1_ave-10.*x_true)
            
            histos["BTLrecHits_length_1_tree"].Fill(event.recHits_uncal_position_left[i_RecHit])
            histos["BTLrecHits_length_2_tree"].Fill(event.recHits_uncal_position_right[i_RecHit])
            histos["BTLx1_calc_minus_x_true_tree"].Fill((event.recHits_uncal_position_left[i_RecHit]-28.5)-10.*(x_true))
            histos["BTLx2_calc_minus_x_true_tree"].Fill(-(28.5-event.recHits_uncal_position_right[i_RecHit])-10.*(x_true))
            
            if(abs(event.simHits_entry_local_y[match_simHit])<1.0 and abs(event.simHits_entry_local_x[match_simHit])<0.1 and abs(event.simHits_entry_local_z[match_simHit])<0.13):
                histos["BTLrecHits_length_1_inside"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[match_recHit]-t_travelled_calc))
                histos["BTLrecHits_length_2_inside"].Fill(1000.*speed_of_light*(event.recHits_uncal_time2[match_recHit]-t_travelled_calc))
                histos["BTLx1_calc_minus_x_true_inside"].Fill(10.*(x1_calc-x_true))
                histos["BTLx2_calc_minus_x_true_inside"].Fill(10.*(x2_calc-x_true))
                histos["res_x2_ave_inside"].Fill(x2_ave-10.*x_true)
                histos["res_x1_ave_inside"].Fill(x1_ave-10.*x_true)
            
            else:
                histos["BTLrecHits_length_1_outside"].Fill(1000.*speed_of_light*(event.recHits_uncal_time1[match_recHit]-t_travelled_calc))
                histos["BTLrecHits_length_2_outside"].Fill(1000.*speed_of_light*(event.recHits_uncal_time2[match_recHit]-t_travelled_calc))
            
                histos["BTLx1_calc_minus_x_true_outside"].Fill(10.*(x1_calc-x_true))
                histos["BTLx2_calc_minus_x_true_outside"].Fill(10.*(x2_calc-x_true))
                histos["res_x1_ave_outside"].Fill(x1_ave-10.*x_true)
                histos["res_x2_ave_outside"].Fill(x2_ave-10.*x_true)




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
