#ifndef _FTL_DUMP_HITS_
#define _FTL_DUMP_HITS_

#include "TMath.h"

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

#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/ForwardDetId/interface/BTLDetId.h"
#include "DataFormats/ForwardDetId/interface/ETLDetId.h"
#include "DataFormats/FTLRecHit/interface/FTLRecHit.h"
#include "DataFormats/FTLRecHit/interface/FTLRecHitCollections.h"
#include "DataFormats/FTLRecHit/interface/FTLClusterCollections.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/MeasurementError.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/MeasurementPoint.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "TrackPropagation/SteppingHelixPropagator/interface/SteppingHelixPropagator.h"
#include "TrackingTools/TrajectoryState/interface/TrajectoryStateOnSurface.h"
#include "TrackingTools/TrajectoryState/interface/FreeTrajectoryState.h"
#include "TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h"
#include "TrackingTools/KalmanUpdators/interface/Chi2MeasurementEstimator.h"
#include "DataFormats/GeometrySurface/interface/Plane.h"
#include "DataFormats/GeometrySurface/interface/Cylinder.h"

#include "TrackingTools/PatternTools/interface/Trajectory.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrackingRecHit/interface/TransientTrackingRecHit.h"
#include "RecoMTD/TransientTrackingRecHit/interface/MTDTransientTrackingRecHitBuilder.h"
#include "TrackingTools/Records/interface/TransientRecHitRecord.h"
#include "TrackingTools/PatternTools/interface/TSCBLBuilderWithPropagator.h"
#include "RecoTracker/TransientTrackingRecHit/interface/Traj2TrackHits.h"
#include "TrackingTools/TrackRefitter/interface/TrackTransformer.h"

#include "SimDataFormats/Vertex/interface/SimVertex.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"

#include "Geometry/CommonTopologies/interface/Topology.h"
#include "Geometry/Records/interface/MTDDigiGeometryRecord.h"
#include "Geometry/MTDGeometryBuilder/interface/MTDGeometry.h"
#include "Geometry/MTDGeometryBuilder/interface/MTDGeomDetUnit.h"
#include "Geometry/MTDGeometryBuilder/interface/RectangularMTDTopology.h"
#include "DataFormats/GeometrySurface/interface/BoundSurface.h"
#include "DataFormats/GeometrySurface/interface/MediumProperties.h"
#include "DataFormats/GeometrySurface/interface/TrapezoidalPlaneBounds.h"

#include "RecoMTD/DetLayers/interface/MTDDetLayerGeometry.h"
#include "RecoMTD/DetLayers/interface/MTDTrayBarrelLayer.h"
#include "RecoMTD/DetLayers/interface/MTDDetTray.h"
#include "RecoMTD/DetLayers/interface/MTDRingForwardDoubleLayer.h"
#include "RecoMTD/DetLayers/interface/MTDDetRing.h"
#include "RecoMTD/Records/interface/MTDRecoGeometryRecord.h"

#include "BTLSimAnalysis/RecHitsAnalysis/interface/FTLHitsTree.h"

#include <memory>
using namespace std;



class FTLDumpHits : public edm::EDAnalyzer
{
public:
  explicit FTLDumpHits(const edm::ParameterSet& pSet);
  ~FTLDumpHits() {};
  
  //---utils
  
  //---methods
  virtual void beginJob() override {};
  virtual void analyze(edm::Event const&, edm::EventSetup const&) override;
  virtual void endJob() override {};
  
  std::string PrintPosition(const GlobalPoint& gp);
  std::string PrintPosition(const LocalPoint& lp);
  
private:
  const MTDGeometry* mtdGeometry_;
  
  //---inputs
  edm::Handle<reco::GenParticleCollection> genParticlesHandle_;
  edm::EDGetTokenT<reco::GenParticleCollection> genParticlesToken_;

  edm::Handle<std::vector<PSimHit> > simHitsBTLHandle_;
  edm::EDGetTokenT<std::vector<PSimHit> > simHitsBTLToken_;
  edm::Handle<FTLRecHitCollection> recHitsBTLHandle_;
  edm::EDGetTokenT<FTLRecHitCollection> recHitsBTLToken_;   

	//***************************** uncalibrated *********************************    
  edm::Handle<FTLUncalibratedRecHitCollection> recHitsBTLHandle_uncal_;
  edm::EDGetTokenT<FTLUncalibratedRecHitCollection> recHitsBTLToken_uncal_;   
  //***************************** uncalibrated *********************************    
	
	 
  edm::Handle<FTLClusterCollection> clustersBTLHandle_;
  edm::EDGetTokenT<FTLClusterCollection> clustersBTLToken_;
  
  edm::Handle<std::vector<PSimHit> > simHitsETLHandle_;
  edm::EDGetTokenT<std::vector<PSimHit> > simHitsETLToken_;
  edm::Handle<FTLRecHitCollection> recHitsETLHandle_;
  edm::EDGetTokenT<FTLRecHitCollection> recHitsETLToken_;    
  edm::Handle<FTLClusterCollection> clustersETLHandle_;
  edm::EDGetTokenT<FTLClusterCollection> clustersETLToken_;    

  edm::EDGetTokenT<edm::View<reco::Track> > tracksToken_;
  edm::Handle<edm::View<reco::Track> > tracksHandle_;
  edm::EDGetTokenT<edm::ValueMap<float> > tracksLengthToken_;
  edm::Handle<edm::ValueMap<float> > tracksLengthHandle_;
  edm::EDGetTokenT<edm::ValueMap<float> > tracktmtdToken_;
  edm::Handle<edm::ValueMap<float> > tracktmtdHandle_;
  edm::EDGetTokenT<vector<SimVertex> >                 genVtxToken_;
  edm::Handle<vector<SimVertex> >                      genVtxHandle_;    
  edm::ESHandle<TransientTrackBuilder> builder;

  //---options
  BTLDetId::CrysLayout crysLayout_;
  double track_hit_DRMax_;
  double track_hit_distMax_;
  bool verbosity_;
  bool dumpSimHits_;
  bool dumpRecHits_;

  //---outputs
  FTLHitsTree outTree_;
  edm::Service<TFileService> fs_;  
  
};

FTLDumpHits::FTLDumpHits(const edm::ParameterSet& pSet):
  genParticlesToken_(consumes<reco::GenParticleCollection>(pSet.getUntrackedParameter<edm::InputTag>("genParticlesTag"))),
  simHitsBTLToken_(consumes<std::vector<PSimHit> >(pSet.getUntrackedParameter<edm::InputTag>("simHitsBTLTag"))),
  recHitsBTLToken_(consumes<FTLRecHitCollection>(pSet.getUntrackedParameter<edm::InputTag>("recHitsBTLTag"))),
  recHitsBTLToken_uncal_(consumes<FTLUncalibratedRecHitCollection>(pSet.getUntrackedParameter<edm::InputTag>("uncal_recHitsBTLTag"))),  
  clustersBTLToken_(consumes<FTLClusterCollection>(pSet.getUntrackedParameter<edm::InputTag>("clustersBTLTag"))),
  simHitsETLToken_(consumes<std::vector<PSimHit> >(pSet.getUntrackedParameter<edm::InputTag>("simHitsETLTag"))),
  recHitsETLToken_(consumes<FTLRecHitCollection>(pSet.getUntrackedParameter<edm::InputTag>("recHitsETLTag"))),
  clustersETLToken_(consumes<FTLClusterCollection>(pSet.getUntrackedParameter<edm::InputTag>("clustersETLTag"))),
  tracksToken_(consumes<edm::View<reco::Track> >(pSet.getUntrackedParameter<edm::InputTag>("tracksTag"))),
  tracksLengthToken_(consumes<edm::ValueMap<float> >(pSet.getUntrackedParameter<edm::InputTag>("tracksLengthTag"))),
  tracktmtdToken_(consumes<edm::ValueMap<float> >(pSet.getUntrackedParameter<edm::InputTag>("trackstmtdTag"))),
  genVtxToken_(consumes<vector<SimVertex> >(pSet.getUntrackedParameter<edm::InputTag>("genVtxTag"))),
  crysLayout_((BTLDetId::CrysLayout)(pSet.getUntrackedParameter<int>("crysLayout"))),
  track_hit_DRMax_(pSet.getParameter<double>("track_hit_DRMax")),
  track_hit_distMax_(pSet.getParameter<double>("track_hit_distMax")),
  verbosity_(pSet.getParameter<bool>("verbosity")),
  dumpSimHits_(pSet.getParameter<bool>("dumpSimHits")),
  dumpRecHits_(pSet.getParameter<bool>("dumpRecHits"))
{
  outTree_ = FTLHitsTree(pSet.getUntrackedParameter<string>("treeName").c_str(), "FTLHits tree for FTL studies");
}



