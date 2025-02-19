from openfast_toolbox.fastfarm.FASTFarmCaseCreation import FFCaseCreation

path = 'fastfarm/case'

# ----------- General hard-coded parameters
cmax = 5       # maximum blade chord (m)
fmax = 10 / 6  # maximum excitation frequency (Hz)
Cmeander = 1.9  # Meandering constant (-)

# ----------- Wind farm
D = 125.0  # Rotor diameter
zhub = 90  # Hub height
wts = {
    0: {'x': 0.0, 'y': 0, 'z': 0.0, 'D': D, 'zhub': zhub, 'cmax': cmax, 'fmax': fmax, 'Cmeander': Cmeander},
}
refTurb_rot = 0  # Reference turbine for rotational effects

# ----------- Additional variables
tmax = 1800  # Total simulation time
nSeeds = 2  # Number of different seeds
zbot = 1  # Bottom of your domain
mod_wake = 1  # Wake model. 1: Polar, 2: Curl, 3: Cartesian

# ----------- Desired sweeps
vhub = [10]       # Wind speed at hub height (m/s)
shear = [0.2]     # Wind shear exponent
TIvalue = [10]    # Turbulence intensity (%)
inflow_deg = [0]  # Wind direction (degrees)

# ----------- Turbine parameters
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = [[0.0]]

# ----------- Low- and high-res boxes parameters
# High-res boxes settings
dt_high_les = 0.5  # Sampling frequency of high-res files
ds_high_les = 5.0  # dx, dy, dz for high-res files
extent_high = 1.2  # High-res box extent in y and x for each turbine, in D.
# Low-res boxes settings
dt_low_les = 3  # Sampling frequency of low-res files
ds_low_les = 20.0  # dx, dy, dz of low-res files
extent_low = [3, 8, 3, 3, 2]  # Extent in xmin, xmax, ymin, ymax, zmax, in D.

# ----------- Execution parameters
ffbin = 'fastfarm/offshoreWTs_zxj/FAST.Farm_x64_341.exe'

# ----------- LES parameters. Use TurbSim-driven inflow
LESpath = None

# ----------- Template files
templatePath = 'fastfarm\\5MW_OC4Semi_WSt_WavesWN'

EDfilename = 'NRELOffshrBsline5MW_OC4DeepCwindSemi_ElastoDyn.dat'
SEDfilename = None 
HDfilename = 'NRELOffshrBsline5MW_OC4DeepCwindSemi_HydroDyn.dat'  
SrvDfilename = 'NRELOffshrBsline5MW_OC4DeepCwindSemi_ServoDyn.dat'   # ServoDyn not needed for control
ADfilename = 'NRELOffshrBsline5MW_OC3Hywind_AeroDyn15.dat'
ADskfilename = None  
SubDfilename = None 
IWfilename = 'NRELOffshrBsline5MW_InflowWind_12mps.dat'
BDfilepath = None  # BeamDyn not used
bladefilename = 'NRELOffshrBsline5MW_BeamDyn_Blade.dat'
towerfilename = 'NRELOffshrBsline5MW_OC4DeepCwindSemi_ElastoDyn_Tower.dat'
turbfilename = '5MW_OC4Semi_WSt_WavesWN.fst'

libdisconfilepath = None  # Control library not needed
controllerInputfilename = None  # Control input not needed
coeffTablefilename = None  
FFfilename = 'FAST.Farm_mode.fstf'

# TurbSim setups
turbsimLowfilepath = 'fastfarm\TSinflow\90m_08mps_mod1.inp'
turbsimHighfilepath = 'fastfarm\TSinflow\90m_08mps_mod1.inp'

# ---------------------------------------------------------------------
# END OF USER INPUT
# ---------------------------------------------------------------------

# Initial setup
case = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg, dt_high_les, ds_high_les, extent_high, dt_low_les, ds_low_les, extent_low, ffbin=ffbin, mod_wake=mod_wake, yaw_init=yaw_init, nSeeds=nSeeds, LESpath=LESpath, refTurb_rot=refTurb_rot, verbose=1)

case.setTemplateFilename(templatePath, EDfilename, SEDfilename, HDfilename, SrvDfilename, ADfilename, ADskfilename, SubDfilename, IWfilename, BDfilepath, bladefilename, towerfilename, turbfilename, libdisconfilepath, controllerInputfilename, coeffTablefilename, turbsimLowfilepath,turbsimHighfilepath, FFfilename)
# print('='*100)
# print(vars(case)) 


# Get domain parameters
case.getDomainParameters()

print(f'get domain parameter')

# Organize file structure
case.copyTurbineFilesForEachCase()

print('Organize file structure')

if LESpath is None:
    case.TS_low_setup()

    case.TS_high_setup()


# Final setup
case.FF_setup()
