import ROOT as R
import math as M
import argparse
import os

def Map(tf):
    """
    Maps objets as dict[obj_name][0] using a TFile (tf) and TObject to browse.
    """
    m = {}
    for k in tf.GetListOfKeys():
        n = k.GetName()
        m[n] = tf.Get(n)
    return m

def saveCanvas(c,n):
#    defaultTitle(0.1,0.93,args.title)
    for ext in ['.png','.pdf' ]:
        c.SaveAs(args.output+"/"+n+ext)

def defaultTitle(x,y,text):
    t=R.TLatex()
    t.SetTextSize(0.035)
    t.DrawLatexNDC(x,y,text)

parser = argparse.ArgumentParser()
parser.add_argument('--output',dest='output')
parser.add_argument('--title',dest='title')
parser.add_argument('--layout',dest='layout')
args = parser.parse_args()

f={}

f['muons_old']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10_pythia8/runHitsRelValSingleMuFlatPt0p7to10pythia8_v4/190108_064045/0000/drawTrackPerformance.root')
#f['muons']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10_pythia8/runHitsRelValSingleMuFlatPt0p7to10pythia8_v5/190111_145357/0000/drawTrackPerformance.root')
f['muons']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10_pythia8/runHitsRelValSingleMuFlatPt0p7to10pythia8_v7/190112_191612/0000/drawTrackPerformance.root')
f['muons_noMTD']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10_pythia8/runHitsRelValSingleMuFlatPt0p7to10pythia8_v7_noMTD/190113_065739/0000/drawTrackPerformance.root')

f['pions_old']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSinglePiFlatPt_0p7to10_pythia8_cfi/runHitsRelValSinglePiFlatPt0p7to10pythia8cfi_v4/190108_064001/0000/drawTrackPerformance.root')
f['pions']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSinglePiFlatPt_0p7to10_pythia8_cfi/runHitsRelValSinglePiFlatPt0p7to10pythia8cfi_v7/190112_191423/0000/drawTrackPerformance.root')
f['pions_noMTD']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSinglePiFlatPt_0p7to10_pythia8_cfi/runHitsRelValSinglePiFlatPt0p7to10pythia8cfi_v7_noMTD/190113_065654/0000/drawTrackPerformance.root')
f['muons_PU200_old']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10/runHitsRelValSingleMuFlatPt0p7to10_v4/190108_064129/0000/drawTrackPerformance.root')
f['muons_PU200']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10/runHitsRelValSingleMuFlatPt0p7to10_v7/190112_191655/0000/drawTrackPerformance.root')
f['muons_noMTD_PU200']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValSingleMuFlatPt_0p7to10/runHitsRelValSingleMuFlatPt0p7to10_v7_noMTD/190113_065824/0000/drawTrackPerformance.root')
#f['DYtoLL']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValDYToLL_M_50_14TeV/runHitsRelValDYToLLM5014TeV_v5/190111_145926/0000/drawTrackPerformance.root')
#f['DYtoLL_PU200']=R.TFile('/eos/cms/store/user/meridian/MTD/DYToLL_M-50_14TeV_pythia8/runHitsDYToLLM-5014TeVpythia8_v5/190111_150009/0000/drawTrackPerformance.root')
f['DYtoLL']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValDYToLL_M_50_14TeV/runHitsRelValDYToLLM5014TeV_v7/190112_191946/0000/drawTrackPerformance.root')
f['DYtoLL_PU200']=R.TFile('/eos/cms/store/user/meridian/MTD/DYToLL_M-50_14TeV_pythia8/runHitsDYToLLM-5014TeVpythia8_v7/190112_192028/0000/drawTrackPerformance.root')
f['DYtoLL_noMTD']=R.TFile('/eos/cms/store/user/meridian/MTD/RelValDYToLL_M_50_14TeV/runHitsRelValDYToLLM5014TeV_v7_noMTD/190113_070123/0000/drawTrackPerformance.root')
f['DYtoLL_noMTD_PU200']=R.TFile('/eos/cms/store/user/meridian/MTD/DYToLL_M-50_14TeV_pythia8/runHitsDYToLLM-5014TeVpythia8_v7_noMTD/190113_070207/0000/drawTrackPerformance.root')

histos={}
for key, value in f.iteritems():
    histos[key]=Map(value)

