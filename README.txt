#**********************************
# Required modules
#**********************************
Reanalysis.py             #  Handle reanalysis data (plain binary)
    |
    |-- detect_fsub.f90   # fortran module for detections
    |-- JRA55.py          # Handle JRA55  (plain binary)
    |-- JRA25.py          # Handle JRA25  (plain binary)

Cyclone.py                # Handle cyclone data
    |
    |-- detect_fsub.f90   # fortran module for detections
    |-- ConstCyclone      # paramers for cyclone detection
    |-- BestTrackTC       # handle best track TC data. Comment out if not necessary
        |
        |-- IBTrACS.py    # handle TC best track data IBTrACS (Knapp et al., 2010)

Front.py
    |
    |-- detect_fsub.f90   # fortran module for detections
    |-- front_fsub.f90    # fortran module for front detection
    |-- ConstFront.py     # parameters for front detection
    |-- Reanalysis.py     # handle reanalysis data
      

 
#**********************************
# Cyclones
#**********************************
#---------------------------
#--- Extratropical cyclone (ExC) centers 
#---------------------------
python ./f2py.make.py detect_fsub.f90   # Compile fortran code as python module
python ./c.runmean.wind.py              # Create running mean wind speed  
python ./c.findcyclone.py               # Find cyclone-center candidates
python ./c.connectc.fwd.py              # Track cyclones (forward)
python ./c.connectc.bwd.py              # Track cyclones (backward)
python ./c.mk.clist.obj.py              # Create cyclone list file

#---------------------------
#--- Tropical cyclone (TC) centers      # After the ExCs detection !!
#---------------------------
python ./tc.mk.clist.obj.py             # Create TC list file
python ./tc.mk.clist.obj.initState.py   # Create list file for TC initial position&time

#---------------------------
#--- Create 2D maps for ExC-centers and TC-centers
#---------------------------
python ./c.write.cyclone.py             # Create 2D maps for cyclone centers
python ./c.write.mask.py                # Create 2D masps for masks (with specified radius)

#**********************************
# Front 
#**********************************
python ./f2py.make.py front_fsub.f90    # Compile fortran code as python module
python ./f.mk.orogdata.py               # Create orographic parameter map
python ./f.mk.potloc.obj.py             # Create front candidates
python ./f.write.front.py               # Create front 2D map
python ./f.write.mask.py                # Create 2D masps for masks (with specified radius)

#**********************************
# Handle weather system masks
#**********************************
Tag.py



