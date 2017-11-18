
class ConfirmSolution(object):
    def __init__(self, forbidden_segs, forbidden_entry_segs, segments, points, entry_nodes, exit_nodes):

        self.forbidden_segs = forbidden_segs
        self.forbidden_entry_segs = forbidden_entry_segs
        self.segments = segments
        self.points = points
        self.entry_nodes = entry_nodes
        self.possible_routes = []
        self.exit_nodes = exit_nodes

    def isForbidden(self, seg, entry_seg):
        if entry_seg['from'] in self.entry_nodes:
            if seg in self.forbidden_segs[entry_seg['from']]:
                return True
        else:
            return False

    def getSegments(self, fr):
        segs = [seg for seg in self.segments if seg['from']==fr]
        return segs

    def find_path(self, seg, used_segs):
        node = seg['to']

        if (node in self.exit_nodes or self.points[node]['area'][0]!='Z'):
            self.possible_routes.append(used_segs)
        
        else:
            for sg in self.getSegments(node):
                if not(self.isForbidden(sg, used_segs[0])):
                    used_segs_tmp = used_segs[:] # needs [:] (otherwise used_segs_tmp will point to used_segs and change it as well)
                    used_segs_tmp.append(sg)
                    self.find_path(sg, used_segs_tmp)


    def getPossibleRoutes(self):
        start_segs = []
        
        [start_segs.extend(self.getSegments(node)) for node in self.entry_nodes]
        
        for start_seg in start_segs:
            used_segs = [start_seg]
            if not(self.isForbidden(start_seg, used_segs[0])):
                self.find_path(start_seg, used_segs)

        return self.possible_routes