labels={}
labels['DYtoLL']='DY#rightarrowLL noPU'
labels['DYtoLL_PU200']='DY#rightarrowLL PU200'
labels['DYtoLL_noMTD']='DY#rightarrowLL noPU'
labels['DYtoLL_noMTD_PU200']='DY#rightarrowLL PU200'
labels['muons']='Single #mu p_{T} 0.7-10 GeV noPU'
labels['muons_old']='Single #mu p_{T} 0.7-10 GeV noPU'
labels['muons_noMTD']='Single #mu p_{T} 0.7-10 GeV noPU'
labels['pions']='Single #pi p_{T} 0.7-10 GeV noPU'
labels['pions_old']='Single #pi p_{T} 0.7-10 GeV noPU'
labels['pions_noMTD']='Single #pi p_{T} 0.7-10 GeV noPU'
labels['muons_PU200']='Single #mu p_{T} 0.7-10 GeV PU200'
labels['muons_PU200_old']='Single #mu p_{T} 0.7-10 GeV PU200'
labels['muons_noMTD_PU200']='Single #mu p_{T} 0.7-10 GeV PU200'

legends={}
legends['DYtoLL']='DY#rightarrowLL noPU'
legends['DYtoLL_PU200']='DY#rightarrowLL PU200'
legends['DYtoLL_noMTD']='DY#rightarrowLL noPU'
legends['DYtoLL_noMTD_PU200']='DY#rightarrowLL PU200'
legends['muons']='Single #mu noPU'
legends['muons_old']='Single #mu noPU mtd3'
legends['muons_noMTD']='Single #mu noPU'
legends['pions']='Single #pi noPU'
legends['pions_old']='Single #pi noPU mtd3'
legends['pions_noMTD']='Single #pi noPU'
legends['muons_PU200']='Single #mu PU200'
legends['muons_PU200_old']='Single #mu PU200 mtd3'
legends['muons_noMTD_PU200']='Single #mu PU200'

if not os.path.exists(args.output):
    print('Creating dir '+args.output)
    os.makedirs(args.output)

#print histos
R.gROOT.SetBatch(True)
c1=R.TCanvas("c1","c1",800,600)
R.gStyle.SetOptStat(0)
R.gStyle.SetOptTitle(0)

titles={}
titles['bestCluster_size']=' cluster size'
titles['bestCluster_energy']=' cluster energy [MeV]'
titles['bestCluster_time']=' cluster time [ns]'
titles['bestCluster_size_vs_eta']=' cluster size'
titles['bestCluster_size_vs_pt']=' cluster size'
titles['bestCluster_energy_vs_eta']=' cluster energy [MeV]'
titles['bestCluster_time_vs_eta']=' cluster time [ns]'
titles['bestCluster_energy_vs_pt']=' cluster energy [MeV]'
titles['bestCluster_time_vs_pt']=' cluster time [ns]'
titles['bestCluster_DR']=' cluster-track #DeltaR'
titles['matchedTrack_nCluster']=' #clusters in #DeltaR=0.05'
titles['mtdTrack_dt']=' track-vertex time [ns]'
titles['mtdTrack_ptRes']='track p_{T}/gen p_{T} -1.'
titles['mtdTrack_dz']='track-vertex z [cm]'
titles['divide_mtdTrack_pt_by_track_pt']='track p_{T} [GeV]'
titles['divide_mtdTrack_eta_by_track_eta']='track #eta'
titles['divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt']='track p_{T} (|#eta|<1.5)'
titles['divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt']='track p_{T} (1.5<|#eta|<3.)'
titles['divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta']='track #eta'
titles['divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta']='track #eta'

ranges={}
ranges['bestCluster_size']=[0,10]
ranges['bestCluster_size_vs_eta']=[0,10]
ranges['bestCluster_size_vs_pt']=[0,10]
ranges['bestCluster_energy']=[0,20]
ranges['bestCluster_energy_vs_eta']=[0,20]
ranges['bestCluster_energy_vs_pt']=[0,20]
ranges['bestCluster_time']=[0,25]
ranges['bestCluster_time_vs_eta']=[0,25]
ranges['bestCluster_time_vs_pt']=[0,25]
ranges['bestCluster_DR']=[0,0.05]
ranges['matchedTrack_nCluster']=[0,20]
ranges['mtdTrack_dt']=[-0.15,0.15]
ranges['mtdTrack_ptRes']=[-0.05,0.05]
ranges['mtdTrack_dz']=[-0.05,0.05]

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size' , 'bestCluster_energy', 'bestCluster_time', 'bestCluster_DR', 'matchedTrack_nCluster' ]:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','muons_noMTD_PU200']):
            histos[t][det+h].GetXaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetLineColor(1+i)
            histos[t][det+h].SetLineWidth(1)
            histos[t][det+h].SetLineStyle(1+i)
            if (histos[t][det+h].GetMaximum()>max):
                max=histos[t][det+h].GetMaximum()
            l.AddEntry(histos[t][det+h],legends[t],"L")
            if (i==0):
                histos[t][det+h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].DrawNormalized()
            else:
                histos[t][det+h].DrawNormalized("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_muPUcomp")

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size' , 'bestCluster_energy', 'bestCluster_time', 'bestCluster_DR', 'matchedTrack_nCluster' ]:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['DYtoLL_noMTD','DYtoLL_noMTD_PU200']):
            histos[t][det+h].GetXaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetLineColor(1+i)
            histos[t][det+h].SetLineWidth(1)
            histos[t][det+h].SetLineStyle(1+i)
            if (histos[t][det+h].GetMaximum()>max):
                max=histos[t][det+h].GetMaximum()
            l.AddEntry(histos[t][det+h],legends[t],"L")
            if (i==0):
                histos[t][det+h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].DrawNormalized()
            else:
                histos[t][det+h].DrawNormalized("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_DYPUcomp")

