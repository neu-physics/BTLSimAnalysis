#ifndef _FTL_DUMP_JETS_
#define _FTL_DUMP_JETS_

#include "PrecisionTiming/FTLAnalysis/interface/FTLJetsTree.h"

#include "TLorentzVector.h"

#include "FWCore/Utilities/interface/BranchType.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Common/interface/Provenance.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/ForwardDetId/interface/FastTimeDetId.h"
#include "DataFormats/FTLRecHit/interface/FTLRecHit.h"
#include "DataFormats/FTLRecHit/interface/FTLRecHitCollections.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "Geometry/Records/interface/FastTimeGeometryRecord.h"
#include "Geometry/HGCalGeometry/interface/FastTimeGeometry.h"

#include "SimDataFormats/Vertex/interface/SimVertex.h"



class FTLDumpJets : public edm::EDAnalyzer
{
public:
  typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> genXYZ;
  
  
  explicit FTLDumpJets(const edm::ParameterSet& pSet);
  ~FTLDumpJets() {};
  
  //---utils
  
  //---methods
  virtual void beginJob() override {};
  virtual void analyze(edm::Event const&, edm::EventSetup const&) override;
  virtual void endJob() override {};
  
  
private:
  //---inputs
  edm::Handle<reco::GenParticleCollection> genParticlesHandle_;
  edm::EDGetTokenT<reco::GenParticleCollection> genParticlesToken_;
  edm::Handle<vector<reco::GenJet> > genJetsHandle_;
  edm::EDGetTokenT<vector<reco::GenJet> > genJetsToken_;
  // edm::EDGetTokenT<genXYZ> genXYZToken_;
  // edm::Handle<genXYZ> genXYZHandle_;
  // edm::EDGetTokenT<float> genT0Token_;    
  // edm::Handle<float> genT0Handle_;
  edm::EDGetTokenT<reco::VertexCollection> vtxsToken_;
  edm::Handle<reco::VertexCollection> vtxsHandle_;
  edm::Handle<FTLRecHitCollection> ftlRecHitsHandle_;
  edm::EDGetTokenT<FTLRecHitCollection> ftlRecHitsToken_;    
  edm::Handle<pat::JetCollection> jetsHandle_;
  edm::EDGetTokenT<pat::JetCollection> jetsToken_;    
  edm::EDGetTokenT<edm::View<pat::PackedCandidate> > tracksToken_;
  edm::Handle<edm::View<pat::PackedCandidate> > tracksHandle_;
  
  //---options
  bool readFTLrecHits_;
  
  //---outputs
  FTLJetsTree outTree_;
  edm::Service<TFileService> fs_;    
};



FTLDumpJets::FTLDumpJets(const edm::ParameterSet& pSet):
  genParticlesToken_(consumes<reco::GenParticleCollection>(pSet.getUntrackedParameter<edm::InputTag>("genParticlesTag"))),
  genJetsToken_(consumes<vector<reco::GenJet> >(pSet.getUntrackedParameter<edm::InputTag>("genJetsTag"))),
  // genXYZToken_(consumes<genXYZ>(pSet.getUntrackedParameter<edm::InputTag>("genXYZTag"))),    
  // genT0Token_(consumes<float>(pSet.getUntrackedParameter<edm::InputTag>("genT0Tag"))),
  vtxsToken_ (consumes<reco::VertexCollection>(pSet.getUntrackedParameter<edm::InputTag>("vtxTag"))),
  ftlRecHitsToken_(consumes<FTLRecHitCollection>(pSet.getUntrackedParameter<edm::InputTag>("ftlRecHitsTag"))),
  jetsToken_(consumes<pat::JetCollection>(pSet.getUntrackedParameter<edm::InputTag>("jetsTag"))),
  tracksToken_(consumes<edm::View<pat::PackedCandidate> >(pSet.getUntrackedParameter<edm::InputTag>("tracksTag"))),
  readFTLrecHits_(pSet.getUntrackedParameter<bool>("readFTLRecHits"))
{
  outTree_ = FTLJetsTree(pSet.getUntrackedParameter<string>("treeName").c_str(), "Jets tree for FTL studies");
}

