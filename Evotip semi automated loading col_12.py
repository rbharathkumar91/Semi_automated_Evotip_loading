#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import opentrons.execute
from opentrons import protocol_api
metadata = {
    'protocolName': 'Evotip semi-automated loading OT2_col_12 ',
    'author': 'Name <bkr@evosep.com>',
    'description': 'Evotip loading using the OT-2',
    'apiLevel': '2.12'
}
def run(protocol: protocol_api.ProtocolContext):
    
    #turn on robot rail lights
    protocol.rail_lights_on
    
    #homing 
    protocol.home()

    # labware
    
    
    Sampleplate = protocol.load_labware('grenier_96_wellplate_300ul', location='4') 
    Reservoir = protocol.load_labware('homemade_4_reservoir_40000ul',location='9' )
    EvotipBox= protocol.load_labware('evotipboxv2_96_wellplate_200ul',location='3' )
    tiprack300_1 =protocol.load_labware('opentrons_96_tiprack_300ul', location='10')
    tiprack300_2 =protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    
    

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_multi_gen2', mount='left', tip_racks=[tiprack300_1,tiprack300_2])
    
    left_pipette.flow_rate.aspirate = 80
    left_pipette.flow_rate.dispense = 70
    
    left_pipette.default_speed = 300
   
    #columns
    col=12
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.1
    left_pipette.well_bottom_clearance.dispense = 3.3
    
    
    #Adding 0.1% FA to the digestion plate
    
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_1.well('A6')
    left_pipette.pick_up_tip()
    for i in range(col):
        left_pipette.transfer (300, Reservoir.columns_by_name()['2'], Sampleplate.columns()[i], new_tip='never', mix_before= (1,250), blow_out=True,blowout_location='destination well')
    left_pipette.return_tip() 
   
    
    
    
   #Mixing the sample plate to reconstitute the peptides
  
    left_pipette.starting_tip = tiprack300_2.well('A1')
    location=['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    
    for i in range(col):
        pos=location[i]
        left_pipette.pick_up_tip()
        left_pipette.mix (3, 240, Sampleplate[pos])
        left_pipette.return_tip()
        
    
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.7
    left_pipette.well_bottom_clearance.dispense = 32
    
    #100 %ACN reservoir to Evotip box
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_1.well('A5')
    left_pipette.pick_up_tip()
   
    left_pipette.distribute(22, Reservoir.columns_by_name()['1'], [EvotipBox.columns_by_name()[column] for column in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']],new_tip='never',trash=False, touch_tip=True)
    left_pipette.return_tip()   
    
    protocol.home()
    protocol.pause('Do isopropanol soak, Centrifuge, and resume protocol')
    
    
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 32
   
    
    
   #0.1% FA reservoir to Evotip box
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_1.well('A6')
    left_pipette.pick_up_tip()
   
    left_pipette.distribute(22, Reservoir.columns_by_name()['2'], [EvotipBox.columns_by_name()[column] for column in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']],new_tip='never',trash=False)
    left_pipette.return_tip()   
    
    protocol.home()
    protocol.pause('Centrifuge and resume protocol')
    
    
     
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 1.3
    left_pipette.well_bottom_clearance.dispense = 32
   
    
    
    
   #Sample to evotips
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_2.well('A1')
    
    for i in range(12):
        left_pipette.transfer (20, Sampleplate.columns()[i], EvotipBox.columns()[i], mix_before= (1,250), trash=True,blow_out=True,blowout_location='destination well')
    
    
    protocol.home()
    protocol.pause('Centrifuge and resume protocol')
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 32
   
    
    
    
   #0.1% FA reservoir to Evotip box for washing the tips
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_1.well('A7')
    left_pipette.pick_up_tip()
   
    left_pipette.distribute(100, Reservoir.columns_by_name()['3'], [EvotipBox.columns_by_name()[column] for column in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']],new_tip='never',trash=False)
    left_pipette.return_tip() 
    
    protocol.home()
    

