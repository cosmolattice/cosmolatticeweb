#ifndef TANHP4DANI_H  
#define TANHP4DANI_H

#include "CosmoInterface/cosmointerface.h"


namespace TempLat
{

    struct ModelPars : public TempLat::DefaultModelPars {
        static constexpr size_t NScalars = 2;
        static constexpr size_t NPotTerms = 2;
    };

  #define MODELNAME tanhp4Dani

  template<class R>
  using Model = MakeModel(R, ModelPars);

  class MODELNAME : public Model<MODELNAME>

  {

private:

	double M, Lambda, phii, omega, q, g, Mphi, Lphi;
  
  public:
  
    //static constexpr int pExp = 4;

    MODELNAME(ParameterParser& parser, RunParameters<double>& runPar, std::shared_ptr<MemoryToolBox> toolBox): //Constructor of our model.
    Model<MODELNAME>(parser,runPar.getLatParams(), toolBox, runPar.dt, STRINGIFY(MODELLABEL)) //MODELLABEL is defined in the cmake.
    {
        M = parser.get<double>("M");
        Lambda = parser.get<double>("Lambda");
        q = parser.get<double>("q");
        
        fldS0 = parser.get<double, 2>("initial_amplitudes");
        piS0 = parser.get<double, 2>("initial_momenta", {0, 0});
        
        phii = fldS0[0];
        Mphi = M/phii;
        Lphi = Lambda/phii;
        omega = phii*pow<2>(Lphi)/pow<2>(Mphi);//sqrt(Lambda4)/M;
        g = sqrt(q)*omega/phii;


        alpha = 0.;
   		fStar = fldS0[0];
   		omegaStar = omega;
   		 
   		setInitialPotentialAndMassesFromPotential();
   		
   	}
   		    
    auto potentialTerms(Tag<0>){ return pow<4>(Mphi) * pow<4>(tanh(fldS(0_c)/Mphi)) / 4; }
    auto potentialTerms(Tag<1>){ return 0.5 * q * pow<2>(fldS(0_c)) * pow<2>(fldS(1_c)); }
    
    auto potDeriv(Tag<0>){ return 2*pow<3>(M/phii) * pow<4>(tanh(fldS(0_c)/Mphi))/sinh(2*fldS(0_c)/Mphi) + q * fldS(0_c) * pow<2>(fldS(1_c)); }
    auto potDeriv(Tag<1>){ return  q * fldS(1_c) * pow<2>(fldS(0_c)); }

    auto potDeriv2(Tag<0>){ return  4 * pow<2>(Mphi) * (4 - cosh(2*fldS(0_c)/Mphi) ) * pow<4>(tanh(fldS(0_c)/Mphi)) / pow<2>(sinh(2*fldS(0_c)/Mphi)) +  q * pow<2>(fldS(1_c)); }
    auto potDeriv2(Tag<1>){ return  q * pow<2>(fldS(0_c)); }

    };
}

#endif //TANHP4DANI_H