void FTLDumpHits::analyze(edm::Event const& event, edm::EventSetup const& setup)
{
  outTree_.Reset();

  //---get the MTD geometry
  edm::ESHandle<MTDGeometry> geoHandle;
  setup.get<MTDDigiGeometryRecord>().get(geoHandle);
  mtdGeometry_ = geoHandle.product();
  
  edm::ESHandle<MTDDetLayerGeometry> layerGeo;
  setup.get<MTDRecoGeometryRecord>().get(layerGeo);
  
  //--- get the B field
  edm::ESHandle<MagneticField> theField;
  setup.get<IdealMagneticFieldRecord>().get(theField);
  PropagationDirection dir(alongMomentum);
  SteppingHelixPropagator* propagator = new SteppingHelixPropagator(theField.product(),dir);
  propagator -> setMaterialMode(false);
  propagator -> setNoErrorPropagation(false);
  setup.get<TransientTrackRecord>().get("TransientTrackBuilder", builder);

  //--- load gen particles
  event.getByToken(genParticlesToken_, genParticlesHandle_);
  auto genParticles = *genParticlesHandle_.product();
  
  //---load sim hits
  event.getByToken(simHitsBTLToken_, simHitsBTLHandle_);
  auto simHitsBTL = *simHitsBTLHandle_.product();
  
  //---load the FTL collection if present in the EventContent (avoid crash with standard geometry)
  event.getByToken(recHitsBTLToken_, recHitsBTLHandle_);
  auto recHitsBTL = FTLRecHitCollection();
  if(recHitsBTLHandle_.isValid())
    recHitsBTL = *recHitsBTLHandle_.product();
  //***************************** uncalibrated *********************************    
  event.getByToken(recHitsBTLToken_uncal_, recHitsBTLHandle_uncal_);
  auto recHitsBTL_uncal = FTLUncalibratedRecHitCollection();
  if(recHitsBTLHandle_uncal_.isValid())
    recHitsBTL_uncal = *recHitsBTLHandle_uncal_.product();
  //***************************** uncalibrated *********************************    


  event.getByToken(clustersBTLToken_, clustersBTLHandle_);

   //auto clusters = FTLClusterCollection();
   //if(clustersBTLHandle_.isValid())
  auto clustersBTL = *clustersBTLHandle_.product();

  //---load sim hits
  event.getByToken(simHitsETLToken_, simHitsETLHandle_);
  auto simHitsETL = *simHitsETLHandle_.product();

  //---load the FTL collection if present in the EventContent (avoid crash with standard geometry)
  event.getByToken(recHitsETLToken_, recHitsETLHandle_);
  auto recHitsETL = FTLRecHitCollection();
  if(recHitsETLHandle_.isValid())
    recHitsETL = *recHitsETLHandle_.product();
  event.getByToken(clustersETLToken_, clustersETLHandle_);
   //auto clusters = FTLClusterCollection();
   //if(clustersETLHandle_.isValid())
  auto clustersETL = *clustersETLHandle_.product();

  //---load tracks
  event.getByToken(tracksToken_,tracksHandle_);
  auto tracks = *tracksHandle_.product();
  event.getByToken(tracksLengthToken_,tracksLengthHandle_);
  event.getByToken(tracktmtdToken_,tracktmtdHandle_);
  
  event.getByToken(genVtxToken_, genVtxHandle_);    
  const SimVertex* genPV = NULL;

  //if(genVtxHandle_.isValid())   // comment out BBT 02-06-19: was causing nuGun200PU sample to crash
  if(genVtxHandle_.product()->size()>0)
    genPV = &(genVtxHandle_.product()->at(0));
  
  for(auto& genParts : genParticles)
  {
    float eta = genParts.eta();
    float phi = genParts.phi();
    outTree_.GenPart_eta->push_back(eta);
    outTree_.GenPart_phi->push_back(phi);
  }



  //---fill the tree - simHits
  outTree_.simHits_n = 0;
  //if (dumpSimHits_)
  {
    std::cout << "simHits size: " << simHitsBTL.size() << std::endl;
    for(auto simHit : simHitsBTL)
    {
      BTLDetId id = simHit.detUnitId();
      DetId geoId = id.geographicalId( crysLayout_);
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());
      
      double energy = simHit.energyLoss()*1000.;
      double time   = simHit.tof();
      
      if ((time)<0 || (time)>25) continue;
      
      int RR = id.mtdRR();
      int module = id.module();
      int modType = id.modType();
      int crystal = id.crystal();
      int ieta = id.ieta(crysLayout_);
      int iphi = id.iphi(crysLayout_);
      
      LocalPoint lp_entry(simHit.entryPoint().x()/10., simHit.entryPoint().y()/10., simHit.entryPoint().z()/10.);
      //LocalPoint lp_mid  (simHit.localPosition().x()/10.,simHit.localPosition().y()/10.,simHit.localPosition().z()/10.);
      LocalPoint lp_exit ( simHit.exitPoint().x()/10.,  simHit.exitPoint().y()/10.,  simHit.exitPoint().z()/10.);
      GlobalPoint gp_entry = det->toGlobal(topo.pixelToModuleLocalPoint(lp_entry,id.row(topo.nrows()),id.column(topo.nrows())));
      GlobalPoint gp_exit  = det->toGlobal(topo.pixelToModuleLocalPoint(lp_exit,id.row(topo.nrows()),id.column(topo.nrows())));
      //GlobalPoint gp_mid   = det->toGlobal(topo.pixelToModuleLocalPoint(lp_mid,id.row(topo.nrows()),id.column(topo.nrows())));    
      
      float eta = gp_entry.eta();
      float phi = gp_entry.phi();
      
      outTree_.simHits_n += 1;
      
      outTree_.simHits_det->push_back(1);
      outTree_.simHits_energy->push_back(energy);
      outTree_.simHits_time->push_back(time);
      outTree_.simHits_rr->push_back(RR);
      outTree_.simHits_module->push_back(module);
      outTree_.simHits_modType->push_back(modType);
      outTree_.simHits_crystal->push_back(crystal);
      outTree_.simHits_ieta->push_back(ieta);
      outTree_.simHits_iphi->push_back(iphi);
      outTree_.simHits_eta->push_back(eta);
      outTree_.simHits_phi->push_back(phi);
      outTree_.simHits_entry_local_x->push_back(lp_entry.x());
      outTree_.simHits_entry_local_y->push_back(lp_entry.y());
      outTree_.simHits_entry_local_z->push_back(lp_entry.z());
      outTree_.simHits_entry_global_R->push_back(sqrt(gp_entry.perp2()));
      outTree_.simHits_exit_local_x->push_back(lp_exit.x());
      outTree_.simHits_exit_local_y->push_back(lp_exit.y());
      outTree_.simHits_exit_local_z->push_back(lp_exit.z());
      outTree_.simHits_exit_global_R->push_back(sqrt(gp_exit.perp2()));
    }
  }  
  
  
  //---fill the tree - BTL recHits
  outTree_.recHits_n = 0;
  if (dumpRecHits_)
  {
    for(auto recHit : recHitsBTL)
    {
      BTLDetId id = recHit.id();
      DetId geoId = id.geographicalId( crysLayout_);
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
      
      double energy = recHit.energy();
      double time   = recHit.time();
      double timeError = recHit.timeError();
      float dis_left = recHit.position().first;
      float dis_right = recHit.position().second;
      
      MeasurementPoint mp(recHit.row(),recHit.column());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      int RR = id.mtdRR();
      int side = id.mtdSide();
      int module = id.module();
      int modType = id.modType();
      int crystal = id.crystal();
      int ieta = id.ieta(crysLayout_);
      int iphi = id.iphi(crysLayout_);
      float eta = gp.eta();
      float phi = gp.phi();
      /************************* matching uncalibrated recHits with recHits ***********************/
      /*
      bool match_success = false;
      for(auto recHit_uncal_ : recHitsBTL_uncal)
      {
        if((recHit.row()==recHit_uncal_.row())&&(recHit.column()==recHit_uncal_.column()))
        {
          BTLDetId id_uncal = recHit_uncal_.id();
          DetId geoId_uncal = id_uncal.geographicalId( crysLayout_);
          const auto& det_uncal = mtdGeometry_ -> idToDet(geoId_uncal);
          const ProxyMTDTopology& topoproxy_uncal = static_cast<const ProxyMTDTopology&>(det_uncal->topology());
          const RectangularMTDTopology& topo_uncal = static_cast<const RectangularMTDTopology&>(topoproxy_uncal.specificTopology());
          std::pair<float,float> time_pair = recHit_uncal_.time();
          float time1 = time_pair.first;
          float time2 = time_pair.second;
          outTree_.recHits_time1_uncalibrated->push_back(time1);
          outTree_.recHits_time2_uncalibrated->push_back(time2);
          
          MeasurementPoint mp_uncal(recHit_uncal_.row(),recHit_uncal_.column());
          LocalPoint lp_uncal = topo_uncal.localPosition(mp_uncal);
          GlobalPoint gp_uncal = det_uncal->toGlobal(lp_uncal);
          float eta_uncal = gp_uncal.eta();
          float phi_uncal = gp_uncal.phi();
          outTree_.recHits_eta_uncalibrated->push_back(eta_uncal);
          outTree_.recHits_phi_uncalibrated->push_back(phi_uncal);
          outTree_.recHits_matched_with_uncalibrated->push_back(1.0);
          match_success = true;
          break;
        }
      }
      
      if(!match_success)
      {
        //std::cout << "nothing matched" << std::endl;
        outTree_.recHits_matched_with_uncalibrated->push_back(0.0);
      }
      match_success = false;*/
      //std::cout << "local y: " << lp.y() << "	col:" << recHit.column() << std::endl;
      
      outTree_.recHits_n += 1;
        
      outTree_.recHits_det->push_back(1);
      outTree_.recHits_energy->push_back(energy);
      outTree_.recHits_time->push_back(time);
      outTree_.recHits_timeError->push_back(timeError);
      outTree_.recHits_dis_left->push_back(dis_left);
      outTree_.recHits_dis_right->push_back(dis_right);
      outTree_.recHits_rr->push_back(RR);
      outTree_.recHits_side->push_back(side);
      outTree_.recHits_module->push_back(module);
      outTree_.recHits_modType->push_back(modType);
      outTree_.recHits_crystal->push_back(crystal);
      outTree_.recHits_ieta->push_back(ieta);
      outTree_.recHits_iphi->push_back(iphi);
      outTree_.recHits_eta->push_back(eta);
      outTree_.recHits_phi->push_back(phi);
      outTree_.recHits_local_x->push_back(lp.x());
      outTree_.recHits_local_y->push_back(lp.y());
      outTree_.recHits_local_z->push_back(lp.z());
      outTree_.recHits_global_R->push_back(sqrt(gp.perp2()));
    }
/****************************** looping over uncalibrated recHits *********************/
    for(auto recHit_uncal : recHitsBTL_uncal)
    {
      BTLDetId id = recHit_uncal.id();
      DetId geoId = id.geographicalId( crysLayout_);
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
      
      //double energy = recHit_uncal.energy();
      //double time   = recHit_uncal.time();
      
      std::pair<float,float> time_pair = recHit_uncal.time();
      float time1 = time_pair.first;
      float time2 = time_pair.second;
      
      std::pair<float,float> position_pair = recHit_uncal.position();
      float position_left = position_pair.first;
      float position_right = position_pair.second;
      
      outTree_.recHits_uncal_time1->push_back(time1);
      outTree_.recHits_uncal_time2->push_back(time2);
      outTree_.recHits_uncal_position_left->push_back(position_left);
      outTree_.recHits_uncal_position_right->push_back(position_right);
      MeasurementPoint mp(recHit_uncal.row(),recHit_uncal.column());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      float eta = gp.eta();
      float phi = gp.phi();
      float x = gp.x();
      float y = gp.y();
      float z = gp.z();
      outTree_.recHits_uncal_eta->push_back(eta);
      outTree_.recHits_uncal_phi->push_back(phi);
      outTree_.recHits_uncal_x->push_back(x);
      outTree_.recHits_uncal_y->push_back(y);
      outTree_.recHits_uncal_z->push_back(z);
      
      
      //outTree_.recHits_uncal_n += 1  
    }
  }



    

  //---fill the tree - BTL clusters
  outTree_.clusters_n = 0;
  
  for (auto clusIt : clustersBTL)
  {    
    DetId id = clusIt.detId();
    const auto& det = mtdGeometry_ -> idToDet(id);
    const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
    const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
    for ( auto cluster : clusIt)
    {
      float energy = cluster.energy();
      float time   = cluster.time();
      float x=cluster.x();
      float y=cluster.y();
    
      int size=cluster.size();
      int sizeX=cluster.sizeX();
      int sizeY=cluster.sizeY();
      float seed_energy=cluster.seed().energy();
      float seed_time=cluster.seed().time();
      int seed_x=cluster.seed().x();
      int seed_y=cluster.seed().y();
      
      MeasurementPoint mp(cluster.x(),cluster.y());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      MTDDetId mtdId(id);
      int RR = 0;
      int module = 0;
      int modType = 0;
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
      float eta = 0;
      float phi = 0;
    
      if ( mtdId.mtdSubDetector() == MTDDetId::BTL )
      {
        BTLDetId btlId(id);
        RR = btlId.mtdRR();
        module = btlId.module();
        modType = btlId.modType();
        crystal = btlId.crystal();
        ieta = btlId.ieta(crysLayout_);
        iphi = btlId.iphi(crysLayout_);
        eta = gp.eta();
        phi = gp.phi();
      }
    
      outTree_.clusters_n += 1;    
      outTree_.clusters_det->push_back(1);
      outTree_.clusters_size->push_back(size);
      outTree_.clusters_size_x->push_back(sizeX);
      outTree_.clusters_size_y->push_back(sizeY);
      outTree_.clusters_energy->push_back(energy);
      outTree_.clusters_time->push_back(time);
      outTree_.clusters_rr->push_back(RR);
      outTree_.clusters_module->push_back(module);
      outTree_.clusters_modType->push_back(modType);
      outTree_.clusters_crystal->push_back(crystal);
      outTree_.clusters_ieta->push_back(ieta);
      outTree_.clusters_iphi->push_back(iphi);
      outTree_.clusters_eta->push_back(eta);
      outTree_.clusters_phi->push_back(phi);
      outTree_.clusters_x->push_back(x);
      outTree_.clusters_y->push_back(y);
      outTree_.clusters_seed_energy->push_back(seed_energy);
      outTree_.clusters_seed_time->push_back(seed_time);
      outTree_.clusters_seed_x->push_back(seed_x);
      outTree_.clusters_seed_y->push_back(seed_y);
      outTree_.clusters_local_x->push_back(lp.x());
      outTree_.clusters_local_y->push_back(lp.y());
      outTree_.clusters_local_z->push_back(lp.z());
      outTree_.clusters_global_R->push_back(sqrt(gp.perp2()));
    }
  }

  if (dumpSimHits_)
  {
    for(auto simHit : simHitsETL)
    {
      ETLDetId id = simHit.detUnitId();
      DetId geoId = id.geographicalId();
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());
      
      double energy = simHit.energyLoss()*1000.;
      double time   = simHit.tof();
    
      if ((time)<0 || (time)>25) continue;
    
      int RR = id.mtdRR();
      int module = id.module();
      int modType = id.modType();
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
    
      //need to add protection of oot
      // ETL is already in module-local coordinates so just scale to cm from mm
      Local3DPoint simscaled(0.1*simHit.entryPoint().x(),0.1*simHit.entryPoint().y(),0.1*simHit.entryPoint().z());
      const auto& thepixel = topo.pixel(simscaled); // mm -> cm here is the switch                               
      const uint8_t row(thepixel.first), col(thepixel.second);
    
      LocalPoint lp_entry(simHit.entryPoint().x()/10., simHit.entryPoint().y()/10., simHit.entryPoint().z()/10.);
      LocalPoint lp_exit ( simHit.exitPoint().x()/10.,  simHit.exitPoint().y()/10.,  simHit.exitPoint().z()/10.);
      GlobalPoint gp_entry = det->toGlobal(topo.pixelToModuleLocalPoint(lp_entry,row,col));
      GlobalPoint gp_exit  = det->toGlobal(topo.pixelToModuleLocalPoint(lp_exit,row,col));
      
      outTree_.simHits_n += 1;
      
      outTree_.simHits_det->push_back(2);
      outTree_.simHits_energy->push_back(energy);
      outTree_.simHits_time->push_back(time);
      outTree_.simHits_rr->push_back(RR);
      outTree_.simHits_module->push_back(module);
      outTree_.simHits_modType->push_back(modType);
      outTree_.simHits_crystal->push_back(crystal);
      outTree_.simHits_ieta->push_back(ieta);
      outTree_.simHits_iphi->push_back(iphi);
      outTree_.simHits_entry_local_x->push_back(lp_entry.x());
      outTree_.simHits_entry_local_y->push_back(lp_entry.y());
      outTree_.simHits_entry_local_z->push_back(lp_entry.z());
      outTree_.simHits_entry_global_R->push_back(sqrt(gp_entry.perp2()));
      outTree_.simHits_exit_local_x->push_back(lp_exit.x());
      outTree_.simHits_exit_local_y->push_back(lp_exit.y());
      outTree_.simHits_exit_local_z->push_back(lp_exit.z());
      outTree_.simHits_exit_global_R->push_back(sqrt(gp_exit.perp2()));
    }
  }  
  
  if (dumpRecHits_)
  {
    //---fill the tree - ETL recHits
    for(auto recHit : recHitsETL)
    {
      ETLDetId id = recHit.id();
      DetId geoId = id.geographicalId( );
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
      
      double energy = recHit.energy();
      double time   = recHit.time();
      
      MeasurementPoint mp(recHit.row(),recHit.column());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      int RR = id.mtdRR();
      int side = id.mtdSide();
      int module = id.module();
      int modType = id.modType();
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
      //int ieta = id.ieta();
      //int iphi = id.iphi();
      float eta = gp.eta();
      float phi = gp.phi();
    
      outTree_.recHits_n += 1;
      outTree_.recHits_det->push_back(2);
      outTree_.recHits_energy->push_back(energy);
      outTree_.recHits_time->push_back(time);
      outTree_.recHits_rr->push_back(RR);
      outTree_.recHits_side->push_back(side);
      outTree_.recHits_module->push_back(module);
      outTree_.recHits_modType->push_back(modType);
      outTree_.recHits_crystal->push_back(crystal);
      outTree_.recHits_ieta->push_back(ieta);
      outTree_.recHits_iphi->push_back(iphi);
      outTree_.recHits_eta->push_back(eta);
      outTree_.recHits_phi->push_back(phi);
      outTree_.recHits_local_x->push_back(lp.x());
      outTree_.recHits_local_y->push_back(lp.y());
      outTree_.recHits_local_z->push_back(lp.z());
      outTree_.recHits_global_R->push_back(sqrt(gp.perp2()));
    }
  }

  //---fill the tree - ETL cluters  
  for (auto clusIt : clustersETL)
  {    
    DetId id = clusIt.detId();
    const auto& det = mtdGeometry_ -> idToDet(id);
    const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
    const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
    for ( auto cluster : clusIt)
    {
      float energy = cluster.energy();
      float time   = cluster.time();
      float x=cluster.x();
      float y=cluster.y();
    
      int size=cluster.size();
      int sizeX=cluster.sizeX();
      int sizeY=cluster.sizeY();
      float seed_energy=cluster.seed().energy();
      float seed_time=cluster.seed().time();
      int seed_x=cluster.seed().x();
      int seed_y=cluster.seed().y();
      
      MeasurementPoint mp(cluster.x(),cluster.y());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      MTDDetId mtdId(id);
      int RR = 0;
      int module = 0;
      int modType = 0;
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
      float eta = 0;
      float phi = 0;
      
      if ( mtdId.mtdSubDetector() == MTDDetId::ETL )
      {
        ETLDetId etlId(id);
        RR = etlId.mtdRR();
        module = etlId.module();
        modType = etlId.modType();
        // crystal = btlId.crystal();
        //ieta = etlId.ieta();
        //iphi = etlId.iphi();
        eta = gp.eta();
        phi = gp.phi();
      }

      outTree_.clusters_n += 1;    
      outTree_.clusters_det->push_back(2);
      outTree_.clusters_size->push_back(size);
      outTree_.clusters_size_x->push_back(sizeX);
      outTree_.clusters_size_y->push_back(sizeY);
      outTree_.clusters_energy->push_back(energy);
      outTree_.clusters_time->push_back(time);
      outTree_.clusters_rr->push_back(RR);
      outTree_.clusters_module->push_back(module);
      outTree_.clusters_modType->push_back(modType);
      outTree_.clusters_crystal->push_back(crystal);
      outTree_.clusters_ieta->push_back(ieta);
      outTree_.clusters_iphi->push_back(iphi);
      outTree_.clusters_eta->push_back(eta);
      outTree_.clusters_phi->push_back(phi);
      outTree_.clusters_x->push_back(x);
      outTree_.clusters_y->push_back(y);
      outTree_.clusters_seed_energy->push_back(seed_energy);
      outTree_.clusters_seed_time->push_back(seed_time);
      outTree_.clusters_seed_x->push_back(seed_x);
      outTree_.clusters_seed_y->push_back(seed_y);
      outTree_.clusters_local_x->push_back(lp.x());
      outTree_.clusters_local_y->push_back(lp.y());
      outTree_.clusters_local_z->push_back(lp.z());
      outTree_.clusters_global_R->push_back(sqrt(gp.perp2()));
    }
  }

  //--- fill the tree - tracks
  int idx=0;
  for(unsigned iTrack = 0; iTrack < tracks.size(); ++iTrack)
  {
    auto track = tracks.at(iTrack);
    // skip neutrals
    if( track.charge() == 0 ) continue;
    //    if( fabs(track.eta()) > 1.5 ) continue;
    if( track.pt() < 0.7 ) continue;
    edm::Ptr< reco::Track > ptr( tracksHandle_, iTrack);
    double trackLength = (*tracksLengthHandle_)[ptr];
    double tracktmtd = (*tracktmtdHandle_)[ptr];

    // match with gen particles
    float DRMin = 999999;
    int genPdgId = 0;
    float genEta = -999.;
    float genPhi = -999.;
    float genPt = -999.;
    for(auto& genPart : genParticles)
	  {
	    if( genPart.status() != 1 ) continue;
	    if( genPart.charge() == 0 ) continue;
        
	    float Deta = track.eta()-genPart.eta();
	    float Dphi = deltaPhi(track.phi(),genPart.phi());
	    float DR   = sqrt(Deta*Deta+Dphi*Dphi);
        
	    if( DR < DRMin )
	    {
	      DRMin = DR;
	      genPdgId = genPart.pdgId();
	      genEta   = genPart.eta();
	      genPhi   = genPart.phi();
	      genPt    = genPart.pt();
	    }
	  }
    
    if (genPV)
    {
      outTree_.track_mcMatch_genVtx_x -> push_back(genPV->position().x());
      outTree_.track_mcMatch_genVtx_y -> push_back(genPV->position().y());
      outTree_.track_mcMatch_genVtx_z -> push_back(genPV->position().z());
      outTree_.track_mcMatch_genVtx_t -> push_back(genPV->position().t()*1E9); //ns
    }
    else
    {
      outTree_.track_mcMatch_genVtx_x -> push_back(-999.);
      outTree_.track_mcMatch_genVtx_y -> push_back(-999.);
      outTree_.track_mcMatch_genVtx_z -> push_back(-999.);
      outTree_.track_mcMatch_genVtx_t -> push_back(-999.);
    }
    
    std::cout << "Track velocity: " << track.beta() << std:: endl;
    outTree_.track_idx -> push_back(idx);
    outTree_.track_pt -> push_back(track.pt());
    outTree_.track_eta -> push_back(track.eta());
    outTree_.track_phi -> push_back(track.phi());
    outTree_.track_x -> push_back(track.vx());
    outTree_.track_y -> push_back(track.vy());
    outTree_.track_z -> push_back(track.vz());
    outTree_.track_t -> push_back(track.t0());
    outTree_.track_length -> push_back(trackLength);
    outTree_.track_velocity -> push_back(track.beta());
    outTree_.track_tmtd -> push_back(tracktmtd);
    outTree_.track_energy -> push_back(sqrt(track.momentum().mag2()));
    outTree_.track_normalizedChi2 -> push_back(track.normalizedChi2());
    outTree_.track_numberOfValidHits -> push_back(track.numberOfValidHits());
    outTree_.track_numberOfLostHits -> push_back(track.numberOfLostHits());
    outTree_.track_isHighPurity -> push_back(track.quality(reco::TrackBase::TrackQuality::highPurity));
    outTree_.track_hasMTD -> push_back(track.isTimeOk());
    outTree_.track_mcMatch_genPdgId -> push_back(genPdgId);
    outTree_.track_mcMatch_genPt -> push_back(genPt);
    outTree_.track_mcMatch_genEta -> push_back(genEta);
    outTree_.track_mcMatch_genPhi -> push_back(genPhi);
    outTree_.track_mcMatch_DR -> push_back(DRMin);
      
    if( verbosity_ ) std::cout << "*** track " << iTrack << " / " << tracks.size() << "   pt: " << track.pt() << "   eta: " << track.eta() << "   phi: " << track.phi() << std::endl;
    if( verbosity_ ) std::cout << "*** match with gen particle   DR: " << DRMin << "   gen pdgId: " << genPdgId << "   gen eta: " << genEta << "   gen phi: " << genPhi << "   genPt: " << genPt << std::endl;
    if( verbosity_ ) std::cout << "---" << std::endl;

    outTree_.matchedSimHits_n->resize(idx+1);
    outTree_.matchedRecHits_n->resize(idx+1);
    outTree_.matchedClusters_n->resize(idx+1);

    if (dumpSimHits_)
    {
      outTree_.matchedSimHits_idx->resize(idx+1);
      outTree_.matchedSimHits_det->resize(idx+1);
      outTree_.matchedSimHits_energy->resize(idx+1);
      outTree_.matchedSimHits_energyCorr->resize(idx+1);
      outTree_.matchedSimHits_time->resize(idx+1);
      outTree_.matchedSimHits_rr->resize(idx+1);
      outTree_.matchedSimHits_module->resize(idx+1);
      outTree_.matchedSimHits_modType->resize(idx+1);
      outTree_.matchedSimHits_crystal->resize(idx+1);
      outTree_.matchedSimHits_ieta->resize(idx+1);
      outTree_.matchedSimHits_iphi->resize(idx+1);
      outTree_.matchedSimHits_entry_local_x->resize(idx+1);
      outTree_.matchedSimHits_entry_local_y->resize(idx+1);
      outTree_.matchedSimHits_entry_local_z->resize(idx+1);
      outTree_.matchedSimHits_entry_global_R->resize(idx+1);
      outTree_.matchedSimHits_exit_local_x->resize(idx+1);
      outTree_.matchedSimHits_exit_local_y->resize(idx+1);
      outTree_.matchedSimHits_exit_local_z->resize(idx+1);
      outTree_.matchedSimHits_exit_global_R->resize(idx+1);
      outTree_.matchedSimHits_track_Deta->resize(idx+1);
      outTree_.matchedSimHits_track_Dphi->resize(idx+1);
      outTree_.matchedSimHits_track_DR->resize(idx+1);
      outTree_.matchedSimHits_track_Dz->resize(idx+1);
      outTree_.matchedSimHits_track_RDphi->resize(idx+1);
      outTree_.matchedSimHits_track_dist->resize(idx+1);
    }
    
    if (dumpRecHits_)
    {
      outTree_.matchedRecHits_idx->resize(idx+1);
      outTree_.matchedRecHits_det->resize(idx+1);
      outTree_.matchedRecHits_energy->resize(idx+1);
      outTree_.matchedRecHits_energyCorr->resize(idx+1);
      outTree_.matchedRecHits_time->resize(idx+1);
      outTree_.matchedRecHits_rr->resize(idx+1);
      outTree_.matchedRecHits_module->resize(idx+1);
      outTree_.matchedRecHits_modType->resize(idx+1);
      outTree_.matchedRecHits_crystal->resize(idx+1);
      outTree_.matchedRecHits_ieta->resize(idx+1);
      outTree_.matchedRecHits_iphi->resize(idx+1);
      outTree_.matchedRecHits_local_x->resize(idx+1);
      outTree_.matchedRecHits_local_y->resize(idx+1);
      outTree_.matchedRecHits_local_z->resize(idx+1);
      outTree_.matchedRecHits_global_R->resize(idx+1);
      outTree_.matchedRecHits_track_Deta->resize(idx+1);
      outTree_.matchedRecHits_track_Dphi->resize(idx+1);
      outTree_.matchedRecHits_track_DR->resize(idx+1);
      outTree_.matchedRecHits_track_Dz->resize(idx+1);
      outTree_.matchedRecHits_track_RDphi->resize(idx+1);
      outTree_.matchedRecHits_track_dist->resize(idx+1);
      outTree_.matchedRecHits_sietaieta->resize(idx+1);
      outTree_.matchedRecHits_siphiiphi->resize(idx+1);
    }

    outTree_.matchedClusters_idx->resize(idx+1);
    outTree_.matchedClusters_det->resize(idx+1);
    outTree_.matchedClusters_energy->resize(idx+1);
    outTree_.matchedClusters_energyCorr->resize(idx+1);
    outTree_.matchedClusters_time->resize(idx+1);
    outTree_.matchedClusters_rr->resize(idx+1);
    outTree_.matchedClusters_module->resize(idx+1);
    outTree_.matchedClusters_modType->resize(idx+1);
    outTree_.matchedClusters_crystal->resize(idx+1);
    outTree_.matchedClusters_ieta->resize(idx+1);
    outTree_.matchedClusters_iphi->resize(idx+1);
    outTree_.matchedClusters_size->resize(idx+1);
    outTree_.matchedClusters_size_x->resize(idx+1);
    outTree_.matchedClusters_size_y->resize(idx+1);
    outTree_.matchedClusters_local_x->resize(idx+1);
    outTree_.matchedClusters_local_y->resize(idx+1);
    outTree_.matchedClusters_local_z->resize(idx+1);
    outTree_.matchedClusters_global_R->resize(idx+1);
    outTree_.matchedClusters_track_Deta->resize(idx+1);
    outTree_.matchedClusters_track_Dphi->resize(idx+1);
    outTree_.matchedClusters_track_DR->resize(idx+1);
    outTree_.matchedClusters_track_Dz->resize(idx+1);
    outTree_.matchedClusters_track_RDphi->resize(idx+1);
    outTree_.matchedClusters_track_dist->resize(idx+1);
      
    //---get compatible layers/Dets
    std::vector<GlobalPoint> gp_ext;
    auto tTrack = builder->build(track);
    TrajectoryStateOnSurface tsos = tTrack.outermostMeasurementState();
    float theMaxChi2 = 25.;
    float theNSigma = 5.;
    std::unique_ptr<MeasurementEstimator> theEstimator = std::make_unique<Chi2MeasurementEstimator>(theMaxChi2,theNSigma);
    SteppingHelixPropagator prop(theField.product(),anyDirection);

    //try BTL
    bool inBTL=false;
    const vector<const DetLayer*>& layersBTL = layerGeo->allBTLLayers();
    for (const DetLayer* ilay : layersBTL) 
    {
      pair<bool, TrajectoryStateOnSurface> comp = ilay->compatible(tsos,prop,*theEstimator);	
      if (!comp.first) continue;
      vector<DetLayer::DetWithState> compDets = ilay->compatibleDets(tsos,prop,*theEstimator);
      for( const auto& detWithState : compDets ) 
      {
        gp_ext.push_back(detWithState.second.globalPosition());
        if (!inBTL)
        {
          outTree_.track_eta_atBTL -> push_back(gp_ext.back().eta());
          outTree_.track_phi_atBTL -> push_back(gp_ext.back().phi());
          inBTL=true;
        }
      }
    }

    //try ETL
    bool inETL=false;
    const vector<const DetLayer*>& layersETL = layerGeo->allETLLayers();
    for (const DetLayer* ilay : layersETL) 
    {
      const BoundDisk& disk = static_cast<const MTDRingForwardDoubleLayer*>(ilay)->specificSurface();
      const double diskZ = disk.position().z();
      if( tsos.globalPosition().z() * diskZ < 0 ) continue; // only propagate to the disk that's on the same side
      pair<bool, TrajectoryStateOnSurface> comp = ilay->compatible(tsos,prop,*theEstimator);	
      if (!comp.first) continue;
      vector<DetLayer::DetWithState> compDets = ilay->compatibleDets(tsos,prop,*theEstimator);
      for( const auto& detWithState : compDets ) 
      {
        gp_ext.push_back(detWithState.second.globalPosition());
        if (!inETL)
        {
          outTree_.track_eta_atETL -> push_back(gp_ext.back().eta());
          outTree_.track_phi_atETL -> push_back(gp_ext.back().phi());
          inETL=true;
        }
      }
    }

    if( !inBTL )
    {
      outTree_.track_eta_atBTL -> push_back(-999.);
      outTree_.track_phi_atBTL -> push_back(-999.);
    }

    if( !inETL )
    {
      outTree_.track_eta_atETL -> push_back(-999.);
      outTree_.track_phi_atETL -> push_back(-999.);
    }

    {
    if (dumpSimHits_)
	  {
	    //---get associated simHits
	    if( verbosity_ ) std::cout << "*** simHits - n tot: " << simHitsBTL.size() << std::endl;
	    int simHitIt = 0;
	    for(auto simHit : simHitsBTL)
	    {
        BTLDetId id = simHit.detUnitId();
        DetId geoId = id.geographicalId( crysLayout_ );
        const auto& det = mtdGeometry_ -> idToDet(geoId);
        const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
        const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());
          
        double energy = simHit.energyLoss()*1000.;
        double time   = simHit.tof();
        
        if ((time)<0 || (time)>25) continue;
        int RR = id.mtdRR();
        int module = id.module();
        int modType = id.modType();
        int crystal = id.crystal();
        int ieta = id.ieta(crysLayout_);
        int iphi = id.iphi(crysLayout_);
          
        LocalPoint lp_entry(   simHit.entryPoint().x()/10.,   simHit.entryPoint().y()/10.,   simHit.entryPoint().z()/10.);
        LocalPoint lp_mid  (simHit.localPosition().x()/10.,simHit.localPosition().y()/10.,simHit.localPosition().z()/10.);
        LocalPoint lp_exit (    simHit.exitPoint().x()/10.,    simHit.exitPoint().y()/10.,    simHit.exitPoint().z()/10.);
        GlobalPoint gp_entry = det->toGlobal(topo.pixelToModuleLocalPoint(lp_entry,id.row(topo.nrows()),id.column(topo.nrows())));
        GlobalPoint gp_mid   = det->toGlobal(topo.pixelToModuleLocalPoint(lp_mid,id.row(topo.nrows()),id.column(topo.nrows())));
        GlobalPoint gp_exit  = det->toGlobal(topo.pixelToModuleLocalPoint(lp_exit,id.row(topo.nrows()),id.column(topo.nrows())));
          
        float eta = gp_mid.eta();
        float phi = gp_mid.phi();
        
        int closestPoint=-1;
        float minDist=999;
        for (unsigned int ic=0; ic<gp_ext.size();++ic)
        {
          GlobalPoint diff(gp_ext[ic].x()-gp_mid.x(),gp_ext[ic].y()-gp_mid.y(),gp_ext[ic].z()-gp_mid.z());
          if (diff.mag()<minDist)
          {
            closestPoint=ic;
            minDist=diff.mag();
          }
        }
        
        if (closestPoint == -1)
          continue;
        
        GlobalPoint gp_track = gp_ext[closestPoint];      
        //GlobalPoint gp_track = gp_ext[abs(id.row(topo.nrows())-int())];
        
        float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
        float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
        float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
        float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp_mid.z()      : -999.;
        float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
        float dist  = gp_track.mag() > 0. ? (gp_mid-gp_track).mag()      : -999.;
        if( DR < 0.05 && DR > 0. )
        {
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":   energy: " << energy << " MeV   time: " << time << " ns"
            << "   RR: " << RR << "   module: " << module << "   modType: " << modType << "   crystal: " << crystal
            << "   ieta: " << ieta << "   iphi: " << iphi << "   row: " << id.row(topo.nrows()) << "   column: " << id.column(topo.nrows()) << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":   entryPoint:   local: " << PrintPosition(lp_entry)        << "   global: " << PrintPosition(gp_entry) << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":     midPoint:   local: " << PrintPosition(lp_mid)          << "   global: " << PrintPosition(gp_mid)   << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":    exitPoint:   local: " << PrintPosition(lp_exit)         << "   global: " << PrintPosition(gp_exit)  << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":  detPosition:  global: " << PrintPosition(det->position()) << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ": hit position:   local: " << PrintPosition(lp_mid)          << "   global: " << PrintPosition(gp_mid) << "   DR: " << DR << "   dist: " << (gp_track-gp_mid).mag() << std::endl;
        }
          
        if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
        if( gp_track.mag() <= 0. ) continue;
          
        outTree_.matchedSimHits_n->at(idx) += 1;
          
        outTree_.matchedSimHits_idx->at(idx).push_back(idx);
        outTree_.matchedSimHits_det->at(idx).push_back(1);
        outTree_.matchedSimHits_energy->at(idx).push_back(energy);
        outTree_.matchedSimHits_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
        outTree_.matchedSimHits_time->at(idx).push_back(time);
        outTree_.matchedSimHits_rr->at(idx).push_back(RR);
        outTree_.matchedSimHits_module->at(idx).push_back(module);
        outTree_.matchedSimHits_modType->at(idx).push_back(modType);
        outTree_.matchedSimHits_crystal->at(idx).push_back(crystal);
        outTree_.matchedSimHits_ieta->at(idx).push_back(ieta);
        outTree_.matchedSimHits_iphi->at(idx).push_back(iphi);
        outTree_.matchedSimHits_eta->at(idx).push_back(eta);
        outTree_.matchedSimHits_phi->at(idx).push_back(phi);
        outTree_.matchedSimHits_entry_local_x->at(idx).push_back(lp_entry.x());
        outTree_.matchedSimHits_entry_local_y->at(idx).push_back(lp_entry.y());
        outTree_.matchedSimHits_entry_local_z->at(idx).push_back(lp_entry.z());
        outTree_.matchedSimHits_entry_global_R->at(idx).push_back(sqrt(gp_entry.perp2()));
        outTree_.matchedSimHits_exit_local_x->at(idx).push_back(lp_exit.x());
        outTree_.matchedSimHits_exit_local_y->at(idx).push_back(lp_exit.y());
        outTree_.matchedSimHits_exit_local_z->at(idx).push_back(lp_exit.z());
        outTree_.matchedSimHits_exit_global_R->at(idx).push_back(sqrt(gp_exit.perp2()));
        outTree_.matchedSimHits_track_Deta->at(idx).push_back(fabs(Deta));
        outTree_.matchedSimHits_track_Dphi->at(idx).push_back(fabs(Dphi));
        outTree_.matchedSimHits_track_DR->at(idx).push_back(DR);
        outTree_.matchedSimHits_track_Dz->at(idx).push_back(Dz);
        outTree_.matchedSimHits_track_RDphi->at(idx).push_back(RDphi);
        outTree_.matchedSimHits_track_dist->at(idx).push_back(dist);
          
        ++simHitIt;
        }
        if( verbosity_ ) std::cout << "---" << std::endl;
        }
        
  //---find associated recHits
  float sieie=0, sipip=0;
  float ss_hit_count=0;
  if (dumpRecHits_)
  {
    int recHitIt = 0;
    if( verbosity_ ) std::cout << "*** recHits - tot: " << recHitsBTL.size() << std::endl;
    for(auto recHit : recHitsBTL)
    {
      BTLDetId id = recHit.id();
      DetId geoId = id.geographicalId( crysLayout_ );
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
        
      double energy = recHit.energy();
      double time   = recHit.time();
        
      MeasurementPoint mp(recHit.row()+0.5f,recHit.column()+0.5f); //to get the center you need +0.5
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      float eta = gp.eta();
      float phi = gp.phi();
        
      int RR = id.mtdRR();
      int module = id.module();
      int modType = id.modType();
      int crystal = id.crystal();
      int ieta = id.ieta(crysLayout_);
      int iphi = id.iphi(crysLayout_);
        
      int closestPoint=-1;
      float minDist=999;
      for (unsigned int ic=0; ic<gp_ext.size();++ic)
      {
        GlobalPoint diff(gp_ext[ic].x()-gp.x(),gp_ext[ic].y()-gp.y(),gp_ext[ic].z()-gp.z());
        if (diff.mag()<minDist)
        {
          closestPoint=ic;
          minDist=diff.mag();
        }
      }
        
      if (closestPoint == -1)
        continue;
      
      GlobalPoint gp_track = gp_ext[closestPoint];      
      //      GlobalPoint gp_track = gp_ext[abs(id.row(topo.nrows())-int())];
        
      float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
      float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
      float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
      float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp.z()          : -999.;
      float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
      float dist  = gp_track.mag() > 0. ? (gp-gp_track).mag()          : -999.;
        
      // if( DR < 0.2 && DR > 0. )
      {
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ":   energy: " << energy << " MeV   time: " << time << " ns"
          << "   RR: " << RR << "   module: " << module << "   modType: " << modType << "   crystal: " << crystal
          << "   ieta: " << ieta << "   iphi: " << iphi << "   row: " << recHit.row() << "- " << id.row(topo.nrows()) << "   column: " << recHit.column() << std::endl;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ":  detPosition:  global: " << PrintPosition(det->position()) << "   DR: " << DR << "   dist: " << (gp_track-det->position()).mag() << std::endl;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ": hit position:   local: " << PrintPosition(lp) << "   global: " << PrintPosition(gp) << "DR: " << DR << "   dist: " << (gp_track-gp).mag() << std::endl;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ": extrapolated track " << abs(recHit.row()-int()) << " : " << PrintPosition(gp_track) << std::endl;
      }
        
      if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
      if( gp_track.mag() <= 0. ) continue;
        
      outTree_.matchedRecHits_n->at(idx) += 1;
        
      outTree_.matchedRecHits_idx->at(idx).push_back(idx);
      outTree_.matchedRecHits_det->at(idx).push_back(1);
      outTree_.matchedRecHits_energy->at(idx).push_back(energy);
      outTree_.matchedRecHits_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
      outTree_.matchedRecHits_time->at(idx).push_back(time);
      outTree_.matchedRecHits_rr->at(idx).push_back(RR);
      outTree_.matchedRecHits_module->at(idx).push_back(module);
      outTree_.matchedRecHits_modType->at(idx).push_back(modType);
      outTree_.matchedRecHits_crystal->at(idx).push_back(crystal);
      outTree_.matchedRecHits_ieta->at(idx).push_back(ieta);
      outTree_.matchedRecHits_iphi->at(idx).push_back(iphi);
      outTree_.matchedRecHits_local_x->at(idx).push_back(lp.x());
      outTree_.matchedRecHits_local_y->at(idx).push_back(lp.y());
      outTree_.matchedRecHits_local_z->at(idx).push_back(lp.z());
      outTree_.matchedRecHits_global_R->at(idx).push_back(sqrt(gp.perp2()));
      outTree_.matchedRecHits_track_Deta->at(idx).push_back(fabs(Deta));
      outTree_.matchedRecHits_track_Dphi->at(idx).push_back(fabs(Dphi));
      outTree_.matchedRecHits_track_Dz->at(idx).push_back(Dz);
      outTree_.matchedRecHits_track_RDphi->at(idx).push_back(RDphi);
      outTree_.matchedRecHits_track_DR->at(idx).push_back(DR);
      outTree_.matchedRecHits_track_dist->at(idx).push_back(dist);
        
      if(recHit.energy() > 0.5)
      {
        sieie += energy*pow(eta-gp_track.eta(),2);
        sipip += energy*pow(phi-gp_track.phi(),2);
        ss_hit_count += energy;
      }
        
      ++recHitIt;
    }
  }  
  //---find associated recHits
  int clusterIt = 0;
  
  for (auto clusIt : clustersBTL)
  {    
    DetId id = clusIt.detId();
    const auto& det = mtdGeometry_ -> idToDet(id);
    const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
    const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
    for ( auto cluster : clusIt)
    {
      MTDDetId mtdId(id);
      int RR = 0;
      int module = 0;
      int modType = 0;
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
        
      if ( mtdId.mtdSubDetector() == MTDDetId::BTL )
      {
        BTLDetId btlId(id);
        RR = btlId.mtdRR();
        module = btlId.module();
        modType = btlId.modType();
        crystal = btlId.crystal();
        ieta = btlId.ieta(crysLayout_);
        iphi = btlId.iphi(crysLayout_);
      }
        
      double energy = cluster.energy();
      double time   = cluster.time();
      int size=cluster.size();
      int sizeX=cluster.sizeX();
      int sizeY=cluster.sizeY();
        
      MeasurementPoint mp(cluster.x(),cluster.y());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
        
      float eta = gp.eta();
      float phi = gp.phi();
        
      int closestPoint=-1;
      float minDist=999;
      for (unsigned int ic=0; ic<gp_ext.size();++ic)
      {
        GlobalPoint diff(gp_ext[ic].x()-gp.x(),gp_ext[ic].y()-gp.y(),gp_ext[ic].z()-gp.z());
        if (diff.mag()<minDist)
        {
          closestPoint=ic;
          minDist=diff.mag();
        }
      }
      
      if (closestPoint == -1)
        continue;
      
      GlobalPoint gp_track = gp_ext[closestPoint];      
      //	    GlobalPoint gp_track = gp_ext[abs(cluster.seed().x-int())];
        
      float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
      float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
      float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
      float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp.z()          : -999.;
      float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
      float dist  = gp_track.mag() > 0. ? (gp-gp_track).mag()          : -999.;
        
      if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
      if( gp_track.mag() <= 0. ) continue;
        
      outTree_.matchedClusters_n->at(idx) += 1;
        
      outTree_.matchedClusters_idx->at(idx).push_back(idx);
      outTree_.matchedClusters_det->at(idx).push_back(1);
      outTree_.matchedClusters_energy->at(idx).push_back(energy);
      outTree_.matchedClusters_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
      outTree_.matchedClusters_time->at(idx).push_back(time);
      outTree_.matchedClusters_rr->at(idx).push_back(RR);
      outTree_.matchedClusters_module->at(idx).push_back(module);
      outTree_.matchedClusters_modType->at(idx).push_back(modType);
      outTree_.matchedClusters_crystal->at(idx).push_back(crystal);
      outTree_.matchedClusters_ieta->at(idx).push_back(ieta);
      outTree_.matchedClusters_iphi->at(idx).push_back(iphi);
      outTree_.matchedClusters_size->at(idx).push_back(size);
      outTree_.matchedClusters_size_x->at(idx).push_back(sizeX);
      outTree_.matchedClusters_size_y->at(idx).push_back(sizeY);
      outTree_.matchedClusters_local_x->at(idx).push_back(lp.x());
      outTree_.matchedClusters_local_y->at(idx).push_back(lp.y());
      outTree_.matchedClusters_local_z->at(idx).push_back(lp.z());
      outTree_.matchedClusters_global_R->at(idx).push_back(sqrt(gp.perp2()));
      outTree_.matchedClusters_track_Deta->at(idx).push_back(fabs(Deta));
      outTree_.matchedClusters_track_Dphi->at(idx).push_back(fabs(Dphi));
      outTree_.matchedClusters_track_Dz->at(idx).push_back(Dz);
      outTree_.matchedClusters_track_RDphi->at(idx).push_back(RDphi);
      outTree_.matchedClusters_track_DR->at(idx).push_back(DR);
      outTree_.matchedClusters_track_dist->at(idx).push_back(dist);
        
      ++clusterIt;
    }
  }
  
  
  if( verbosity_ ) std::cout << "---\n\n\n" << std::endl;
  
  if (dumpRecHits_)
  {
    outTree_.matchedRecHits_sietaieta->at(idx).push_back( ss_hit_count>0 ? sqrt(sieie)/ss_hit_count : -999. );
    outTree_.matchedRecHits_siphiiphi->at(idx).push_back( ss_hit_count>0 ? sqrt(sipip)/ss_hit_count : -999. );
  }
  }
  ///ETL
  {
  if (dumpSimHits_)
  {
    //---get associated simHits
    if( verbosity_ ) std::cout << "*** simHits - n tot: " << simHitsETL.size() << std::endl;
    int simHitIt = 0;
    for(auto simHit : simHitsETL)
    {
      ETLDetId id = simHit.detUnitId();
      DetId geoId = id.geographicalId(  );
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());
        
      double energy = simHit.energyLoss()*1000.;
      double time   = simHit.tof();
      
      if ((time)<0 || (time)>25) continue;
        
      int RR = id.mtdRR();
      int module = id.module();
      int modType = id.modType();
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
      
      // ETL is already in module-local coordinates so just scale to cm from mm
      Local3DPoint simscaled(0.1*simHit.entryPoint().x(),0.1*simHit.entryPoint().y(),0.1*simHit.entryPoint().z());
      const auto& thepixel = topo.pixel(simscaled); // mm -> cm here is the switch                               
      const uint8_t row(thepixel.first), col(thepixel.second);
        
      LocalPoint lp_entry(   simHit.entryPoint().x()/10.,   simHit.entryPoint().y()/10.,   simHit.entryPoint().z()/10.);
      LocalPoint lp_mid  (simHit.localPosition().x()/10.,simHit.localPosition().y()/10.,simHit.localPosition().z()/10.);
      LocalPoint lp_exit (    simHit.exitPoint().x()/10.,    simHit.exitPoint().y()/10.,    simHit.exitPoint().z()/10.);
      GlobalPoint gp_entry = det->toGlobal(topo.pixelToModuleLocalPoint(lp_entry ,row,col));
      GlobalPoint gp_mid   = det->toGlobal(topo.pixelToModuleLocalPoint(lp_mid   ,row,col));
      GlobalPoint gp_exit  = det->toGlobal(topo.pixelToModuleLocalPoint(lp_exit  ,row,col));
        
      float eta = gp_mid.eta();
      float phi = gp_mid.phi();
      
      int closestPoint=-1;
      float minDist=999;
      for (unsigned int ic=0; ic<gp_ext.size();++ic)
      {
        GlobalPoint diff(gp_ext[ic].x()-gp_mid.x(),gp_ext[ic].y()-gp_mid.y(),gp_ext[ic].z()-gp_mid.z());
        if (diff.mag()<minDist)
        {
          closestPoint=ic;
          minDist=diff.mag();
        }
      }
      
      if (closestPoint == -1)
        continue;
      
      GlobalPoint gp_track = gp_ext[closestPoint];      
      
      float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
      float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
      float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
      float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp_mid.z()      : -999.;
      float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
      float dist  = gp_track.mag() > 0. ? (gp_mid-gp_track).mag()      : -999.;
      if( DR < 0.05 && DR > 0. )
        {
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":   energy: " << energy << " MeV   time: " << time << " ns"
             << "   RR: " << RR << "   module: " << module << "   modType: " << modType << "   crystal: " << crystal;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":   entryPoint:   local: " << PrintPosition(lp_entry)        << "   global: " << PrintPosition(gp_entry) << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":     midPoint:   local: " << PrintPosition(lp_mid)          << "   global: " << PrintPosition(gp_mid)   << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":    exitPoint:   local: " << PrintPosition(lp_exit)         << "   global: " << PrintPosition(gp_exit)  << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ":  detPosition:  global: " << PrintPosition(det->position()) << std::endl;
          if( verbosity_ ) std::cout << ">>> " << simHitIt << ": hit position:   local: " << PrintPosition(lp_mid)          << "   global: " << PrintPosition(gp_mid) << "   DR: " << DR << "   dist: " << (gp_track-gp_mid).mag() << std::endl;
        }
        
      if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
      if( gp_track.mag() <= 0. ) continue;
        
      outTree_.matchedSimHits_n->at(idx) += 1;
        
      outTree_.matchedSimHits_idx->at(idx).push_back(idx);
      outTree_.matchedSimHits_det->at(idx).push_back(2);
      outTree_.matchedSimHits_energy->at(idx).push_back(energy);
      outTree_.matchedSimHits_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
      outTree_.matchedSimHits_time->at(idx).push_back(time);
      outTree_.matchedSimHits_rr->at(idx).push_back(RR);
      outTree_.matchedSimHits_module->at(idx).push_back(module);
      outTree_.matchedSimHits_modType->at(idx).push_back(modType);
      outTree_.matchedSimHits_crystal->at(idx).push_back(crystal);
      outTree_.matchedSimHits_ieta->at(idx).push_back(ieta);
      outTree_.matchedSimHits_iphi->at(idx).push_back(iphi);
      outTree_.matchedSimHits_entry_local_x->at(idx).push_back(lp_entry.x());
      outTree_.matchedSimHits_entry_local_y->at(idx).push_back(lp_entry.y());
      outTree_.matchedSimHits_entry_local_z->at(idx).push_back(lp_entry.z());
      outTree_.matchedSimHits_entry_global_R->at(idx).push_back(sqrt(gp_entry.perp2()));
      outTree_.matchedSimHits_exit_local_x->at(idx).push_back(lp_exit.x());
      outTree_.matchedSimHits_exit_local_y->at(idx).push_back(lp_exit.y());
      outTree_.matchedSimHits_exit_local_z->at(idx).push_back(lp_exit.z());
      outTree_.matchedSimHits_exit_global_R->at(idx).push_back(sqrt(gp_exit.perp2()));
      outTree_.matchedSimHits_track_Deta->at(idx).push_back(fabs(Deta));
      outTree_.matchedSimHits_track_Dphi->at(idx).push_back(fabs(Dphi));
      outTree_.matchedSimHits_track_DR->at(idx).push_back(DR);
      outTree_.matchedSimHits_track_Dz->at(idx).push_back(Dz);
      outTree_.matchedSimHits_track_RDphi->at(idx).push_back(RDphi);
      outTree_.matchedSimHits_track_dist->at(idx).push_back(dist);
        
      ++simHitIt;
    }
  if( verbosity_ ) std::cout << "---" << std::endl;
  }
  
  //---find associated recHits
  float sieie=0, sipip=0;
  float ss_hit_count=0;
  
  if (dumpRecHits_)
  {
    int recHitIt = 0;
    if( verbosity_ ) std::cout << "*** recHits - tot: " << recHitsETL.size() << std::endl;
    for(auto recHit : recHitsETL)
    {
      ETLDetId id = recHit.id();
      DetId geoId = id.geographicalId(  );
      const auto& det = mtdGeometry_ -> idToDet(geoId);
      const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
      const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
        
      double energy = recHit.energy();
      double time   = recHit.time();
        
      MeasurementPoint mp(recHit.row()+0.5f,recHit.column()+0.5f);
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
      
      float eta = gp.eta();
      float phi = gp.phi();
        
      int RR = id.mtdRR();
      int module = id.module();
      int modType = id.modType();
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
        
      int closestPoint=-1;
      float minDist=999;
      for (unsigned int ic=0; ic<gp_ext.size();++ic)
      {
        GlobalPoint diff(gp_ext[ic].x()-gp.x(),gp_ext[ic].y()-gp.y(),gp_ext[ic].z()-gp.z());
        if (diff.mag()<minDist)
        {
          closestPoint=ic;
          minDist=diff.mag();
        }
      }
        
      if (closestPoint == -1)
        continue;
      
      GlobalPoint gp_track = gp_ext[closestPoint];      
        
      float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
      float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
      float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
      float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp.z()          : -999.;
      float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
      float dist  = gp_track.mag() > 0. ? (gp-gp_track).mag()          : -999.;
        
      // if( DR < 0.2 && DR > 0. )
      {
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ":   energy: " << energy << " MeV   time: " << time << " ns"
      			     << "   RR: " << RR << "   module: " << module << "   modType: " << modType << "   crystal: " << crystal;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ":  detPosition:  global: " << PrintPosition(det->position()) << "   DR: " << DR << "   dist: " << (gp_track-det->position()).mag() << std::endl;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ": hit position:   local: " << PrintPosition(lp) << "   global: " << PrintPosition(gp) << "DR: " << DR << "   dist: " << (gp_track-gp).mag() << std::endl;
        if( verbosity_ ) std::cout << ">>> " << recHitIt << ": extrapolated track " << abs(recHit.row()-int()) << " : " << PrintPosition(gp_track) << std::endl;
      }
        
      if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
      if( gp_track.mag() <= 0. ) continue;
        
      outTree_.matchedRecHits_n->at(idx) += 1;
        
      outTree_.matchedRecHits_idx->at(idx).push_back(idx);
      outTree_.matchedRecHits_det->at(idx).push_back(2);
      outTree_.matchedRecHits_energy->at(idx).push_back(energy);
      outTree_.matchedRecHits_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
      outTree_.matchedRecHits_time->at(idx).push_back(time);
      outTree_.matchedRecHits_rr->at(idx).push_back(RR);
      outTree_.matchedRecHits_module->at(idx).push_back(module);
      outTree_.matchedRecHits_modType->at(idx).push_back(modType);
      outTree_.matchedRecHits_crystal->at(idx).push_back(crystal);
      outTree_.matchedRecHits_ieta->at(idx).push_back(ieta);
      outTree_.matchedRecHits_iphi->at(idx).push_back(iphi);
      outTree_.matchedRecHits_local_x->at(idx).push_back(lp.x());
      outTree_.matchedRecHits_local_y->at(idx).push_back(lp.y());
      outTree_.matchedRecHits_local_z->at(idx).push_back(lp.z());
      outTree_.matchedRecHits_global_R->at(idx).push_back(sqrt(gp.perp2()));
      outTree_.matchedRecHits_track_Deta->at(idx).push_back(fabs(Deta));
      outTree_.matchedRecHits_track_Dphi->at(idx).push_back(fabs(Dphi));
      outTree_.matchedRecHits_track_Dz->at(idx).push_back(Dz);
      outTree_.matchedRecHits_track_RDphi->at(idx).push_back(RDphi);
      outTree_.matchedRecHits_track_DR->at(idx).push_back(DR);
      outTree_.matchedRecHits_track_dist->at(idx).push_back(dist);
        
      if(recHit.energy() > 0.5)
      {
        sieie += energy*pow(eta-gp_track.eta(),2);
        sipip += energy*pow(phi-gp_track.phi(),2);
        ss_hit_count += energy;
      }
        
      ++recHitIt;
    }
  }  
  //---find associated recHits
  int clusterIt = 0;
  
  for (auto clusIt : clustersETL)
  {    
    DetId id = clusIt.detId();
    const auto& det = mtdGeometry_ -> idToDet(id);
    const ProxyMTDTopology& topoproxy = static_cast<const ProxyMTDTopology&>(det->topology());
    const RectangularMTDTopology& topo = static_cast<const RectangularMTDTopology&>(topoproxy.specificTopology());    
    for ( auto cluster : clusIt)
    {
      MTDDetId mtdId(id);
      int RR = 0;
      int module = 0;
      int modType = 0;
      int crystal = 0;
      int ieta = 0;
      int iphi = 0;
        
      if ( mtdId.mtdSubDetector() == MTDDetId::ETL )
      {
        ETLDetId btlId(id);
        RR = btlId.mtdRR();
        module = btlId.module();
        modType = btlId.modType();
        // crystal = btlId.crystal();
        // ieta = btlId.ieta();
        // iphi = btlId.iphi();
      }
        
      double energy = cluster.energy();
      double time   = cluster.time();
      int size=cluster.size();
      int sizeX=cluster.sizeX();
      int sizeY=cluster.sizeY();
        
      MeasurementPoint mp(cluster.x(),cluster.y());
      LocalPoint lp = topo.localPosition(mp);
      GlobalPoint gp = det->toGlobal(lp);
        
      float eta = gp.eta();
      float phi = gp.phi();
        
      int closestPoint=-1;
      float minDist=999;
      for (unsigned int ic=0; ic<gp_ext.size();++ic)
      {
        GlobalPoint diff(gp_ext[ic].x()-gp.x(),gp_ext[ic].y()-gp.y(),gp_ext[ic].z()-gp.z());
        if (diff.mag()<minDist)
        {
          closestPoint=ic;
          minDist=diff.mag();
        }
      }
        
      if (closestPoint == -1)
        continue;
      
      GlobalPoint gp_track = gp_ext[closestPoint];      
        
      float Deta  = gp_track.mag() > 0. ? eta-gp_track.eta()           : -999.;
      float Dphi  = gp_track.mag() > 0. ? deltaPhi(phi,gp_track.phi()) : -999.;
      float DR    = gp_track.mag() > 0. ? sqrt(Deta*Deta+Dphi*Dphi)    : -999.;
      float Dz    = gp_track.mag() > 0. ? gp_track.z()-gp.z()          : -999.;
      float RDphi = gp_track.mag() > 0. ? sqrt(gp_track.perp2())*Dphi  : -999.;
      float dist  = gp_track.mag() > 0. ? (gp-gp_track).mag()          : -999.;
        
      if( DR > track_hit_DRMax_ || dist > track_hit_distMax_ ) continue;
      if( gp_track.mag() <= 0. ) continue;
        
      outTree_.matchedClusters_n->at(idx) += 1;
        
      outTree_.matchedClusters_idx->at(idx).push_back(idx);
      outTree_.matchedClusters_det->at(idx).push_back(2);
      outTree_.matchedClusters_energy->at(idx).push_back(energy);
      outTree_.matchedClusters_energyCorr->at(idx).push_back(energy*fabs(sin(track.theta())));
      outTree_.matchedClusters_time->at(idx).push_back(time);
      outTree_.matchedClusters_rr->at(idx).push_back(RR);
      outTree_.matchedClusters_module->at(idx).push_back(module);
      outTree_.matchedClusters_modType->at(idx).push_back(modType);
      outTree_.matchedClusters_crystal->at(idx).push_back(crystal);
      outTree_.matchedClusters_ieta->at(idx).push_back(ieta);
      outTree_.matchedClusters_iphi->at(idx).push_back(iphi);
      outTree_.matchedClusters_size->at(idx).push_back(size);
      outTree_.matchedClusters_size_x->at(idx).push_back(sizeX);
      outTree_.matchedClusters_size_y->at(idx).push_back(sizeY);
      outTree_.matchedClusters_local_x->at(idx).push_back(lp.x());
      outTree_.matchedClusters_local_y->at(idx).push_back(lp.y());
      outTree_.matchedClusters_local_z->at(idx).push_back(lp.z());
      outTree_.matchedClusters_global_R->at(idx).push_back(sqrt(gp.perp2()));
      outTree_.matchedClusters_track_Deta->at(idx).push_back(fabs(Deta));
      outTree_.matchedClusters_track_Dphi->at(idx).push_back(fabs(Dphi));
      outTree_.matchedClusters_track_Dz->at(idx).push_back(Dz);
      outTree_.matchedClusters_track_RDphi->at(idx).push_back(RDphi);
      outTree_.matchedClusters_track_DR->at(idx).push_back(DR);
      outTree_.matchedClusters_track_dist->at(idx).push_back(dist);
        
      ++clusterIt;
    }
  }
  
  
  if( verbosity_ ) std::cout << "---\n\n\n" << std::endl;
  if (dumpRecHits_)
  {
    outTree_.matchedRecHits_sietaieta->at(idx).push_back( ss_hit_count>0 ? sqrt(sieie)/ss_hit_count : -999. );
    outTree_.matchedRecHits_siphiiphi->at(idx).push_back( ss_hit_count>0 ? sqrt(sipip)/ss_hit_count : -999. );
  }
  }
  ++idx;
  }
  
  outTree_.GetTTreePtr()->Fill();
}


