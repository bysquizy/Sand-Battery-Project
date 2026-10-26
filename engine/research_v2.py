"""Advanced v2 demonstrators: scenarios, not calibrated plant predictions."""
from dataclasses import dataclass
import math
import numpy as np
from scipy.integrate import solve_ivp
from .physics import summarize,J_PER_MWH,geometry

def exergy_mwh(m,volume,tmin,tmax,ambient):
    if not (-273.15 < ambient <= tmin < tmax): raise ValueError("Invalid exergy temperatures")
    lo=tmin+273.15;hi=tmax+273.15;ta=ambient+273.15
    a=m.cp_25-298.15*m.cp_slope;b=m.cp_slope
    return max(0,m.bulk_density*volume*((a-ta*b)*(hi-lo)+b*(hi*hi-lo*lo)/2-ta*a*math.log(hi/lo))/J_PER_MWH)

def invert_energy(m,mass,e_mwh,tmin):
    if mass<=0 or e_mwh<0:raise ValueError("Invalid heat state")
    cp=m.cp(tmin);b=m.cp_slope;h=e_mwh*J_PER_MWH/mass
    if cp<=0:raise ValueError("Invalid cp")
    return tmin+(h/cp if abs(b)<1e-12 else 2*h/(cp+math.sqrt(cp*cp+2*b*h)))

def illustrative_renewables(hours=168,pv_mwp=10,wind_mw=8,seed=11):
    if not 1<=hours<=8760 or min(pv_mwp,wind_mw)<0:raise ValueError("Invalid renewable parameters")
    t=np.arange(hours);rng=np.random.default_rng(seed)
    pv=pv_mwp*.75*np.maximum(0,np.sin((t%24-6)/12*np.pi))**1.7
    wind=wind_mw*np.clip(.32+.13*np.sin(t*2*np.pi/48)+rng.normal(0,.07,hours),0,1)
    return pv+wind

def dispatch(d,m,available_mw,demand_mw):
    s=summarize(d,m);cap=s['capacity_mwh'];state=0.;mass=d.volume_m3*m.bulk_density
    supply=np.asarray(available_mw,dtype=float);demand=np.broadcast_to(np.asarray(demand_mw,dtype=float),supply.shape)
    if supply.ndim!=1 or not 1<=len(supply)<=8760 or not np.all(np.isfinite(supply)) or not np.all(np.isfinite(demand)) or min(np.min(supply),np.min(demand))<0:raise ValueError("Invalid hourly data")
    soc=[0.];delivered=[];losses=[];curtailed=[];unmet=[];accepted=[]
    for src,load in zip(supply,demand):
        loss=min(state,max(0.,s['ua_w_k']*(invert_energy(m,mass,state,d.minimum_c)-d.ambient_c)/1e6))
        state-=loss
        inp=min(src,d.charge_mw,(cap-state)/d.charge_efficiency)
        state+=inp*d.charge_efficiency
        take=min(load,d.thermal_output_mw,state)
        state-=take
        soc.append(100*state/cap);delivered.append(take);losses.append(loss);curtailed.append(src-inp);unmet.append(load-take);accepted.append(inp)
    accepted=np.asarray(accepted);delivered=np.asarray(delivered);losses=np.asarray(losses)
    return {'soc_pct':np.asarray(soc),'delivered_mwh':delivered,'loss_mwh':losses,'curtailed_mwh':np.asarray(curtailed),
      'unmet_mwh':np.asarray(unmet),'available_mw':supply,'demand_mw':demand,
      'balance_residual_mwh':float(accepted.sum()-(accepted*(1-d.charge_efficiency)).sum()-losses.sum()-delivered.sum()-state)}

@dataclass(frozen=True)
class Exchanger:
    hot_in_c:float=500.;cold_in_c:float=60.;ch_kw_k:float=25.;cc_kw_k:float=20.;ua_kw_k:float=40.;kind:str='counterflow'
def exchanger(p):
    if p.hot_in_c<=p.cold_in_c or min(p.ch_kw_k,p.cc_kw_k,p.ua_kw_k)<=0 or p.kind not in ('counterflow','parallel'):raise ValueError("Invalid exchanger inputs")
    cmin=min(p.ch_kw_k,p.cc_kw_k);cr=cmin/max(p.ch_kw_k,p.cc_kw_k);ntu=p.ua_kw_k/cmin
    if p.kind=='parallel':eff=-math.expm1(-ntu*(1+cr))/(1+cr)
    elif abs(cr-1)<1e-10:eff=ntu/(1+ntu)
    else:
        x=math.exp(-ntu*(1-cr));eff=(1-x)/(1-cr*x)
    q=eff*cmin*(p.hot_in_c-p.cold_in_c)
    return {'effectiveness':eff,'ntu':ntu,'q_mw':q/1000,'hot_out_c':p.hot_in_c-q/p.ch_kw_k,'cold_out_c':p.cold_in_c+q/p.cc_kw_k}
