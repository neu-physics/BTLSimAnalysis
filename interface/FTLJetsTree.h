#ifndef FTL_JETS_TREE
#define FTL_JETS_TREE

#include "ExternalTools/DynamicTTree/interface/DynamicTTreeBase.h"

using namespace std;

//---Define the TTree branches
#define DYNAMIC_TREE_NAME FTLJetsTree

#define DATA_TABLE          \
  DATA(int, event)          \
  DATA(int, lumi)           \
  DATA(int, run)            \
  DATA(int, genLeptons_n)   \
  DATA(float, genVtx_x)     \
  DATA(float, genVtx_y)     \
  DATA(float, genVtx_z)     \
  DATA(float, genVtx_t)     \
  DATA(int, jets_n)         \
  DATA(int, vtxs_n)         \
  
#define DATA_CLASS_TABLE                           \
  DATA(std::vector<float>, genLeptons_pt)          \
  DATA(std::vector<float>, genLeptons_eta)         \
  DATA(std::vector<float>, genLeptons_phi)         \
  DATA(std::vector<float>, genLeptons_energy)      \
  DATA(std::vector<int>,   genLeptons_charge)      \
  DATA(std::vector<int>,   genLeptons_pdgId)       \
  DATA(std::vector<float>, genLeptons_vtx_x)       \
  DATA(std::vector<float>, genLeptons_vtx_y)       \
  DATA(std::vector<float>, genLeptons_vtx_z)       \
  DATA(std::vector<float>, vtxs_x)                 \
  DATA(std::vector<float>, vtxs_y)                 \
  DATA(std::vector<float>, vtxs_z)                 \
  DATA(std::vector<float>, vtxs_t)                 \
  DATA(std::vector<float>, vtxs_normalizedChi2)    \
  DATA(vector<float>, jets_pt)                     \
  DATA(vector<float>, jets_eta)                    \
  DATA(vector<float>, jets_phi)                    \
  DATA(vector<float>, jets_energy)                 \
  DATA(vector<int>,   jets_isPU)                   \
  DATA(vector<float>, jets_matchedGenJet_pt)       \
  DATA(vector<float>, jets_matchedGenJet_eta)      \
  DATA(vector<float>, jets_matchedGenJet_phi)      \
  DATA(vector<float>, jets_matchedGenJet_energy)

#include "ExternalTools/DynamicTTree/interface/DynamicTTreeInterface.h"

#endif