std::string FTLDumpHits::PrintPosition(const GlobalPoint& gp)
{
  std::stringstream output;
  
  output << "(";
  output << std::fixed << std::setprecision(3) << std::setw(8) << gp.x() << ",";
  output << std::fixed << std::setprecision(3) << std::setw(8) << gp.y() << ",";
  output << std::fixed << std::setprecision(3) << std::setw(8) << gp.z();
  output << ") cm";
  
  output << "   R: " << std::fixed << std::setprecision(3) << std::setw(7) << gp.perp();
  output << " cm";
  
  output << "   eta: " << std::setprecision(3) << std::setw(6) << gp.eta(); 
  output << "   phi: " << std::setprecision(3) << std::setw(6) << gp.phi();
  
  return output.str();
}

std::string FTLDumpHits::PrintPosition(const LocalPoint& lp)
{
  std::stringstream output;
  
  output << "(";
  output << std::fixed << std::setprecision(3) << std::setw(8) << lp.x() << ",";
  output << std::fixed << std::setprecision(3) << std::setw(8) << lp.y() << ",";
  output << std::fixed << std::setprecision(3) << std::setw(8) << lp.z();
  output << ") cm";
  
  return output.str();
}
DEFINE_FWK_MODULE(FTLDumpHits);

#endif
