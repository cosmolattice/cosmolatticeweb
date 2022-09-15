#ifndef TANHPDANI_H  
#define TANHPDANI_H

#include "CosmoInterface/cosmointerface.h"


namespace TempLat
{

    struct ModelPars : public TempLat::DefaultModelPars {
        static constexpr size_t NScalars = 2;
        static constexpr size_t NPotTerms = 2;
    };

  #define MODELNAME tanhpDani

  template<class R>
  using Model = MakeModel(R, ModelPars);

  class MODELNAME : public Model<MODELNAME>

  {

private:

	double M, Lambda, phii, omega, q, g, Mphi, Lphi, pExp;
  
  public:
  
    //static constexpr int pExp = 4;

    MODELNAME(ParameterParser& parser, RunParameters<double>& runPar, std::shared_ptr<MemoryToolBox> toolBox): //Constructor of our model.
    Model<MODELNAME>(parser,runPar.getLatParams(), toolBox, runPar.dt, STRINGIFY(MODELLABEL)) //MODELLABEL is defined in the cmake.
    {
        M = parser.get<double>("M");
        Lambda = parser.get<double>("Lambda");
        q = parser.get<double>("q");
        pExp = parser.get<double>("pExp");
        
        fldS0 = parser.get<double, 2>("initial_amplitudes");
        piS0 = parser.get<double, 2>("initial_momenta", {0, 0});
        
        phii = fldS0[0];
        Mphi = M/phii;
        Lphi = Lambda/phii;
        omega = phii*pow(Lphi,2)/pow(Mphi,pExp/2);//sqrt(Lambda4)/M;
        g = sqrt(q)*omega/phii;


        alpha = 3.0 * (pExp - 2.0) / (pExp + 2.0);
   		fStar = fldS0[0];
   		omegaStar = omega;
   		 
   		setInitialPotentialAndMassesFromPotential();
   		
   	}
   		    
    auto potentialTerms(Tag<0>){ return pow(Mphi,pExp) * pow(tanh(fldS(0_c)/Mphi),pExp) / pExp; }
    auto potentialTerms(Tag<1>){ return 0.5 * q * pow<2>(fldS(0_c)) * pow<2>(fldS(1_c)); }
    
    auto potDeriv(Tag<0>){ return 2*pow(M/phii,pExp-1) * pow(tanh(fldS(0_c)/Mphi),pExp)/sinh(2*fldS(0_c)/Mphi) + q * fldS(0_c) * pow<2>(fldS(1_c)); }
    auto potDeriv(Tag<1>){ return  q * fldS(1_c) * pow<2>(fldS(0_c)); }

    auto potDeriv2(Tag<0>){ return  4 * pow(Mphi,pExp-2) * (pExp - cosh(2*fldS(0_c)/Mphi) ) * pow(tanh(fldS(0_c)/Mphi),pExp) / pow<2>(sinh(2*fldS(0_c)/Mphi)) +  q * pow<2>(fldS(1_c)); }
    auto potDeriv2(Tag<1>){ return  q * pow<2>(fldS(0_c)); }

    };
}

#endif //TANHPDANI_H