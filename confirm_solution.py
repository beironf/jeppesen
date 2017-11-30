
class ConfirmSolution(object):
    def __init__(self, forbidden_seqs, forbidden_entry_segs, segments, points, entry_nodes, exit_nodes, allowed_nodes, chinese_areas):
        self.forbidden_seqs = forbidden_seqs
        self.forbidden_entry_segs = forbidden_entry_segs
        self.segments = segments
        self.points = points
        self.entry_nodes = entry_nodes
        self.possible_routes = []
        self.exit_nodes = exit_nodes
        self.allowed_nodes = allowed_nodes
        self.chinese_areas = chinese_areas

    def isSubsetInOrder(self, a, b):
        if type(a) is dict:
            a = [a]
        if type(b) is dict:
            b = [b]
        if len(a)>len(b):
            return False
        else:
            j_start = 0
            count = 0
            for i in range(len(a)):
                for j in range(j_start, len(b)):
                    if a[i]==b[j]:
                        j_start = j+1
                        count = count+1
                        break
            return count == len(a)

    def getNodes(self, seq):
        if type(seq) is dict:
            seq = [seq]
        nodes = [seq[0]['from']]
        [nodes.append(seg['to']) for seg in seq]
        return nodes

    def isForbidden(self, seg, used_segs):
        if used_segs:
            if seg['to'] in self.getNodes(used_segs):
                return True
            seq = used_segs+[seg]
            for forbid in self.forbidden_seqs[seq[0]['from']]:
                if self.isSubsetInOrder(forbid, seq):
                    return True
            return False
        else:
            if seg in self.forbidden_seqs[seg['from']]:
                return True
            else:
                return False

    def getSegments(self, fr):
        segs = [seg for seg in self.segments if seg['from']==fr]
        return segs

    def find_path(self, seg, used_segs):
        node = seg['to']
        used_segs_tmp = used_segs+[seg]
        if node in self.exit_nodes or (self.points[node]['area'][0:2] not in self.chinese_areas and node not in self.allowed_nodes):
            self.possible_routes.append(used_segs_tmp)
        else:
            for sg in self.getSegments(node):
                if not self.isForbidden(sg, used_segs_tmp):
                    self.find_path(sg, used_segs_tmp)

    def getPossibleRoutes(self):
        start_segs = []
        [start_segs.extend(self.getSegments(node)) for node in self.entry_nodes]
                
        for start_seg in start_segs:
            used_segs = []
            if not self.isForbidden(start_seg, used_segs):
                self.find_path(start_seg, used_segs)

        return self.possible_routes
