# This program generates an srad file with forbid constraints for overfly
# routes in China. 
#
#It needs the files 'create_forbid_segments.py' and'parse_date.py' 
#in the same folder. 
#and the files 'NAVDATA_POINTS',
# 'NAVDATA_SEGMENTS' and '_CHINA_MANDATE_OVERFLIGHT.srad' in the folder
# '../data/'

import create_forbid_segments as cfs

forbidden_segs = cfs.getForbiddenSegments()


