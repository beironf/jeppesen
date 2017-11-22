
class ConfirmSolution(object):
    def __init__(self, forbidden_seqs, forbidden_entry_segs, segments, points, entry_nodes, exit_nodes, allowed_nodes):
        self.forbidden_seqs = forbidden_seqs
        self.forbidden_entry_segs = forbidden_entry_segs
        self.segments = segments
        self.points = points
        self.entry_nodes = entry_nodes
        self.possible_routes = []
        self.exit_nodes = exit_nodes
        self.allowed_nodes = allowed_nodes

    def isForbidden(self, seg, used_segs):
        if used_segs[0]['from'] in self.entry_nodes:
            seqs = [seg]
            # get all two-joined combinations + seg
            if len(used_segs)>1:
                for i in range(len(used_segs)-2):
                    seqs.append([used_segs[i],used_segs[i+1],seg])
            # test if some of these seqs are forbidden
            for seq in seqs:
                if seq in self.forbidden_seqs[used_segs[0]['from']]:
                    return True
        else:
            return False

    def getSegments(self, fr):
        segs = [seg for seg in self.segments if seg['from']==fr]
        return segs

    def find_path(self, seg, used_segs):
        node = seg['to']
        if (node in self.exit_nodes or (self.points[node]['area'][0]!='Z' and node not in self.allowed_nodes)):
            self.possible_routes.append(used_segs)
        else:
            for sg in self.getSegments(node):
                if not(self.isForbidden(sg, used_segs)):
                    used_segs_tmp = used_segs[:] # needs [:] (otherwise used_segs_tmp will point to used_segs and change it as well)
                    used_segs_tmp.append(sg)
                    self.find_path(sg, used_segs_tmp)

    def getPossibleRoutes(self):
        start_segs = []
        
        [start_segs.extend(self.getSegments(node)) for node in self.entry_nodes]
        
        for start_seg in start_segs:
            used_segs = [start_seg]
            if not(self.isForbidden(start_seg, used_segs)):
                self.find_path(start_seg, used_segs)

        return self.possible_routes