for h in [ 'mtdTrack_dt', 'mtdTrack_ptRes', 'mtdTrack_dz' ]:
    max=0.
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons','muons_PU200']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetLineWidth(1)
        histos[t][h].SetLineStyle(1+i)
        if (histos[t][h].GetMaximum()>max):
            max=histos[t][h].GetMaximum()
        l.AddEntry(histos[t][h],legends[t],"L")
        if (i==0):
            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].DrawNormalized()
        else:
            histos[t][h].DrawNormalized("SAME")
    l.Draw()
    saveCanvas(c1,h+"_muPUcomp")

for h in [ 'mtdTrack_dt', 'mtdTrack_ptRes', 'mtdTrack_dz' ]:
    max=0.
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['pions','pions_old']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetLineWidth(1)
        histos[t][h].SetLineStyle(1+i)
        if (histos[t][h].GetMaximum()>max):
            max=histos[t][h].GetMaximum()
        l.AddEntry(histos[t][h],legends[t],"L")
        if (i==0):
            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].DrawNormalized()
        else:
            histos[t][h].DrawNormalized("SAME")
    l.Draw()
    saveCanvas(c1,h+"_piOLDcomp")

for h in [ 'mtdTrack_dt', 'mtdTrack_ptRes', 'mtdTrack_dz' ]:
    max=0.
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons','muons_old']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetLineWidth(1)
        histos[t][h].SetLineStyle(1+i)
        if (histos[t][h].GetMaximum()>max):
            max=histos[t][h].GetMaximum()
        l.AddEntry(histos[t][h],legends[t],"L")
        if (i==0):
            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].DrawNormalized()
        else:
            histos[t][h].DrawNormalized("SAME")
    l.Draw()
    saveCanvas(c1,h+"_muOLDcomp")

for h in [ 'mtdTrack_dt', 'mtdTrack_ptRes', 'mtdTrack_dz' ]:
    max=0.
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['DYtoLL','DYtoLL_PU200']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetLineWidth(1)
        histos[t][h].SetLineStyle(1+i)
        if (histos[t][h].GetMaximum()>max):
            max=histos[t][h].GetMaximum()
        l.AddEntry(histos[t][h],legends[t],"L")
        if (i==0):
            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].DrawNormalized()
        else:
            histos[t][h].DrawNormalized("SAME")
    l.Draw()
    saveCanvas(c1,h+"_DYPUcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons','muons_PU200']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_muPUcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons_PU200','muons_PU200_old']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_muPUOLDcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['pions','pions_old']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_piOLDcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['DYtoLL','DYtoLL_PU200']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_DYPUcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['pions','DYtoLL']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_piDYcomp")

for h in [ 'divide_mtdTrack_pt_by_track_pt' , 'divide_mtdTrack_eta_by_track_eta', 'divide_BTLmatchedBestClusterTrack_pt_by_BTLtrack_pt', 'divide_ETLmatchedBestClusterTrack_pt_by_ETLtrack_pt', 'divide_BTLmatchedBestClusterTrack_eta_by_BTLtrack_eta', 'divide_ETLmatchedBestClusterTrack_eta_by_ETLtrack_eta' ]:
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons','pions']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetMarkerColor(1+i)
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetMarkerSize(1.1)
        histos[t][h].SetMarkerStyle(20)
        l.AddEntry(histos[t][h],legends[t],"PL")
        if (i==0):
#            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].Draw("AP")
            histos[t][h].SetMaximum(1.3)
        else:
            histos[t][h].Draw("PSAME")
    l.Draw()
    saveCanvas(c1,h+"_mupicomp")

