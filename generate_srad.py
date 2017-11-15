# This program generates an srad file with forbid constraints for overfly
# routes in China. 

import create_forbid_segments as cfs

#forbidden_segs = cfs.createForbiddenSegments()
FIR = open('../data/_CHINA_MANDATE_OVERFLIGHT.srad', 'r')
sourcelines = FIR.readlines()
FIR.close()

sourcelines = sourcelines[2:31]

srad = open('_CHINA_FORBID_OVERFLIGHT.srad', 'w')

srad.write(
          "(SuluRad 1 0)\n"
          "(Restriction \"FORBIDDEN ENTRY SEGMENTS\" F \"Forbidden rules for China overflight\" \"Auto generated by script\" ()\n" 
          )
for line in sourcelines:
    srad.write(line)
srad.write()


srad.close()