void FTLDumpJets::analyze(edm::Event const& event, edm::EventSetup const& setup)
{
  outTree_.Reset();
  
  
  //---load gen particles
  event.getByToken(genParticlesToken_, genParticlesHandle_);
  auto genParticles = *genParticlesHandle_.product();
  
  std::vector<reco::GenParticle> leptons;
  for(auto& genPart : genParticles)
  {
    // if(genPart.status() != 1) continue;
    // if(genPart.isPromptFinalState() != 1) continue;
    if( genPart.isHardProcess() != 1 ) continue;
    if(std::abs(genPart.pdgId())!=11 && std::abs(genPart.pdgId())!=13 && std::abs(genPart.pdgId())!=15) continue;
    leptons.push_back(genPart);
    
    outTree_.genLeptons_pt->push_back(genPart.pt());
    outTree_.genLeptons_eta->push_back(genPart.eta());
    outTree_.genLeptons_phi->push_back(genPart.phi());
    outTree_.genLeptons_energy->push_back(genPart.energy());
    outTree_.genLeptons_charge->push_back(genPart.charge());
    outTree_.genLeptons_pdgId->push_back(genPart.pdgId());
    outTree_.genLeptons_vtx_x->push_back(genPart.vx());
    outTree_.genLeptons_vtx_y->push_back(genPart.vy());
    outTree_.genLeptons_vtx_z->push_back(genPart.vz());
    // outTree_.genLeptons_vtx_t->push_back(genPart.vertex());
    
    // std::cout << ">>> genPart:    pdgId: " << genPart.pdgId() << "   pt: " << genPart.pt() << "   eta: " << genPart.eta() << "   phi: " << genPart.phi() << "   mass: " << genPart.mass() << "   isPromptFinalState: " << genPart.isPromptFinalState() << "   isPromptDecayed: " << genPart.isPromptDecayed() << "   isHardProcess: " << genPart.isHardProcess() << "   vertex: " << genPart.vertex() << std::endl;
  }
  // std::cout << std::endl;
  outTree_.genLeptons_n = outTree_.genLeptons_pt->size();
  
  
  //---get truth PV
  // event.getByToken(genXYZToken_, genXYZHandle_);
  // event.getByToken(genT0Token_, genT0Handle_);
  // auto xyz = genXYZHandle_.product();
  // auto t = *genT0Handle_.product();
  // outTree_.genVtx_x = xyz->x();
  // outTree_.genVtx_y = xyz->y();
  // outTree_.genVtx_z = xyz->z();
  // outTree_.genVtx_t = t;
  
  
  //---load genJets
  event.getByToken(genJetsToken_, genJetsHandle_);
  auto genJets = *genJetsHandle_.product();
  // for(auto& genJet : genJets)
  // {
  //   std::cout << ">>> genJet:   pt: " << genJet.pt() << "   eta: " << genJet.eta() << "   phi: " << genJet.phi();
  
  //   bool skipJet = false;
  //   for(auto& lepton : leptons)
  //   {
  //     float DR = deltaR(genJet.eta(),genJet.phi(),lepton.eta(),lepton.phi());
  //     if( DR < 0.4 ) skipJet = true;
  //   }
  //   if( skipJet )
  //   {
  //     std::cout << "   <--- matched to lepton" << std::endl;
  //   }
  //   else
  //   {
  //     std::cout << std::endl;
  //   }
  // }
  // std::cout << std::endl;
  
    
  //--- load vertexes
  event.getByToken(vtxsToken_, vtxsHandle_);
  auto vtxs = *vtxsHandle_.product();
  outTree_.vtxs_n = vtxs.size();
  
  for(auto &vtx : *vtxsHandle_)
  {
    outTree_.vtxs_x -> push_back( vtx.x() );
    outTree_.vtxs_y -> push_back( vtx.y() );
    outTree_.vtxs_z -> push_back( vtx.z() );
    outTree_.vtxs_t -> push_back( vtx.t() );
    outTree_.vtxs_normalizedChi2 -> push_back( vtx.normalizedChi2() );
  }
  
  
  //---load the jets
  event.getByToken(jetsToken_, jetsHandle_);
  auto jets = *jetsHandle_.product();
  
  for(auto& jet : jets)
  {        
    // std::cout << ">>> recoJet:   pt: " << jet.pt() << "   eta: " << jet.eta() << "   phi:  "<< jet.phi() << std::endl;
    
    //---skim
    if( jet.pt() < 30 ) continue;
    
    //---remove jets matched with a hard lepton
    bool skipJet = false;
    for(auto& lepton : leptons)
    {
      float DR = deltaR(jet.eta(),jet.phi(),lepton.eta(),lepton.phi());
      if( DR < 0.4 ) skipJet = true;
    }
    if( skipJet ) continue;
    
    //---jet standard info
    outTree_.jets_pt->push_back(jet.pt());
    outTree_.jets_eta->push_back(jet.eta());
    outTree_.jets_phi->push_back(jet.phi());
    outTree_.jets_energy->push_back(jet.energy());
    
    reco::GenJet* genJetMatched = NULL;
    int nMatch0p6 = 0;
    for(auto& genJet : genJets)
    {
      if( genJet.pt() < 4. ) continue;
      
      float DR = deltaR(jet.eta(),jet.phi(),genJet.eta(),genJet.phi());
      
      if( DR < 0.6 ) ++nMatch0p6;
      
      if( DR < 0.2 )
      {
        genJetMatched = &genJet;
        break;
      }
    }
    
    if( nMatch0p6 == 0 )     outTree_.jets_isPU->push_back(1);
    else if( genJetMatched ) outTree_.jets_isPU->push_back(0);
    else                     outTree_.jets_isPU->push_back(-1);
    
    // std::cout << ">>>>>> selected:   nMatch0p6: " << nMatch0p6 << "   genJetMatched: " << genJetMatched << "   isPU: " << outTree_.isPU->at(outTree_.isPU->size()-1) << std::endl;
    
    if( genJetMatched )
    {
      outTree_.jets_matchedGenJet_pt->push_back(genJetMatched->pt());
      outTree_.jets_matchedGenJet_eta->push_back(genJetMatched->eta());
      outTree_.jets_matchedGenJet_phi->push_back(genJetMatched->phi());
      outTree_.jets_matchedGenJet_energy->push_back(genJetMatched->energy());        
    }
    else
    {
      outTree_.jets_matchedGenJet_pt->push_back(-99.);
      outTree_.jets_matchedGenJet_eta->push_back(-99.);
      outTree_.jets_matchedGenJet_phi->push_back(-99.);
      outTree_.jets_matchedGenJet_energy->push_back(-99.);        
    }
  }
  // std::cout << std::endl;
  outTree_.jets_n = outTree_.jets_pt->size();
  
  
  
  //---load the tracks
  event.getByToken(tracksToken_, tracksHandle_);
  for(unsigned i = 0; i < tracksHandle_->size(); ++i)
  {
    auto ref = tracksHandle_->refAt(i);
    
    //---skip neutrals
    if(ref->charge() == 0)
      continue;
    const reco::Track* track = ref->bestTrack();
    if(track!=nullptr || !track->quality(reco::TrackBase::highPurity))
      continue;
    
    std::cout << "track pt: " << ref->pt() << "   eta: " << ref->eta() << "   time: " << ref->time() << std::endl;
  }
  
  
  //---load the FTL collection if present in the EventContent (avoid crash with standard geometry)
  // auto ftlRecHits = FTLRecHitCollection();
  // if(readFTLrecHits_)
  //     event.getByToken(ftlRecHitsToken_, ftlRecHitsHandle_);
  // if(ftlRecHitsHandle_.isValid())
  //     ftlRecHits = *ftlRecHitsHandle_.product();
  
  
  outTree_.GetTTreePtr()->Fill();
}

DEFINE_FWK_MODULE(FTLDumpJets);

#endif
