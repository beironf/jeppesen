
class ConfirmSolution(object):
	def __init__(self, forbidden_segs, forbidden_entry_segs, segments, points, entry_nodes):
		self.forbidden_segs = forbidden_segs
		self.forbidden_entry_segs = forbidden_entry_segs
		self.segments = segments
		self.points = points
		self.entry_nodes = entry_nodes
		self.possible_routes = []

	def isForbidden(self, seg, entry_seg):
		if entry_seg['from'] in self.entry_nodes:
			if seg in self.forbidden_segs[entry_seg['from']]:
				return True
		elif entry_seg['to'] in self.entry_nodes:
			if seg in self.forbidden_segs[entry_seg['to']]:
				return True
		else:
			if seg in self.forbidden_entry_segs:
				return True
			else:
				return False

	def getSegments(self, fr):
		segs = [seg for seg in self.segments if seg['from']==fr]
		return segs

	def find_path(self, seg, used_segs):
		node = seg['to']
		for seg in self.getSegments(node):
			if (to in self.entry_nodes or self.points[to]['area'][0]!='Z'):
				used_segs.append(seg)
				self.possible_routes.append(used_segs)
			elif not(self.isForbidden(seg, used_segs[0])):
				used_segs.append(seg)
				self.find_path(seg, used_segs)


	def getPossibleRoutes(self):
		start_segs = []
        
		for seg in self.segments:
			fr = self.points[seg['from']]['area'][0]
			to = self.points[seg['to']]['area'][0]
			if (fr != 'Z' and to == 'Z'): # if seg is from another country to China
				start_segs.append(seg)

		for start_seg in start_segs:
			used_segs = [start_seg]
			if not(self.isForbidden(start_seg, used_segs[0])):
				self.find_path(start_seg, used_segs)

		return self.possible_routes