def ergun(height,area,void,diameter,velocity,viscosity=3.5e-5,rho=.9,fan_eff=.65):
    if min(height,area,diameter,viscosity,rho,fan_eff)<=0 or not .15<=void<=.75 or velocity<0 or fan_eff>1:raise ValueError("Invalid packed-bed input")
    gradient=150*viscosity*(1-void)**2/(void**3*diameter**2)*velocity+1.75*rho*(1-void)/(void**3*diameter)*velocity**2
    drop=height*gradient
    return {'delta_p_pa':drop,'fan_kw':drop*velocity*area/fan_eff/1000,'particle_re':rho*velocity*diameter/viscosity}
def uncertainty(d,m,n=400,spread=.1,seed=17):
    if not 50<=n<=5000 or not 0<=spread<=.5:raise ValueError("Invalid uncertainty settings")
    s=summarize(d,m);r=np.random.default_rng(seed)
    f=np.maximum(.05,r.normal(1,spread,(n,3)))
    return {'capacity_samples_mwh':s['capacity_mwh']*f[:,0]*f[:,1],
            'loss_samples_kw':s['initial_loss_kw']*f[:,2]}
def levelized_heat(capex,years,rate,cycles,delivered_mwh,input_mwh,energy_price,fixed_om):
    if capex<0 or not 1<=years<=50 or not 0<=rate<=.5 or min(cycles,delivered_mwh,input_mwh,energy_price,fixed_om)<0 or cycles*delivered_mwh<=0:raise ValueError("Invalid cost scenario")
    crf=1/years if rate==0 else rate/(1-(1+rate)**(-years))
    return (capex*crf+fixed_om+cycles*input_mwh*energy_price)/(cycles*delivered_mwh)

@dataclass(frozen=True)
class LTNE:
    cells:int=20;hours:float=2.;inlet_c:float=520.;initial_c:float=60.
    velocity:float=.012;void:float=.42;gas_rho:float=.9;gas_cp:float=1050.
    hv:float=1500.;k_s:float=1.;k_g:float=.05
def ltne(d,m,c):
    d.validate()
    if not 8<=c.cells<=48 or not 0<c.hours<=24 or not 0<c.void<.85 or not 0<=c.velocity<2 or min(c.gas_rho,c.gas_cp,c.hv,c.k_s,c.k_g)<=0:raise ValueError("Invalid LTNE settings")
    r,h=geometry(d.volume_m3/d.modules,d.height_over_radius);dz=h/c.cells
    cg=c.void*c.gas_rho*c.gas_cp;adv=c.gas_rho*c.gas_cp*c.velocity/dz
    wall=summarize(d,m)['ua_w_k']/d.volume_m3
    flux=c.gas_rho*c.gas_cp*c.velocity*np.pi*r*r*d.modules
    y0=np.r_[np.full(c.cells,c.initial_c),np.full(c.cells,c.initial_c),0.,0.]
    def lap(v):
        o=np.empty_like(v);o[1:-1]=(v[:-2]-2*v[1:-1]+v[2:])/dz**2
        o[0]=(v[1]-v[0])/dz**2;o[-1]=(v[-2]-v[-1])/dz**2
        return o
    def f(_t,y):
        g=y[:c.cells];s=y[c.cells:-2];inter=c.hv*(g-s)
        dg=(adv*(np.r_[c.inlet_c,g[:-1]]-g)+c.k_g*lap(g)-inter)/cg
        ds=(c.k_s*lap(s)+inter-wall*(s-d.ambient_c))/(m.bulk_density*m.cp(s))
        return np.r_[dg,ds,flux*(c.inlet_c-g[-1]),wall*np.mean(s-d.ambient_c)*d.volume_m3]
    t=np.linspace(0,c.hours*3600,36)
    sol=solve_ivp(f,(0,t[-1]),y0,t_eval=t,method='BDF',rtol=5e-6,atol=1e-5)
    if not sol.success or not np.all(np.isfinite(sol.y)):raise RuntimeError("Two-temperature solver failed")
    gas=sol.y[:c.cells].T;solid=sol.y[c.cells:-2].T
    vol=d.volume_m3/c.cells
    de=m.bulk_density*vol*np.sum(m.enthalpy(solid[-1])-m.enthalpy(c.initial_c))+cg*d.volume_m3*np.mean(gas[-1]-c.initial_c)
    return {'time_h':sol.t/3600,'z_m':(np.arange(c.cells)+.5)*dz,'gas_c':gas,'solid_c':solid,'residual_mwh':(sol.y[-2,-1]-sol.y[-1,-1]-de)/J_PER_MWH}