for h in [ 'mtdTrack_dt', 'mtdTrack_ptRes', 'mtdTrack_dz' ]:
    max=0.
    l=R.TLegend(0.75,0.8,0.96,0.93)
    for i,t in enumerate(['muons','pions']):
        histos[t][h].GetXaxis().SetTitle(titles[h])
        histos[t][h].SetLineColor(1+i)
        histos[t][h].SetLineWidth(1)
        histos[t][h].SetLineStyle(1+i)
        if (histos[t][h].GetMaximum()>max):
            max=histos[t][h].GetMaximum()
        l.AddEntry(histos[t][h],legends[t],"L")
        if (i==0):
            histos[t][h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
            histos[t][h].DrawNormalized()
        else:
            histos[t][h].DrawNormalized("SAME")
    l.Draw()
    saveCanvas(c1,h+"_mupicomp")

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size' , 'bestCluster_energy', 'bestCluster_time', 'bestCluster_DR', 'matchedTrack_nCluster' ]:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','pions_noMTD']):
            histos[t][det+h].GetXaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetLineColor(1+i)
            histos[t][det+h].SetLineWidth(1)
            histos[t][det+h].SetLineStyle(1+i)
            if (histos[t][det+h].GetMaximum()>max):
                max=histos[t][det+h].GetMaximum()
            l.AddEntry(histos[t][det+h],legends[t],"L")
            if (i==0):
                histos[t][det+h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].DrawNormalized()
            else:
                histos[t][det+h].DrawNormalized("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_mupicomp")

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size' , 'bestCluster_energy', 'bestCluster_time', 'bestCluster_DR', 'matchedTrack_nCluster' ]:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['pions_noMTD','DYtoLL_noMTD']):
            histos[t][det+h].GetXaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetLineColor(1+i)
            histos[t][det+h].SetLineWidth(1)
            histos[t][det+h].SetLineStyle(1+i)
            if (histos[t][det+h].GetMaximum()>max):
                max=histos[t][det+h].GetMaximum()
            l.AddEntry(histos[t][det+h],legends[t],"L")
            if (i==0):
                histos[t][det+h].GetXaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].DrawNormalized()
            else:
                histos[t][det+h].DrawNormalized("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_piDYcomp")


for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size_vs_eta' , 'bestCluster_time_vs_eta']:
        p={}
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','muons_noMTD_PU200']):
            histos[t][det+h].GetXaxis().SetTitle("track #eta")
            histos[t][det+h].GetYaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetMarkerColor(1+i)
#            f[t].cd()
            histos[t][det+h].ProfileX()
#            p[t]=f[t].Get(det+h+"_pfx")
#            p[t].SetMarkerColor(1+i)
#            p[t].SetLineColor(1+i)
#            p[t].SetMarkerSize(1.1)
#            p[t].SetMarkerStyle(20)
            if (i==0):
                histos[t][det+h].GetYaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].Draw()
            else:
                histos[t][det+h].Draw("SAME")
            l.AddEntry(histos[t][det+h],legends[t],"PL")
        l.Draw()
        saveCanvas(c1,det+h+"_muPUcomp")


for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size_vs_eta' , 'bestCluster_time_vs_eta']:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','pions_noMTD']):
            histos[t][det+h].GetXaxis().SetTitle("track #eta")
            histos[t][det+h].GetYaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetMarkerColor(1+i)
            l.AddEntry(histos[t][det+h],legends[t],"P")
            if (i==0):
                histos[t][det+h].GetYaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].Draw()
            else:
                histos[t][det+h].Draw("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_mupicomp")

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size_vs_pt' , 'bestCluster_time_vs_pt']:
        p={}
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','muons_noMTD_PU200']):
            histos[t][det+h].GetXaxis().SetTitle("track p_{T}")
            histos[t][det+h].GetYaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetMarkerColor(1+i)
            l.AddEntry(histos[t][det+h],legends[t],"P")
            if (i==0):
                histos[t][det+h].GetYaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].Draw()
            else:
                histos[t][det+h].Draw("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_muPUcomp")

for det in ['BTL','ETL']:
    for h in [ 'bestCluster_size_vs_pt' , 'bestCluster_time_vs_pt']:
        max=0.
        l=R.TLegend(0.75,0.8,0.96,0.93)
        for i,t in enumerate(['muons_noMTD','pions_noMTD']):
            histos[t][det+h].GetXaxis().SetTitle("track p_{T}")
            histos[t][det+h].GetYaxis().SetTitle(det+titles[h])
            histos[t][det+h].SetMarkerColor(1+i)
            l.AddEntry(histos[t][det+h],legends[t],"P")
            if (i==0):
                histos[t][det+h].GetYaxis().SetRangeUser(ranges[h][0],ranges[h][1])
                histos[t][det+h].Draw()
            else:
                histos[t][det+h].Draw("SAME")
        l.Draw()
        saveCanvas(c1,det+h+"_mupicomp")


